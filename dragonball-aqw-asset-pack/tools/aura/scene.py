"""Composição de cena: fundo, chão, ator, FX e HUD de validação."""
from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFilter

from aura.core import COLORS, rgba
from aura.easing import ease

W, H = 512, 512
GROUND_Y = 448
FLOOR = 96          # altura do piso projetado


def _bg_palette(kind: str):
    return {
        "dojo": ((26, 28, 38), (44, 48, 62), (58, 50, 44)),
        "paozu": ((38, 52, 44), (74, 96, 66), (120, 92, 58)),
        "void": ((18, 18, 24), (30, 30, 40), (40, 40, 52)),
        "grid": ((16, 18, 24), (28, 32, 42), (34, 38, 50)),
    }.get(kind, ((26, 28, 38), (44, 48, 62), (58, 50, 44)))


def make_background(kind: str = "grid", size=(W, H)) -> Image.Image:
    """Fundo flat em bandas (paleta fechada) — estilo AQW e leve para GIF."""
    w, h = size
    sky, ground, accent = _bg_palette(kind)
    gy = int(GROUND_Y * h / 512)
    img = Image.new("RGBA", size, sky + (255,))
    d = ImageDraw.Draw(img)
    # 3 bandas chapadas de céu/ambiente (sem degradê por pixel)
    for i, k in enumerate((0.0, 0.30, 0.62)):
        c = tuple(int(sky[j] + (ground[j] - sky[j]) * k * 0.55) for j in range(3))
        d.rectangle([0, int(gy * (i / 3)), w, int(gy * ((i + 1) / 3))], fill=c + (255,))
    if kind == "paozu":
        # colinas chapadas no horizonte (atras do piso)
        d.ellipse([-w * 0.15, gy - 130, w * 0.55, gy + 20], fill=(sky[0] + 16, sky[1] + 26, sky[2] + 14, 255))
        d.ellipse([w * 0.45, gy - 100, w * 1.2, gy + 20], fill=(sky[0] + 9, sky[1] + 16, sky[2] + 9, 255))
    # piso
    floor_c = (ground[0] - 10, ground[1] - 10, ground[2] - 8)
    d.rectangle([0, gy, w, h], fill=floor_c + (255,))
    # faixas do piso (perspectiva)
    for i in range(1, 4):
        y = gy + FLOOR * (i / 4) ** 1.6
        d.line([(0, y), (w, y)], fill=(floor_c[0] + 10, floor_c[1] + 10, floor_c[2] + 9, 255), width=2)
    # linha de contato do piso
    d.line([(0, gy), (w, gy)], fill=(accent[0] + 30, accent[1] + 30, accent[2] + 20, 255), width=2)
    if kind in ("grid", "void"):
        for i in range(1, 8):
            x = int(i * w / 8)
            d.line([(x, 0), (x, gy)], fill=(sky[0] + 6, sky[1] + 7, sky[2] + 9, 255), width=1)
    if kind == "dojo":
        # painéis de parede e vigas
        for i in range(1, 4):
            x = int(i * w / 4)
            d.line([(x, 0), (x, gy)], fill=(sky[0] + 8, sky[1] + 8, sky[2] + 10, 255), width=3)
        d.line([(0, gy - 96), (w, gy - 96)], fill=(sky[0] + 10, sky[1] + 10, sky[2] + 12, 255), width=4)
    return img


def vignette(img: Image.Image, strength: float = 0.55) -> Image.Image:
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-w * 0.25, -h * 0.35, w * 1.25, h * 1.15], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(w / 14))
    dark = Image.new("RGBA", (w, h), (0, 0, 0, int(255 * strength)))
    return Image.composite(img, Image.alpha_composite(img, dark), mask)


# ------------------------------------------------------------------ FX
def fx_slash(size=(512, 512), progress: float = 0.0, kind: str = "light",
             origin=(0.72, 0.52), facing: int = 1):
    """Crescente de corte: arco fino que abre e desvanece."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    if progress <= 0 or progress >= 1:
        return img
    d = ImageDraw.Draw(img)
    cx, cy = size[0] * origin[0], size[1] * origin[1]
    p = ease(progress, "out")
    alpha = int(240 * (1 - progress) ** 1.3)
    r = 34 + 46 * p
    wdt = max(1, int(11 * (1 - progress) ** 0.7))
    a0 = (-62 + 34 * p) * facing
    a1 = (58 + 46 * p) * facing
    d.arc([cx - r, cy - r, cx + r, cy + r],
          min(a0, a1) - 90, max(a0, a1) - 90,
          fill=(255, 255, 255, alpha), width=wdt)
    # segunda lâmina, mais curta e deslocada
    r2 = r * 0.78
    d.arc([cx - r2, cy - r2, cx + r2, cy + r2],
          min(a0, a1) - 90 + 6, max(a0, a1) - 90 - 6,
          fill=(170, 225, 255, int(alpha * 0.55)), width=max(1, wdt // 2))
    return img.filter(ImageFilter.GaussianBlur(1.4))


def motion_trail(size, points, color=(255, 245, 220), width=9, alpha=150):
    """Rastro do punho: faixa afunilada ligando posições recentes."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    if len(points) < 2:
        return img
    d = ImageDraw.Draw(img)
    n = len(points)
    for i in range(n - 1):
        t = i / max(1, n - 2)
        w = max(1, int(width * (0.25 + 0.75 * t)))
        a = int(alpha * (0.15 + 0.85 * t))
        d.line([points[i], points[i + 1]], fill=color + (a,), width=w)
        d.ellipse([points[i][0] - w / 2, points[i][1] - w / 2,
                   points[i][0] + w / 2, points[i][1] + w / 2], fill=color + (a,))
    return img.filter(ImageFilter.GaussianBlur(2.0))


def fx_impact(size=(512, 512), progress: float = 0.0, level: str = "light"):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    if progress <= 0 or progress >= 1:
        return img
    d = ImageDraw.Draw(img)
    cx, cy = size[0] * 0.62, size[1] * 0.52
    p = ease(progress, "out")
    alpha = int(255 * (1 - progress) ** 1.6)
    r = (18 + 70 * p) * (1.6 if level == "crit" else 1.0)
    d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55],
              fill=(255, 255, 255, alpha))
    if level in ("heavy", "crit"):
        n = 9 if level == "crit" else 6
        for i in range(n):
            a = 2 * math.pi * i / n + p * 0.6
            r0, r1 = r * 0.7, r * (2.1 + 0.5 * (i % 2))
            d.line([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)),
                    (cx + r1 * math.cos(a), cy + r1 * math.sin(a))],
                   fill=(255, 220, 120, alpha), width=max(1, int(5 * (1 - progress))))
    img = img.filter(ImageFilter.GaussianBlur(2))
    return img


def fx_impact_at(size, center, progress: float = 0.0, level: str = "light"):
    """Impacto centrado no ponto de contato (não na mão do atacante)."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    if progress <= 0 or progress >= 1:
        return img
    d = ImageDraw.Draw(img)
    cx, cy = center
    p = ease(progress, "out")
    alpha = int(255 * (1 - progress) ** 1.5)
    r = (10 + 34 * p) * (1.5 if level == "crit" else 1.0)
    d.ellipse([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5],
              fill=(255, 255, 255, alpha))
    if level in ("heavy", "crit"):
        n = 10 if level == "crit" else 6
        for i in range(n):
            a = 2 * math.pi * i / n + p * 0.5 + 0.3
            r0, r1 = r * 0.55, r * (1.7 + 0.6 * (i % 2))
            d.line([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)),
                    (cx + r1 * math.cos(a), cy + r1 * math.sin(a))],
                   fill=(255, 226, 140, alpha), width=max(1, int(4 * (1 - progress))))
    return img.filter(ImageFilter.GaussianBlur(1.6))


def fx_charge(size=(512, 512), progress: float = 0.0):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    if progress <= 0 or progress >= 1:
        return img
    d = ImageDraw.Draw(img)
    cx, cy = size[0] * 0.36, size[1] * 0.58
    p = ease(progress, "out")
    alpha = int(220 * min(1.0, progress * 2) * (1 - progress) ** 0.8)
    r = 40 + 26 * p
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 230, 255, alpha))
    img = img.filter(ImageFilter.GaussianBlur(6))
    return img


def dust_puff(size=(512, 512), progress: float = 0.0, y: float = GROUND_Y):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    if progress <= 0 or progress >= 1:
        return img
    d = ImageDraw.Draw(img)
    p = ease(progress, "out")
    alpha = int(150 * (1 - progress) ** 2)
    for i in range(5):
        dx = (i - 2) * (14 + 26 * p)
        r = 8 + 16 * p * (0.6 + 0.4 * (i % 2))
        d.ellipse([size[0] / 2 + dx - r, y - r * 0.7, size[0] / 2 + dx + r, y + r * 0.55],
                  fill=(210, 200, 175, alpha))
    img = img.filter(ImageFilter.GaussianBlur(4))
    return img


def screen_shake(img: Image.Image, amt: float) -> Image.Image:
    if abs(amt) < 0.5:
        return img
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.alpha_composite(img, (int(amt * 0.7), int(-abs(amt) * 0.45)))
    return out


# ------------------------------------------------------------------ HUD
def hud_label(img: Image.Image, title: str, right: str = "", sub: str = "") -> None:
    from PIL import ImageFont
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font = small = ImageFont.load_default()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width, 28], fill=(10, 11, 16, 225))
    d.line([(0, 28), (img.width, 28)], fill=(60, 68, 86, 255), width=1)
    if right:
        rw = d.textlength(right, font=small)
        d.text((img.width - rw - 10, 8), right, fill=(150, 200, 255, 255), font=small)
        limit = img.width - rw - 26
    else:
        limit = img.width - 12
    # trunca o titulo para nunca sobrepor o contador
    text = title
    while d.textlength(text, font=font) > limit and len(text) > 4:
        text = text[:-1]
    if text != title:
        text = text[:-1] + "…"
    d.text((10, 6), text, fill=(236, 240, 248, 255), font=font)
    if sub:
        d.rectangle([0, img.height - 24, img.width, img.height], fill=(10, 11, 16, 210))
        sw = d.textlength(sub, font=small)
        d.text(((img.width - sw) / 2, img.height - 18), sub, fill=(168, 178, 198, 255),
               font=small)


def timeline_strip(img: Image.Image, frame: int, total: int, marks=()) -> None:
    d = ImageDraw.Draw(img)
    h = img.height
    x0, x1 = 10, img.width - 10
    y = h - 10
    d.line([(x0, y), (x1, y)], fill=(70, 78, 96, 255), width=2)
    for m in marks:
        xm = x0 + (x1 - x0) * m / max(1, total - 1)
        d.line([(xm, y - 4), (xm, y + 4)], fill=(255, 200, 90, 255), width=2)
    xf = x0 + (x1 - x0) * min(frame, total - 1) / max(1, total - 1)
    d.ellipse([xf - 4, y - 4, xf + 4, y + 4], fill=(255, 240, 200, 255))
