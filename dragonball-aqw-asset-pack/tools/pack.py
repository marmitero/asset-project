#!/usr/bin/env python3
"""Empacotamento: manifes do personagem + manifesto do pack + checksums.

Os GIFs de validação são renderizados direto em
`exports/characters/<ID>/previews/<Vxx>/`; este script só consolida metadados.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "exports"
CHAR_ID = "DB_CHAR_HERO_GOKU_BASE"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build() -> dict:
    dst = EXPORTS / "characters" / CHAR_ID
    entries = []
    for gif in sorted((dst / "previews").rglob("*.gif")):
        entries.append({
            "id": gif.parent.name,
            "clip": gif.stem.split("__")[1] if "__" in gif.stem else gif.stem,
            "type": "gif",
            "path": str(gif.relative_to(EXPORTS)).replace("\\", "/"),
            "bytes": gif.stat().st_size,
            "sha256": sha256(gif),
        })

    integrity = ROOT / "production" / "qa_reports" / f"{CHAR_ID}__anim.json"
    qa = {}
    if integrity.exists():
        qa = json.loads(integrity.read_text(encoding="utf-8")).get("summary", {})

    manifest = {
        "asset_id": CHAR_ID,
        "asset_type": "character",
        "version": "0.1.0",
        "state": "REVIEW",              # G3 pendente
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "canvas": {"width": 512, "height": 512, "ground_y": 448, "height_px": 220},
        "rig": "DB_RIG_HUMANOID_MALE_A",
        "fps": {"authoring": 24, "sample": 60, "gif": 25},
        "clips": sorted({e["clip"] for e in entries}),
        "files": entries,
        "qa": {"validator": "validate_animation.py", "clips_checked": qa.get("clips", 0),
               "errors": qa.get("errors", 0), "pass": qa.get("pass", False)},
        "license": "fan_art_non_commercial",
    }
    (dst / f"{CHAR_ID}.manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    pack = {
        "pack": "AURA — Dragon Ball x AQW asset pack",
        "version": "0.1.0",
        "matrix_version": "0.0.0 (nao congelada)",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "canvas": {"character": [512, 512], "ground_y": 448, "viewport": [1280, 720]},
        "fps": {"authoring": 24, "sample": 60, "gif": 25},
        "characters": [{"id": CHAR_ID, "version": "0.1.0",
                        "manifest": f"characters/{CHAR_ID}/{CHAR_ID}.manifest.json",
                        "clips": len(manifest["clips"]), "files": len(entries)}],
        "totals": {"files": len(entries), "bytes": sum(e["bytes"] for e in entries)},
    }
    (EXPORTS / "PACK_MANIFEST.json").write_text(
        json.dumps(pack, indent=2, ensure_ascii=False), encoding="utf-8")

    # checksums.sha256 (formato sha256sum)
    lines = []
    for f in sorted(EXPORTS.rglob("*")):
        if f.is_file() and f.name != "checksums.sha256":
            lines.append(f"{sha256(f)}  {f.relative_to(EXPORTS)}")
    (EXPORTS / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return pack


if __name__ == "__main__":
    p = build()
    print(f"exports/ prontos: {p['totals']['files']} arquivos, "
          f"{p['totals']['bytes'] / 1048576:.1f} MB")
