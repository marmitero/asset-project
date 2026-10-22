"""Sonda de estilo: compara o render atual com uma variante 'paint pass v2'.

Nao toca no pipeline canonico (exports/). Gera apenas imagens de comparacao
em experiments/style_probe/out/.

Uso:  python3 experiments/style_probe/probe.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from PIL import Image, ImageDraw  # noqa: E402

from aura import core, scene  # noqa: E402
from aura import render as render_mod  # noqa: E402
from aura.anim import Clip  # noqa: E402
from aura import clips  # noqa: E402
from aura.parts_goku import build_goku_parts  # noqa: E402
from aura.pose import Skeleton  # noqa: E402
from aura.render import ClipRenderer, ShowConfig, clip_to_gif_frames  # noqa: E402
from aura.rig import ActorRig, load_layers  # noqa: E402

OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)

# ------------------------------------------------------------------ estilos
BASE_COLORS = dict(core.COLORS)

# paleta v2: sombra mais funda, highlight mais quente, outline quente
V2_COLORS = {
    "skin": "#F6C9A0", "skin_sh": "#C87F55", "skin_hi": "#FFE6CC",
    "gi": "#F2871F", "gi_sh": "#A9420D", "gi_hi": "#FFC46B",
    "blue": "#2C4CA8", "blue_sh": "#121F52", "blue_hi": "#7C9AE8",
    "hair": "#191320", "hair_sh": "#08060C", "hair_hi": "#4A3F58",
    "boot_sole": "#E8D9B8", "lace": "#B4302A",
    "eye_white": "#FFFBF2", "eye_dark": "#120F16", "mouth": "#6E2F28",
    "outline": "#1A0F18",
}

V2_BG = {
    "sky": (206, 214, 210),
    "sky2": (185, 196, 194),
    "horizon": (150, 164, 160),
    "floor": (196, 172, 132),
    "floor2": (178, 152, 112),
    "line": (120, 98, 70),
}


def stage(size=(512, 512)) -> Image.Image:
    """Palco claro estilo AQW: céu chapado + piso de terra + linha de contato."""
    w, h = size
    gy = int(scene.GROUND_Y * h / 512)
    img = Image.new("RGBA", size, V2_BG["sky"] + (255,))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, int(gy * 0.42)], fill=V2_BG["sky"] + (255,))
    d.rectangle([0, int(gy * 0.42), w, gy], fill=V2_BG["sky2"] + (255,))
    d.rectangle([0, gy - 3, w, gy], fill=V2_BG["horizon"] + (255,))
    d.rectangle([0, gy, w, h], fill=V2_BG["floor"] + (255,))
    for i in range(1, 5):
        y = gy + int((h - gy) * (i / 4) ** 1.7)
        d.line([(0, y), (w, y)], fill=V2_BG["floor2"] + (255,), width=2)
    d.line([(0, gy), (w, gy)], fill=V2_BG["line"] + (255,), width=2)
    return img


def build_rig():
    parts = {k: v.build() for k, v in build_goku_parts().items()}
    skel = Skeleton.load(ROOT / "standards" / "skeleton_humanoid.json")
    rig = ActorRig(skel, parts, load_layers(ROOT / "standards" / "layer_order.json"),
                   skel.data["secondary_chains"])
    return skel, rig


def apply_style(style: str):
    if style == "v2":
        core.COLORS.update(V2_COLORS)
        render_mod.make_background = lambda kind="grid", size=(512, 512): stage(size)
    else:
        core.COLORS.clear()
        core.COLORS.update(BASE_COLORS)
        render_mod.make_background = scene.make_background


# ------------------------------------------------------------------ captura
POSES = [
    ("idle", "V01", 40, "grid"),
    ("attack_whiff", "V11", 14, "dojo"),
    ("combo_light_3", "V09", 22, "dojo"),
]


def grab(style: str, zoom: float = 1.35):
    apply_style(style)
    skel, rig = build_rig()
    renderer = ClipRenderer(rig, skel)
    frames = []
    for name, vid, idx, bg in POSES:
        clip = clips.get(name)
        combat = name in ("attack_whiff",)
        cfg = ShowConfig(background=bg, zoom=zoom, caption="", show_hud=False,
                         dummy=combat, dummy_x=0.755, dummy_scale=0.95, feedback=combat)
        rc = clip_to_gif_frames(clip, renderer, cfg)
        frames.append(rc.frames[min(idx, len(rc.frames) - 1)].convert("RGB"))
    return frames


def sheet(pairs, cell=(300, 300), labels=("atual", "v2")) -> Image.Image:
    cols, rows = 2, len(pairs)
    gap, top = 10, 30
    W = cols * cell[0] + gap * 3
    H = rows * cell[1] + gap * (rows + 1) + top
    out = Image.new("RGB", (W, H), (24, 24, 28))
    d = ImageDraw.Draw(out)
    for r, (a, b) in enumerate(pairs):
        for c, im in enumerate((a, b)):
            x = gap + c * (cell[0] + gap)
            y = top + gap + r * (cell[1] + gap)
            out.paste(im.resize(cell, Image.LANCZOS), (x, y))
            d.rectangle([x, y, x + cell[0], y + cell[1]], outline=(70, 70, 78))
        d.text((gap, top + gap + r * (cell[1] + gap) - 16), POSES[r][0], fill=(200, 200, 210))
    d.text((gap + cell[0] + gap, 8), labels[1], fill=(255, 220, 120))
    d.text((gap, 8), labels[0], fill=(160, 160, 170))
    return out


if __name__ == "__main__":
    old = grab("v1")
    new = grab("v2")
    sh = sheet(list(zip(old, new)))
    sh.save(OUT / "compare_style.png")
    print("wrote", OUT / "compare_style.png", sh.size)
