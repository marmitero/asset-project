"""Teste decisivo: o rig PINTADO por IA anima tao bem quanto o vetorial?

Renderiza o mesmo clipe com os dois rigs e monta comparacao lado a lado.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from aura import clips  # noqa: E402
from aura.render import ClipRenderer, ShowConfig, clip_to_gif_frames  # noqa: E402
from aura.rig import load_layers  # noqa: E402
from aura.pose import Pose  # noqa: E402
from cut_atlas import FRAME, OUT, build_painted_rig, build_rig  # noqa: E402


def vector_rig():
    return build_rig()[1]


def render_pair(clip_name: str, limit: int = 24):
    clip = clips.get(clip_name)
    outs = []
    for rig in (vector_rig(), build_painted_rig(OUT / "ai_painted.jpg")[1]):
        r = ClipRenderer(rig, rig.skel)
        cfg = ShowConfig(background="paozu", zoom=1.5, caption="", show_hud=False,
                         show_fx=False, show_timeline=False)
        rc = clip_to_gif_frames(clip, r, cfg)
        outs.append(rc.frames[:limit])
    return outs


def side_by_side(a: list[Image.Image], b: list[Image.Image]) -> list[Image.Image]:
    frames = []
    for fa, fb in zip(a, b):
        W, H = fa.size
        out = Image.new("RGB", (W * 2 + 6, H), (16, 16, 20))
        out.paste(fa.convert("RGB"), (0, 0))
        out.paste(fb.convert("RGB"), (W + 6, 0))
        frames.append(out)
    return frames


if __name__ == "__main__":
    for name in ("walk", "attack_light_1"):
        a, b = render_pair(name, limit=20)
        frames = side_by_side(a, b)
        # reduz para caber confortavelmente e mantem o GIF leve
        frames = [f.resize((f.width // 2, f.height // 2), Image.LANCZOS) for f in frames]
        path = OUT / f"compare_{name}.gif"
        frames[0].save(path, save_all=True, append_images=frames[1:], duration=40,
                       loop=0, optimize=True, disposal=1)
        print("wrote", path, len(frames), "frames", path.stat().st_size // 1024, "KB")
