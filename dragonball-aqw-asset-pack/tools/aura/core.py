"""Core de geometria, estilo e composição do pipeline AURA.

Coordenadas de autoria: x para a direita, y para baixo, 0 = chão.
O personagem tem 220 px de altura (cabeça em y=-220).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw

# ---------------------------------------------------------------- paleta
OUTLINE = "#0E0B12"

COLORS: dict[str, str] = {
    # Goku
    "skin": "#F6C9A0", "skin_sh": "#D79A72", "skin_hi": "#FFE1C4",
    "gi": "#F08A2E", "gi_sh": "#C25E16", "gi_hi": "#FFB65C",
    "blue": "#2F4FA8", "blue_sh": "#1B2F6B", "blue_hi": "#5B7AD6",
    "hair": "#17121C", "hair_sh": "#0B0810", "hair_hi": "#3A3244",
    "boot_sole": "#E8D9B8", "lace": "#C0392B",
    "eye_white": "#F7F2EA", "eye_dark": "#1A1A22", "mouth": "#7A3B32",
    "outline": OUTLINE,
    # cenário / UI
    "bg": "#14161C", "grid": "#2A2F3C", "ground": "#3A4150",
    "vfx_white": "#FFFFFF", "vfx_cyan": "#5CC8FF", "vfx_blue": "#1E78FF",
    "vfx_yellow": "#FFD84D", "vfx_orange": "#FF9A1E",
    "crit": "#FFB020", "dmg": "#F2E9D8", "miss": "#A9A28C",
    "hp": "#D7382F", "ki": "#2F80D8",
}


def rgba(key: str, alpha: int = 255) -> tuple[int, int, int, int]:
    h = COLORS.get(key, key).lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)


def shade(key: str, factor: float) -> str:
    h = COLORS.get(key, key).lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02X%02X%02X" % (
        max(0, min(255, int(r * factor))),
        max(0, min(255, int(g * factor))),
        max(0, min(255, int(b * factor))),
    )


# ---------------------------------------------------------------- splines
def catmull_rom(points, closed: bool = True, samples: int = 10):
    """Converte pontos de controle em polilinha suave (Catmull-Rom uniforme)."""
    pts = list(points)
    if len(pts) < 3:
        return pts
    if closed:
        p = [pts[-1]] + pts + [pts[0], pts[1]]
        n = len(pts)
    else:
        p = [pts[0]] + pts + [pts[-1]]
        n = len(pts) - 1
    out = []
    for i in range(n):
        p0, p1, p2, p3 = p[i], p[i + 1], p[i + 2], p[i + 3]
        for s in range(samples):
            t = s / samples
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t
                       + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t
                       + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    if not closed:
        out.append(pts[-1])
    return out


# ---------------------------------------------------------------- peças
@dataclass
class Part:
    name: str
    pivot: tuple[float, float]
    ops: list
    stroke: float = 3.0
    z: int = 0
    bone: str = ""
    scale: int = 4

    def build(self):
        return build_part(self)


@dataclass
class PartImage:
    name: str
    image: Image.Image          # RGBA @2x
    pivot: tuple[float, float]  # px na imagem @2x
    z: int
    bone: str
    scale: int = 4

    @property
    def size(self):
        return self.image.size


def _bbox(ops, pad: float):
    xs, ys = [], []
    for op in ops:
        if op[0] in ("fill", "fill_poly", "clip_fill", "clip_fill_poly", "shadow", "shadow_poly", "highlight",
                     "highlight_poly", "line", "clip_line"):
            for x, y in op[1]:
                xs.append(x)
                ys.append(y)
    if not xs:
        return (0, 0, 1, 1)
    return (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


def build_part(part: Part) -> PartImage:
    S = part.scale
    pad = part.stroke * 1.6 + 3
    x0, y0, x1, y1 = _bbox(part.ops, pad)
    w, h = max(1, int(math.ceil((x1 - x0) * S))), max(1, int(math.ceil((y1 - y0) * S)))
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    def tx(p):
        return ((p[0] - x0) * S, (p[1] - y0) * S)

    def poly(points):
        return [tx(p) for p in catmull_rom(points, closed=True)]

    def sharp(points):
        return [tx(p) for p in points]

    def shape(op):
        return sharp(op[1]) if op[0].endswith("_poly") else poly(op[1])

    # 1. fills base
    for op in part.ops:
        if op[0] in ("fill", "fill_poly"):
            draw.polygon(shape(op), fill=rgba(op[2]))
    base_alpha = img.getchannel("A")

    # 2. sombras e brilhos recortados pela silhueta
    for kind in ("shadow", "highlight"):
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for op in part.ops:
            if op[0] in (kind, kind + "_poly"):
                ld.polygon(shape(op), fill=rgba(op[2]))
        if layer.getbbox():
            layer.putalpha(ImageChops.multiply(layer.getchannel("A"), base_alpha))
            img = Image.alpha_composite(img, layer)
            draw = ImageDraw.Draw(img)

    # 1b. preenchimentos recortados pela silhueta (detalhes internos)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for op in part.ops:
        if op[0] in ("clip_fill", "clip_fill_poly"):
            ld.polygon(shape(op), fill=rgba(op[2]))
    if layer.getbbox():
        layer.putalpha(ImageChops.multiply(layer.getchannel("A"), base_alpha))
        img = Image.alpha_composite(img, layer)
        draw = ImageDraw.Draw(img)

    # 2b. sombra/brilho automáticos: silhueta deslocada, recortada pela base
    for op in part.ops:
        if op[0] not in ("auto_shadow", "auto_highlight"):
            continue
        _, color, dx, dy = op
        shifted = Image.new("L", (w, h), 0)
        dx_s, dy_s = int(dx * S), int(dy * S)
        src = base_alpha
        box = (max(0, dx_s), max(0, dy_s), min(w, w + dx_s), min(h, h + dy_s))
        crop = (max(0, -dx_s), max(0, -dy_s),
                min(w, w - dx_s), min(h, h - dy_s))
        if box[2] > box[0] and box[3] > box[1]:
            shifted.paste(src.crop(crop), box[:2])
        mask = ImageChops.multiply(shifted, base_alpha)
        layer = Image.new("RGBA", (w, h), rgba(color))
        layer.putalpha(mask)
        img = Image.alpha_composite(img, layer)
    draw = ImageDraw.Draw(img)

    # 3. linhas internas recortadas
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for op in part.ops:
        if op[0] == "line":
            pts = [tx(p) for p in catmull_rom(op[1], closed=False)]
            ld.line(pts, fill=rgba(op[2]), width=max(1, int(op[3] * S)), joint="curve")
        elif op[0] == "clip_line":
            pts = [tx(p) for p in catmull_rom(op[1], closed=False)]
            ld.line(pts, fill=rgba(op[2]), width=max(1, int(op[3] * S)), joint="curve")
    if layer.getbbox():
        if any(op[0] == "clip_line" for op in part.ops):
            layer.putalpha(ImageChops.multiply(layer.getchannel("A"), base_alpha))
        img = Image.alpha_composite(img, layer)

    # 4. contorno externo por dilatação
    alpha = np.array(img.getchannel("A"))
    radius = max(1, int(round(part.stroke * S / 2)))
    k = radius * 2 + 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    dilated = cv2.dilate(alpha, kernel, iterations=1)
    stroke_layer = Image.new("RGBA", (w, h), rgba("outline"))
    stroke_layer.putalpha(Image.fromarray(dilated))
    out = Image.alpha_composite(stroke_layer, img)
    if S != 2:
        out = out.resize((max(1, w // (S // 2)), max(1, h // (S // 2))), Image.LANCZOS)
    return PartImage(
        name=part.name,
        image=out,
        pivot=((part.pivot[0] - x0) * 2, (part.pivot[1] - y0) * 2),
        z=part.z,
        bone=part.bone,
    )


# ---------------------------------------------------------------- composição
def _warp_onto(canvas: Image.Image, part: PartImage, pivot_px, angle_deg, darken=1.0,
               scale: float = 1.0):
    """Coloca a peça (imagem 2x) no canvas (também 2x), rotacionada em torno do pivô.

    `scale` aplica zoom: 1.0 = tamanho autoral.
    """
    img = part.image
    if darken != 1.0:
        arr = np.array(img).astype(np.float32)
        arr[..., :3] *= darken
        img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    w, h = img.size
    a = math.radians(angle_deg)
    ca, sa = math.cos(a) * scale, math.sin(a) * scale
    px, py = part.pivot
    M = np.array([[ca, -sa, pivot_px[0] - (ca * px - sa * py)],
                  [sa, ca, pivot_px[1] - (sa * px + ca * py)]], np.float32)
    corners = np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float32)
    dst = (M @ np.hstack([corners, np.ones((4, 1), np.float32)]).T).T
    x0, y0 = np.floor(dst.min(0)).astype(int)
    x1, y1 = np.ceil(dst.max(0)).astype(int)
    x0, y0 = max(x0, 0), max(y0, 0)
    x1, y1 = min(x1, canvas.width), min(y1, canvas.height)
    if x1 <= x0 or y1 <= y0:
        return
    M2 = M.copy()
    M2[0, 2] -= x0
    M2[1, 2] -= y0
    warped = cv2.warpAffine(np.array(img), M2, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR,
                            borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    canvas.alpha_composite(Image.fromarray(warped), (int(x0), int(y0)))


def draw_ellipse(canvas: Image.Image, cx: float, cy: float, rx: float, ry: float,
                 color=(0, 0, 0, 90)):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color)
    canvas.alpha_composite(layer)
