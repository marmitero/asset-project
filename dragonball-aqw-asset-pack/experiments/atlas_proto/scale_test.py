"""Comparativo final: mesmo frame, mesmo enquadramento, dois rigs.

Responde a pergunta que decide a rota: em qual RESOLUCAO cada abordagem ganha?
"""
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


def shot(rig, clip_name: str, frame: int, scale: int = 512, zoom: float = 1.35):
    r = ClipRenderer(rig, rig.skel)
    cfg = ShowConfig(background="void", zoom=zoom, caption="", show_hud=False,
                     show_fx=False, show_timeline=False)
    rc = clip_to_gif_frames(clips.get(clip_name), r, cfg)
    im = rc.frames[min(frame, len(rc.frames) - 1)].convert("RGB")
    b = im.getbbox() or (0, 0, scale, scale)
    # recorta janela centrada no personagem COM folga para os pes
    cx = (b[0] + b[2]) // 2
    cy = (b[1] + b[3]) // 2
    hw = max(b[2] - b[0], int(scale * 0.30)) * 0.85
    hh = max(b[3] - b[1], int(scale * 0.30)) * 0.80
    return im.crop((int(max(0, cx - hw)), int(max(0, cy - hh)),
                    int(min(im.width, cx + hw)), int(min(im.height, cy + hh))))


def band(label: str, vec: Image.Image, ai: Image.Image, target_h: int) -> Image.Image:
    def fit(im):
        s = target_h / im.height
        return im.resize((int(im.width * s), target_h), Image.LANCZOS)
    v, a = fit(vec), fit(ai)
    gap, hdr = 12, 26
    out = Image.new("RGB", (v.width + a.width + gap * 3, target_h + gap * 2 + hdr), (18, 18, 22))
    out.paste(v, (gap, hdr + gap))
    out.paste(a, (gap * 2 + v.width, hdr + gap))
    d = ImageDraw.Draw(out)
    d.text((gap, 8), f"{label}  |  ESQUERDA: vetor   DIREITA: IA", fill=(230, 230, 235))
    d.line([(gap * 2 + v.width - gap // 2, 0), (gap * 2 + v.width - gap // 2, out.height)],
           fill=(255, 190, 70), width=2)
    return out


if __name__ == "__main__":
    skel_v, rig_v, _ = build_rig()
    skel_a, rig_a = build_painted_rig(OUT / "ai_painted.jpg")

    # resolucao de jogo (o canvas e 512 e o GIF mostra 1:1)
    v_small = shot(rig_v, "idle", 50, 512, 1.35)
    a_small = shot(rig_a, "idle", 50, 512, 1.35)
    b1 = band("A) ESCALA DE JOGO (~230 px de personagem)", v_small, a_small, 420)

    # resolucao alta (zoom 3 = personagem ~660 px)
    v_big = shot(rig_v, "idle", 50, 1024, 3.0)
    a_big = shot(rig_a, "idle", 50, 1024, 3.0)
    b2 = band("B) ALTA RESOLUCAO (~660 px)", v_big, a_big, 420)

    W = max(b1.width, b2.width)
    out = Image.new("RGB", (W, b1.height + b2.height + 10), (18, 18, 22))
    out.paste(b1, (0, 0))
    out.paste(b2, (0, b1.height + 10))
    out.save(OUT / "resolucao_comparativo.png")
    print("wrote", OUT / "resolucao_comparativo.png", out.size)
