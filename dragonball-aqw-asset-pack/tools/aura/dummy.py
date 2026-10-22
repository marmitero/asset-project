"""Boneco de treino (straw dummy) usado nas cenas de combate V11–V15/V18."""
from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from aura.core import rgba
from aura.scene import GROUND_Y

# paleta do dummy
STRAW = "#C8A65A"
STRAW_D = "#9C7C3C"
STRAW_L = "#E3C888"
WOOD = "#7A5334"
WOOD_D = "#553A24"
ROPE = "#E8DCC0"


def draw_dummy(img: Image.Image, cx: float, gy: float, scale: float = 1.0,
               lean: float = 0.0, squash: float = 0.0, flash: float = 0.0,
               arms_up: float = 0.0) -> None:
    """Dummy de palha (y = altura acima do chão). `lean` em graus inclina p/ direita."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    S = scale
    lx = math.radians(lean)
    sq = 1.0 - 0.12 * squash

    def P(x: float, h: float) -> tuple[float, float]:
        """(x lateral, h altura acima do chao) -> pixel, com inclinacao na base."""
        X = x * math.cos(lx) + h * math.sin(lx)
        H = h * math.cos(lx) - x * math.sin(lx)
        return (cx + X * S, gy - H * S)

    def poly(pts, fill, outline_w=3.0):
        d.polygon([P(x + math.copysign(outline_w, x or 1) * 0.35, h + outline_w * 0.35)
                   for x, h in pts], fill=rgba("outline"))
        d.polygon([P(x, h) for x, h in pts], fill=rgba(fill))

    # sombra de contato
    d.ellipse([cx - 40 * S, gy - 8 * S, cx + 40 * S, gy + 8 * S], fill=(0, 0, 0, 82))

    # poste de madeira
    pole_h = 104 * sq
    p0, p1 = P(-3.5, 0), P(-3.5, pole_h)
    p2, p3 = P(3.5, pole_h), P(3.5, 0)
    d.polygon([p0, p1, p2, p3], fill=rgba(WOOD))
    d.line([p0, p1], fill=rgba("outline"), width=max(2, int(2 * S)))

    # base de madeira (elipse achatada, independente da inclinacao)
    by = gy - 3 * S
    d.ellipse([cx - 34 * S, by - 7 * S, cx + 34 * S, by + 7 * S], fill=rgba(WOOD_D),
              outline=rgba("outline"), width=max(2, int(2 * S)))

    # tronco de palha
    body_bot, body_top = 100 * sq, 132 * sq
    poly([(-33, body_bot), (33, body_bot), (38, body_top), (-38, body_top)], STRAW)

    # bandagens de corda
    for i in range(3):
        h = body_bot + (body_top - body_bot) * (0.18 + 0.28 * i)
        a = P(-35, h)
        b = P(0, h - 3.0)
        c = P(35, h + 1)
        d.line([a, b, c], fill=rgba(ROPE), width=max(2, int(3.6 * S)))
    # linha de costura lateral
    d.line([P(-26, body_top - 2), P(-9, body_bot + 4)], fill=rgba(STRAW_D),
           width=max(2, int(2 * S)))
    # palha saindo pelas laterais
    for side in (-1, 1):
        for k in range(3):
            h = body_bot + 6 + k * 8
            d.line([P(side * 33, h), P(side * (44 + 4 * k), h + 3 + k)], fill=rgba(STRAW_L),
                   width=max(2, int(2 * S)))

    # bracos de madeira
    arm_lift = 26 + arms_up * 34
    for side in (-1, 1):
        sh = P(side * 32, body_top - 10)
        ex = P(side * 62, body_top - 10 - math.sin(math.radians(arm_lift)) * 16)
        d.line([sh, ex], fill=rgba("outline"), width=max(4, int(7 * S)))
        d.line([sh, ex], fill=rgba(WOOD), width=max(2, int(3.4 * S)))
        r = max(3, int(5 * S))
        d.ellipse([ex[0] - r, ex[1] - r, ex[0] + r, ex[1] + r], fill=rgba(STRAW),
                  outline=rgba("outline"), width=max(2, int(1.6 * S)))

    # cabeca de saco
    hx, hy = P(0, body_top + 24)
    r = 25 * S
    d.ellipse([hx - r - 3, hy - r - 3, hx + r + 3, hy + r + 3], fill=rgba("outline"))
    d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=rgba(STRAW_L))
    d.line([(hx - r * 0.72, hy - r * 0.16), (hx + r * 0.72, hy - r * 0.16)],
           fill=rgba(STRAW_D), width=max(2, int(2 * S)))
    for dx in (-0.36, 0.36):
        d.ellipse([hx + dx * r - 2.4 * S, hy - r * 0.46 - 2.4 * S,
                   hx + dx * r + 2.4 * S, hy - r * 0.46 + 2.4 * S], fill=rgba(WOOD_D))
    d.line([(hx - 4 * S, hy + r * 0.34), (hx + 4 * S, hy + r * 0.34)],
           fill=rgba(WOOD_D), width=max(2, int(2 * S)))

    # flash de dano
    if flash > 0:
        # clarão curto (1–3 frames), não um banho de cor
        a = max(0, min(90, int(90 * (flash ** 2))))
        mask = np.array(layer.getchannel("A")).astype(np.float32) / 255.0
        mask = np.where(mask > 0.16, mask * (a / 255.0), 0.0)
        tint = Image.new("RGBA", layer.size, (255, 240, 222, 255))
        tint.putalpha(Image.fromarray((mask * 255).astype(np.uint8)))
        layer = Image.alpha_composite(layer, tint)
    img.alpha_composite(layer)


_FONT_CACHE: dict = {}


def _font(size: int):
    if size not in _FONT_CACHE:
        try:
            _FONT_CACHE[size] = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        except Exception:
            _FONT_CACHE[size] = ImageFont.load_default()
    return _FONT_CACHE[size]


def popup_text(img: Image.Image, text: str, x: float, y: float, progress: float,
               kind: str = "damage") -> None:
    """Número de dano / MISS / CRIT subindo e desvanecendo."""
    if progress <= 0 or progress >= 1:
        return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    size = 27 if kind == "crit" else 22
    if kind == "miss":
        size = 20
    font = _font(size)
    color = {"crit": (255, 196, 60), "miss": (176, 172, 158),
             "damage": (246, 238, 222)}.get(kind, (246, 238, 222))
    alpha = int(255 * (1 - progress ** 2.2))
    rise = -34 * (progress ** 0.65)
    scale = 1.0 + (0.45 * (1 - progress) ** 3 if kind == "crit" else 0.18 * (1 - progress) ** 2)
    f2 = _font(int(size * scale))
    tw = d.textlength(text, font=f2)
    px = max(8, min(img.width - tw - 8, x - tw / 2))
    py = y + rise
    # contorno
    for ox, oy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2)):
        d.text((px + ox, py + oy), text, font=f2, fill=(12, 10, 14, alpha))
    d.text((px, py), text, font=f2, fill=color + (int(alpha * 0.95),))
    img.alpha_composite(layer)
