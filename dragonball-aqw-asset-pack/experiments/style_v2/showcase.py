"""Comparativo v1 -> v2 na escala REAL de jogo (1x), sem ampliacao falsa.

O teste honesto de legibilidade: se nao le bem a 1x, nao presta.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from PIL import Image, ImageDraw  # noqa: E402

from aura import clips  # noqa: E402
from aura.render import ClipRenderer, ShowConfig, clip_to_gif_frames  # noqa: E402

OUT = Path(__file__).resolve().parent


def contact(rig, skel, name, bg, zoom=1.35, frames=(4, 10, 16)):
    r = ClipRenderer(rig, skel)
    cfg = ShowConfig(background=bg, zoom=zoom, caption="", show_hud=False,
                     show_fx=False, show_timeline=False)
    rc = clip_to_gif_frames(clips.get(name), r, cfg)
    out = []
    for i in frames:
        im = rc.frames[min(i, len(rc.frames) - 1)].convert("RGB")
        out.append(im.crop((150, 170, 370, 470)))
    return out


def band(rows, label, scale=1):
    w, h = rows[0][0].size
    W = w * len(rows[0]) + 10 * (len(rows[0]) + 1)
    H = h * len(rows) + 10 * (len(rows) + 1) + 24
    img = Image.new("RGB", (W * scale, H * scale), (18, 18, 22))
    d = ImageDraw.Draw(img)
    d.text((10, 6), label, fill=(255, 215, 110))
    for j, row in enumerate(rows):
        for i, im in enumerate(row):
            x = (10 + i * (w + 10)) * scale
            y = (24 + 10 + j * (h + 10)) * scale
            im2 = im.resize((w * scale, h * scale), Image.NEAREST) if scale > 1 else im
            img.paste(im2, (x, y))
    return img


if __name__ == "__main__":
    import importlib.util
    spec = importlib.util.spec_from_file_location("rigmod", ROOT / "tools" / "render_set.py")
    rs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rs)
    skel, rig, _ = rs.build_rig()

    specs = [("idle", "grid"), ("walk", "paozu"), ("attack_light_1", "dojo")]
    rows = [contact(rig, skel, n, b) for n, b in specs]
    b1 = band(rows, "ESCALA DE JOGO 1:1 (zoom 1.35) - idle / walk / attack", 1)
    b2 = band(rows, "MESMO FRAME AMPLIADO 3x (nearest, sem suavizar)", 3)
    b1.save(OUT / "v2_jogo_1x.png")
    b2.save(OUT / "v2_jogo_3x.png")
    print("wrote", OUT / "v2_jogo_1x.png", b1.size)
    print("wrote", OUT / "v2_jogo_3x.png", b2.size)
