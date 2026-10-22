"""Gera o GIF de comparacao em movimento, ampliado, para revisao humana."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image, ImageDraw  # noqa: E402

from aura import clips  # noqa: E402
from aura.render import ClipRenderer, ShowConfig, clip_to_gif_frames  # noqa: E402
from cut_atlas import OUT, build_painted_rig, build_rig  # noqa: E402


def frames_of(rig, name, zoom=2.6, n=20):
    r = ClipRenderer(rig, rig.skel)
    cfg = ShowConfig(background="void", zoom=zoom, caption="", show_hud=False,
                     show_fx=False, show_timeline=False)
    rc = clip_to_gif_frames(clips.get(name), r, cfg)
    out = []
    for im in rc.frames[:n]:
        im = im.convert("RGB")
        b = im.getbbox() or (0, 0, 512, 512)
        cx, cy = (b[0] + b[2]) // 2, (b[1] + b[3]) // 2
        hw = max(int((b[2] - b[0]) * 0.62), 130)
        hh = max(int((b[3] - b[1]) * 0.60), 150)
        out.append(im.crop((max(0, cx - hw), max(0, cy - hh),
                            min(512, cx + hw), min(512, cy + hh))))
    return out


def make(name: str, label: str) -> Path:
    va = frames_of(build_rig()[1], name)
    a = frames_of(build_painted_rig(OUT / "ai_painted.jpg")[1], name)
    h = max(f.height for f in va + a)
    w = max(f.width for f in va + a)
    frames = []
    for i in range(min(len(va), len(a))):
        f = Image.new("RGB", (w * 2 + 10, h + 22), (14, 14, 18))
        f.paste(va[i].resize((w, h), Image.LANCZOS), (0, 22))
        f.paste(a[i].resize((w, h), Image.LANCZOS), (w + 10, 22))
        d = ImageDraw.Draw(f)
        d.text((4, 5), "VETOR (atual)", fill=(150, 150, 160))
        d.text((w + 14, 5), "IA (atlas)", fill=(255, 205, 90))
        d.line([(w + 5, 0), (w + 5, h + 22)], fill=(255, 190, 70), width=2)
        frames.append(f)
    path = OUT / f"movimento_{name}.gif"
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=45,
                   loop=0, optimize=True, disposal=1)
    print(f"wrote {path}  {len(frames)}f  {path.stat().st_size // 1024} KB  {frames[0].size}")
    return path


if __name__ == "__main__":
    make("walk", "caminhada")
    make("attack_light_1", "ataque")
