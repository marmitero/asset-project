"""Antes/depois do problema 1 (braco de tras).

Antes: upper_arm_b/forearm_b/hand_b em z 60/61/62 (atras do tronco, z 90).
Depois: z 92/93/94 (acima do tronco), como no AQWorlds.

Uso:  python3 experiments/occlusion/antes_depois.py
Saida: experiments/occlusion/antes_depois.png
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))

from PIL import Image, ImageDraw

from aura import clips
from aura.anim import pose_from_params
from aura.parts_goku import build_goku_parts
from aura.pose import Skeleton
from aura.rig import ActorRig, load_layers

ROOT = pathlib.Path(__file__).resolve().parents[2]
ANTES = {"upper_arm_b": 60, "forearm_b": 61, "hand_b": 62}
DEPOIS = {"upper_arm_b": 92, "forearm_b": 93, "hand_b": 94}

CASES = [
    ("attack_whiff", 13), ("attack_whiff", 14), ("attack_whiff", 17),
    ("attack_light_1", 8), ("idle_combat", 55), ("hurt_crit", 4),
]

ZOOM = 2.6
CROP = (150, 160, 390, 400)


def rig_with(zmap, skel, layers):
    parts = {k: v.build() for k, v in build_goku_parts().items()}
    rows = [dict(r) for r in layers]
    for r in rows:
        if r["slot"] in zmap:
            r["z"] = zmap[r["slot"]]
    rig = ActorRig(skel, parts, rows, skel.data["secondary_chains"])
    rig.attachments.update({"face": "face_combat", "hair_front": "hair_front"})
    return rig


def main() -> None:
    skel = Skeleton.load(str(ROOT / "standards/skeleton_humanoid.json"))
    layers = load_layers(str(ROOT / "standards/layer_order.json"))

    rows = []
    for label, zmap in (("ANTES  z 60/61/62 (atras do tronco)", ANTES),
                        ("DEPOIS z 92/93/94 (acima do tronco)", DEPOIS)):
        rig = rig_with(zmap, skel, layers)
        tiles = []
        for name, frame in CASES:
            pose = pose_from_params(clips.get(name).sample(float(frame)), skel)
            im, _ = rig.render(pose, facing=1, zoom=ZOOM, out_size=(512, 512),
                               shadow=False)
            tiles.append((f"{name} f{frame}", im.convert("RGB").crop(CROP)))
        rows.append((label, tiles))

    w, h = rows[0][1][0][1].size
    sheet = Image.new("RGB", (w * len(CASES) + 10 * len(CASES), (h + 30) * 2),
                      (14, 14, 18))
    d = ImageDraw.Draw(sheet)
    for r, (label, tiles) in enumerate(rows):
        y = r * (h + 30) + 26
        d.text((6, y - 20), label, fill=(255, 215, 110) if r else (255, 150, 120))
        for i, (cap, im) in enumerate(tiles):
            x = i * (w + 10) + 5
            sheet.paste(im, (x, y))
            d.text((x + 3, y + h + 2), cap, fill=(170, 170, 180))
    out = ROOT / "experiments/occlusion/antes_depois.png"
    sheet.save(out)
    print(f"{out}  {sheet.size[0]}x{sheet.size[1]}")


if __name__ == "__main__":
    main()
