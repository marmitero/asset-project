"""Diagnostico do braco de tras: mede a fracao VISIVEL de cada peca traseira.

Nao altera nada. Gera um relatorio e uma folha de contato dos piores frames.

Uso: python3 experiments/occlusion/diagnose.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from aura import clips  # noqa: E402
from aura.anim import pose_from_params  # noqa: E402
from aura.core import PartImage  # noqa: E402
from aura.parts_goku import build_goku_parts  # noqa: E402
from aura.pose import Skeleton  # noqa: E402
from aura.rig import ActorRig, load_layers  # noqa: E402

BACK = ("upper_arm_b", "forearm_b", "hand_b", "thigh_b", "shin_b", "foot_b")
FRONT_OCCLUDERS = ("torso", "pelvis")

ALL_CLIPS = ["idle", "idle_combat", "walk", "run", "jump_start", "fall", "land",
             "jump_land", "death", "turn_180", "attack_light_1", "attack_light_2",
             "attack_light_3", "combo_light_3", "attack_heavy", "attack_crit",
             "attack_whiff", "cast", "hurt_light", "hurt_crit", "dodge",
             "evade_backstep", "block_impact"]


def build_parts():
    return {k: v.build() for k, v in build_goku_parts().items()}


def solo_render(base_parts, skel, keep: set[str], pose):
    """Renderiza apenas as pecas em `keep` (copia o dict para nao vazar estado)."""
    local = {}
    for k, v in base_parts.items():
        if k in keep:
            local[k] = v
        else:
            local[k] = PartImage(name=k, image=Image.new("RGBA", v.size, (0, 0, 0, 0)),
                                 pivot=v.pivot, z=v.z, bone=v.bone)
    rig = ActorRig(skel, local, load_layers(ROOT / "standards" / "layer_order.json"),
                   skel.data["secondary_chains"])
    rig.attachments.update({"face": "face_combat", "hair_front": "hair_front"})
    img, _ = rig.render(pose, facing=1, zoom=1.0, out_size=(512, 512),
                        shadow=False, ground_clamp=False)
    return np.array(img)[:, :, 3] > 60


def main():
    base = build_parts()
    skel = Skeleton.load(ROOT / "standards" / "skeleton_humanoid.json")
    rows = []
    for name in ALL_CLIPS:
        c = clips.get(name)
        for f in range(0, c.frames, 2):
            pose = pose_from_params(c.sample(float(f)), skel)
            occ = np.zeros((512, 512), bool)
            for k in FRONT_OCCLUDERS:
                occ |= solo_render(base, skel, {k}, pose)
            for part in ("upper_arm_b", "forearm_b", "hand_b"):
                a = solo_render(base, skel, {part}, pose)
                tot = int(a.sum())
                if tot < 40:
                    continue
                vis = int((a & ~occ).sum())
                frac = vis / tot
                if frac < 0.55:            # começa a virar lasca
                    rows.append((name, f, part, tot, vis, frac))
    rows.sort(key=lambda r: r[5])
    print(f"{'clipe':18s} {'f':>3s} {'peca':14s} {'total':>6s} {'vis':>6s} {'%':>6s}")
    for r in rows[:30]:
        print(f"{r[0]:18s} {r[1]:3d} {r[2]:14s} {r[3]:6d} {r[4]:6d} {100*r[5]:5.1f}%")
    print(f"\n{len(rows)} ocorrencias de peca traseira <55% visivel")
    return rows


if __name__ == "__main__":
    main()
