#!/usr/bin/env python3
"""Verifica links internos em markdown (docs/, README, PLAN)."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / "README.md", ROOT / "PLAN.md"] + sorted((ROOT / "docs").rglob("*.md"))
BAD, TOTAL = [], 0
for f in FILES:
    if not f.exists():
        continue
    text = f.read_text(encoding="utf-8")
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        target = m.group(2).split("#")[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        TOTAL += 1
        p = (f.parent / target).resolve()
        if not p.exists():
            BAD.append((f.relative_to(ROOT), target))
print(f"{len(FILES)} arquivos · {TOTAL} links internos · {len(BAD)} quebrados")
for f, t in BAD:
    print(f"  x {f} -> {t}")
sys.exit(1 if BAD else 0)
