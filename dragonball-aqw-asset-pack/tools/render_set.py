"""Renderiza o conjunto de validação V01–V18 e grava GIFs + relatório de métricas."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image

from aura import clips
from aura.anim import Clip
from aura.export import export_clip, save_gif
from aura.parts_goku import build_goku_parts
from aura.pose import Skeleton
from aura.render import ClipRenderer, ShowConfig, clip_to_gif_frames
from aura.rig import ActorRig, load_layers

ROOT = Path(__file__).resolve().parents[1]
CHAR_ID = "DB_CHAR_HERO_GOKU_BASE"
# os GIFs sao o entregavel do G3: vivem em exports/ (unica copia, sem duplicar)
OUT = ROOT / "exports" / "characters" / CHAR_ID / "previews"


def build_rig():
    parts = {k: v.build() for k, v in build_goku_parts().items()}
    skel = Skeleton.load(ROOT / "standards" / "skeleton_humanoid.json")
    rig = ActorRig(skel, parts, load_layers(ROOT / "standards" / "layer_order.json"),
                   skel.data["secondary_chains"])
    return skel, rig, parts


def compose(name: str, parts: list[tuple[Clip, int | None]]) -> Clip:
    """Concatena clipes (fatiados) em um clipe único."""
    keys, events, off = [], [], 0
    for clip, cut in parts:
        n = clip.frames if cut is None else cut
        for f, p, e in clip.keys:
            if f > n:
                break
            keys.append((off + f, p, e))
        for ev in clip.events:
            if ev["frame"] <= n:
                ev = dict(ev)
                ev["frame"] += off
                events.append(ev)
        off += n
    return Clip(name, off, keys, loop=False, fps=24, events=events)


def montage() -> Clip:
    seq = [("idle_combat", 10), ("walk", 12), ("run", 8), ("attack_light_1", 18),
           ("attack_light_2", 20), ("attack_light_3", 22), ("hurt_light", 12),
           ("attack_crit", 18)]
    return compose("montage_combat", [(clips.get(n), c) for n, c in seq])


def block_dodge() -> Clip:
    return compose("block_impact+dodge",
                   [(clips.get("block_impact"), None), (clips.get("dodge"), None)])


SETS = [
    ("V01", lambda: clips.get("idle"), "grid", "idle — respiracao + blink", True),
    ("V02", lambda: clips.get("idle_combat"), "dojo", "idle_combat — guarda", True),
    ("V03", lambda: clips.get("walk"), "paozu", "walk — 8 poses", True),
    ("V04", lambda: clips.get("run"), "paozu", "run — corrida com airtime", True),
    ("V05", lambda: clips.get("turn_180"), "grid", "turn_180 — virada", False),
    ("V06", lambda: clips.get("jump_land"), "paozu", "jump_land — salto/queda/aterrissagem", False),
    ("V07", lambda: clips.get("attack_light_1"), "dojo", "attack_light_1 — jab", False),
    ("V08", lambda: clips.get("attack_heavy"), "dojo", "attack_heavy — soco carregado", False),
    ("V09", lambda: clips.get("combo_light_3"), "dojo", "combo_light_3 — 3 golpes", False),
    ("V10", lambda: clips.get("cast"), "void", "cast — ki blast", False),
    ("V11", lambda: clips.get("attack_whiff"), "dojo", "attack_whiff — erro (miss)", False),
    ("V12", lambda: clips.get("evade_backstep"), "grid", "evade_backstep — esquiva", False),
    ("V13", lambda: clips.get("attack_crit"), "dojo", "attack_crit — critico", False),
    ("V14", lambda: clips.get("hurt_light"), "grid", "hurt_light — dano leve", False),
    ("V15", lambda: clips.get("hurt_crit"), "grid", "hurt_crit — dano critico", False),
    ("V16", lambda: clips.get("death"), "grid", "death — morte", False),
    ("V17", block_dodge, "grid", "block_impact + dodge", False),
    ("V18", montage, "dojo", "montage_combat — resumo jogavel", True),
]


def main(only: list[str] | None = None, zoom: float = 1.35):
    skel, rig, _ = build_rig()
    renderer = ClipRenderer(rig, skel)
    report = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "fps_gif": 25, "zoom": zoom, "items": []}
    t_all = time.time()
    for vid, factory, bg, caption, loop in SETS:
        if only and vid not in only:
            continue
        clip = factory()
        combat = vid in ("V11", "V12", "V13", "V14", "V15", "V17", "V18")
        cfg = ShowConfig(background=bg, zoom=zoom, caption=f"{vid}  {caption}",
                         show_timeline=False, show_hud=True,
                         dummy=combat, dummy_x=0.755 if combat else 0.79,
                         dummy_scale=0.95, feedback=combat)
        t0 = time.time()
        rc = clip_to_gif_frames(clip, renderer, cfg)
        d = OUT / vid
        info = export_clip(rc, d, gif=True, apng=False, sheet=False, contact=False,
                           loop=loop, prefix=f"{CHAR_ID}__", suffix="__v0.1.0")
        # folha de contato só para QA local (não vai para o pacote)
        from aura.export import save_contact_sheet
        save_contact_sheet(rc.frames, f"/tmp/qa/{vid}_{clip.name}_contact.png",
                           columns=6, thumb=0.34, label=f"{vid} {clip.name}")
        info.update({"id": vid, "clip": clip.name, "caption": caption,
                     "loop": loop, "render_s": round(time.time() - t0, 2)})
        report["items"].append(info)
        print(f"{vid} {clip.name:18s} {len(rc.frames):3d}f  "
              f"{time.time()-t0:5.1f}s  {sum(f['bytes'] for f in info['files'])//1024:4d} KB")
    report["total_s"] = round(time.time() - t_all, 1)
    (OUT / "render_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"total {report['total_s']}s -> {OUT}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a.startswith("V")]
    main(args or None)
