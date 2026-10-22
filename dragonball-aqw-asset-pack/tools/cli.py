#!/usr/bin/env python3
"""CLI unificada do pipeline AURA.

    python3 tools/cli.py validate                 # standards + schemas
    python3 tools/cli.py anim                     # 11 métricas de animação
    python3 tools/cli.py preview  --clip idle     # 1 GIF
    python3 tools/cli.py previews                 # V01–V18
    python3 tools/cli.py pack                     # exports/ + manifests
    python3 tools/cli.py check                    # tudo acima + link check
    python3 tools/cli.py stats                    # inventário do pack
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
CHAR_ID = "DB_CHAR_HERO_GOKU_BASE"


def run(cmd: list[str]) -> int:
    print(f"\n$ {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=ROOT)


def cmd_validate(_args) -> int:
    return run([sys.executable, str(TOOLS / "validate_standards.py")])


def cmd_anim(args) -> int:
    cmd = [sys.executable, str(TOOLS / "validate_animation.py")]
    cmd += args.clips or []
    cmd += ["--json", str(ROOT / "production" / "qa_reports" / f"{CHAR_ID}__anim.json")]
    return run(cmd)


def cmd_preview(args) -> int:
    out = ROOT / "exports" / "characters" / CHAR_ID / "previews" / "WIP" / \
        f"{CHAR_ID}__{args.clip}__v0.1.0.gif"
    return run([sys.executable, str(TOOLS / "make_clip.py"), args.clip,
                str(out), "1" if args.hud else "0"])


def cmd_previews(args) -> int:
    cmd = [sys.executable, str(TOOLS / "render_set.py")] + (args.only or [])
    return run(cmd)


def cmd_pack(_args) -> int:
    return run([sys.executable, str(TOOLS / "pack.py")])


def cmd_links(_args) -> int:
    return run([sys.executable, str(ROOT / "scripts" / "check_links.py")])


def cmd_stats(_args) -> int:
    docs = list((ROOT / "docs").rglob("*.md"))
    stds = list((ROOT / "standards").glob("*.json"))
    previews = list((ROOT / "exports").rglob("*.gif"))
    exports = list((ROOT / "exports").rglob("*")) if (ROOT / "exports").exists() else []
    files = exports + docs + stds
    size = sum(f.stat().st_size for f in files if f.is_file())
    print(f"docs        : {len(docs)} arquivos markdown")
    print(f"standards   : {len(stds)} JSON")
    print(f"previews    : {len(previews)} GIFs")
    print(f"exports     : {len([f for f in exports if f.is_file()])} arquivos")
    print(f"pack size   : {size / 1024:.0f} KB")
    return 0


def cmd_check(args) -> int:
    rc = cmd_validate(args)
    rc |= cmd_anim(args)
    rc |= cmd_previews(args)
    rc |= cmd_pack(args)
    print("\n== check concluído ==" if rc == 0 else "\n== check com falhas ==")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser(prog="aura", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate", help="valida standards/schemas").set_defaults(fn=cmd_validate)

    p = sub.add_parser("anim", help="métricas de animação")
    p.add_argument("clips", nargs="*", help="clipes (padrão: todos)")
    p.set_defaults(fn=cmd_anim)

    p = sub.add_parser("preview", help="renderiza um GIF")
    p.add_argument("--clip", default="idle")
    p.add_argument("--hud", action="store_true")
    p.set_defaults(fn=cmd_preview)

    p = sub.add_parser("previews", help="renderiza V01–V18")
    p.add_argument("only", nargs="*")
    p.set_defaults(fn=cmd_previews)

    sub.add_parser("pack", help="monta exports/").set_defaults(fn=cmd_pack)
    sub.add_parser("links", help="checa links internos").set_defaults(fn=cmd_links)
    sub.add_parser("stats", help="inventário").set_defaults(fn=cmd_stats)

    p = sub.add_parser("check", help="validate + anim + previews + pack")
    p.set_defaults(fn=cmd_check)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
