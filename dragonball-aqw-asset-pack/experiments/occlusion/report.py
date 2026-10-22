"""Relatorio de oclusao por clipe, para calibrar poses de braco de tras.

Lista todo frame em que a peca traseira fica entre 0% e 62% visivel (faixa
em que ela aparece como lasca ou entra no fade). Ignora <1% (escondida de
proposito) e >62% (le como braco).

Uso: python3 experiments/occlusion/report.py [clipe]
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

CLIPS = ["idle", "idle_combat", "walk", "run", "jump_start", "fall", "land",
         "jump_land", "death", "turn_180", "attack_light_1", "attack_light_2",
         "attack_light_3", "combo_light_3", "attack_heavy", "attack_crit",
         "attack_whiff", "cast", "hurt_light", "hurt_crit", "dodge",
         "evade_backstep", "block_impact"]

BACK = ("upper_arm_b", "forearm_b", "hand_b")


def _mask(base, skel, keep, pose):
    local = {}
    for k, v in base.items():
        local[k] = v if k in keep else PartImage(
            name=k, image=Image.new("RGBA", v.size, (0, 0, 0, 0)),
            pivot=v.pivot, z=v.z, bone=v.bone)
    rig = ActorRig(skel, local, load_layers(ROOT / "standards" / "layer_order.json"),
                   skel.data["secondary_chains"])
    rig.attachments.update({"face": "face_combat", "hair_front": "hair_front"})
    img, _ = rig.render(pose, facing=1, zoom=1.0, out_size=(512, 512),
                        shadow=False, ground_clamp=False, occlusion_guard=False)
    return np.array(img)[:, :, 3] > 60


def analyse(name: str):
    base = {k: v.build() for k, v in build_goku_parts().items()}
    skel = Skeleton.load(ROOT / "standards" / "skeleton_humanoid.json")
    c = clips.get(name)
    bad = []
    for f in range(c.frames):
        pose = pose_from_params(c.sample(float(f)), skel)
        occ = np.zeros((512, 512), bool)
        for k in ("torso", "pelvis"):
            occ |= _mask(base, skel, {k}, pose)
        for p in BACK:
            a = _mask(base, skel, {p}, pose)
            tot = int(a.sum())
            if tot < 60:
                continue
            frac = int((a & ~occ).sum()) / tot
            if 0.01 < frac < 0.62:
                bad.append((f, p, round(100 * frac, 1)))
    return bad


if __name__ == "__main__":
    targets = [sys.argv[1]] if len(sys.argv) > 1 else CLIPS
    total = 0
    for name in targets:
        bad = analyse(name)
        total += len(bad)
        if bad:
            piores = sorted(bad, key=lambda r: r[2])[:6]
            print(f"{name:18s} {len(bad):3d} frames ruins  piores: {piores}")
    print(f"\nTOTAL: {total} frames com peca traseira em zona de lasca")
