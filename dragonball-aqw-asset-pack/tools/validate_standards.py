#!/usr/bin/env python3
"""
AURA — validador de padroes (Fase 1).

Valida a consistencia interna dos JSONs de standards/ e production/.
Nao valida arte (nao existe arte ainda); valida contratos.

Uso:
    python3 tools/validate_standards.py
    python3 tools/validate_standards.py --root .
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"^DB_[A-Z0-9]+(_[A-Z0-9]+){2,5}$")
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
COMPOSITE_CLIPS = {
    "jump_land", "combo_light_3", "evade_backstep", "block_impact+dodge", "montage_combat",
}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def load(path: Path):
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:  # noqa: BLE001
        err(f"{path}: JSON invalido: {exc}")
        return None


def walk_ids(node, path="") -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}.{key}" if path else key
            if key == "asset_id" and isinstance(value, str):
                if value.startswith("DB_") and not ID_RE.match(value):
                    err(f"{here}: asset_id fora do padrao: {value}")
            walk_ids(value, here)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            walk_ids(value, f"{path}[{i}]")


def collect_hex(node, path="") -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            collect_hex(value, f"{path}.{key}" if path else key)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            collect_hex(value, f"{path}[{i}]")
    elif isinstance(node, str) and node.startswith("#"):
        if not HEX_RE.match(node):
            err(f"{path}: cor invalida {node}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    standards = root / "standards"
    if not standards.is_dir():
        print(f"ERRO: {standards} nao existe", file=sys.stderr)
        return 2

    # 1. Parse de todos os JSONs
    jsons: dict[str, dict] = {}
    for path in sorted(list(standards.glob("*.json")) + list((root / "production").glob("*.json"))):
        data = load(path)
        if data is not None:
            jsons[path.name] = data
            walk_ids(data, path.name)

    for path in [root / "asset_manifest.json"]:
        if path.exists():
            data = load(path)
            if data is not None:
                jsons[path.name] = data

    # 2. Layer order
    layer = jsons.get("layer_order.json")
    layer_z: set[int] = set()
    layer_slots: set[str] = set()
    if layer:
        for row in layer.get("layers", []):
            z, slot = row.get("z"), row.get("slot")
            if z in layer_z:
                err(f"layer_order: z duplicado {z}")
            layer_z.add(z)
            if slot in layer_slots:
                err(f"layer_order: slot duplicado {slot}")
            layer_slots.add(slot)
        if len(layer.get("layers", [])) != 29:
            err(f"layer_order: esperado 29 camadas, encontrado {len(layer.get('layers', []))}")

    # 3. Skeleton
    sk = jsons.get("skeleton_humanoid.json")
    bones: dict[str, dict] = {}
    if sk:
        names = set()
        for b in sk.get("bones", []):
            name = b.get("name")
            if name in names:
                err(f"skeleton: osso duplicado {name}")
            names.add(name)
            bones[name] = b
            limit = b.get("limit_deg")
            if limit and (len(limit) != 2 or limit[0] > limit[1]):
                err(f"skeleton: limite invalido em {name}: {limit}")
        for b in sk.get("bones", []):
            parent = b.get("parent")
            if parent is not None and parent not in bones:
                err(f"skeleton: pai inexistente {parent} (filho {b.get('name')})")
        if len(sk.get("bones", [])) != 29:
            err(f"skeleton: esperado 29 ossos, encontrado {len(sk.get('bones', []))}")
        for slot in sk.get("slots", []):
            if slot.get("layer") not in layer_z:
                err(f"skeleton: slot {slot.get('slot')} usa camada inexistente {slot.get('layer')}")
            if slot.get("bone") not in bones:
                err(f"skeleton: slot {slot.get('slot')} usa osso inexistente {slot.get('bone')}")
        for sock in sk.get("sockets", []):
            if sock.get("bone") not in bones:
                err(f"skeleton: socket {sock.get('name')} usa osso inexistente {sock.get('bone')}")
        if set(layer_slots) != {s.get("slot") for s in sk.get("slots", [])}:
            warn("skeleton/slots e layer_order divergem em nomes de slot")

    # 4. Clip matrix
    cm = jsons.get("clip_matrix.json")
    clip_ids: set[str] = set()
    if cm:
        for clip in cm.get("clips", []):
            cid = clip.get("id")
            if cid in clip_ids:
                err(f"clip_matrix: clipe duplicado {cid}")
            clip_ids.add(cid)
            frames = clip.get("frames")
            for ev in clip.get("events", []):
                if ev.get("frame", 0) > frames:
                    err(f"clip_matrix: evento fora da duracao em {cid}: frame {ev.get('frame')} > {frames}")
            if clip.get("loop") and "closing_frame" not in cm.get("conventions", {}):
                err("clip_matrix: convencao de closing frame ausente")
        fm = set(cm.get("first_model_set", []))
        if not fm <= clip_ids:
            err(f"clip_matrix: first_model_set referencia clipes inexistentes: {sorted(fm - clip_ids)}")
        for gif in cm.get("validation_gifs", []):
            cid = gif.get("clip")
            if cid in COMPOSITE_CLIPS:
                continue
            if cid not in clip_ids:
                err(f"clip_matrix: GIF {gif.get('id')} referencia clipe inexistente {cid}")
            elif gif.get("frames") != next(c["frames"] for c in cm["clips"] if c["id"] == cid):
                warn(f"clip_matrix: GIF {gif.get('id')} tem frames diferente do clipe {cid}")
        if len(cm.get("validation_gifs", [])) != 18:
            err("clip_matrix: esperado 18 GIFs de validacao")

    # 5. Palette
    pal = jsons.get("palette_master.json")
    if pal:
        collect_hex(pal, "palette_master")
        forms = pal.get("forms", {})
        for name, form in forms.items():
            for key in ("hair", "hair_shadow", "hair_highlight"):
                if key in form and not HEX_RE.match(form[key]):
                    err(f"palette_master.forms.{name}.{key}: cor invalida")

    # 6. Canvas
    canvas = jsons.get("canvas_and_scale.json")
    if canvas:
        ref = canvas.get("reference", {})
        if ref.get("character_height_px") != 220:
            err("canvas: character_height_px deve ser 220")
        if ref.get("canvas") != [512, 512]:
            err("canvas: canvas de personagem deve ser 512x512")
        if ref.get("ground_y_px") != 448:
            err("canvas: ground_y deve ser 448")

    # 7. Manifesto
    manifest = jsons.get("asset_manifest.json")
    if manifest is not None:
        if manifest.get("assets") != []:
            warn("manifesto nao esta vazio; confirme se ha assets aprovados na Fase 1")
        if manifest.get("pack") != "dragonball-aqw-asset-pack":
            err("manifesto: pack incorreto")

    # 8. Backlog: IDs
    backlog = jsons.get("production_backlog.json")
    if backlog:
        for item in backlog.get("items", []):
            aid = item.get("asset_id", "")
            if aid.startswith("DB_") and not ID_RE.match(aid):
                err(f"backlog: asset_id invalido {aid}")

    # 9. Resumo
    print("AURA — validacao de padroes")
    print(f"JSONs lidos: {len(jsons)}")
    print(f"Ossos: {len(bones)} | Camadas: {len(layer_z)} | Clipes: {len(clip_ids)}")
    print(f"GIFs de validacao: {len(cm.get('validation_gifs', [])) if cm else 0}")
    if warnings:
        print("\nAVISOS:")
        for w in warnings:
            print(f"  ! {w}")
    if errors:
        print("\nERROS:")
        for e in errors:
            print(f"  x {e}")
        print(f"\nFALHOU: {len(errors)} erro(s), {len(warnings)} aviso(s)")
        return 1
    print(f"\nOK: 0 erros, {len(warnings)} aviso(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
