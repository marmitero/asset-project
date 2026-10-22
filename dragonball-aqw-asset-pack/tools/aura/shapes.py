"""Formas reutilizáveis para as peças (coordenadas autorais, y para baixo)."""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aura.core import Part  # noqa: E402


def norm(x, y):
    d = math.hypot(x, y) or 1.0
    return (x / d, y / d)


def capsule(p0, p1, w0, w1, bulge: float = 0.0, samples: int = 6):
    """Polígono de membro afunilado com pontas arredondadas."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    pts = []
    wm = (w0 + w1) * 0.5 * (1 + bulge)
    for i in range(samples + 1):
        t = i / samples
        w = (w0 * (1 - t) + w1 * t) * 0.5
        if 0.25 < t < 0.75:
            w = wm * 0.5
        pts.append((p0[0] + dx * t + nx * w, p0[1] + dy * t + ny * w))
    # ponta arredondada
    for k in range(3):
        a = math.radians(90 * k / 3)
        pts.append((p1[0] + nx * (w1 * 0.5) * math.cos(a) + (dx / L) * (w1 * 0.5) * math.sin(a),
                    p1[1] + ny * (w1 * 0.5) * math.cos(a) + (dy / L) * (w1 * 0.5) * math.sin(a)))
    for i in range(samples, -1, -1):
        t = i / samples
        w = (w0 * (1 - t) + w1 * t) * 0.5
        if 0.25 < t < 0.75:
            w = wm * 0.5
        pts.append((p0[0] + dx * t - nx * w, p0[1] + dy * t - ny * w))
    return pts


def oval(cx, cy, rx, ry, n=10):
    return [(cx + rx * math.cos(2 * math.pi * i / n),
             cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


def box(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


F = lambda pts, color: ("fill", pts, color)              # noqa: E731
P = lambda pts, color: ("fill_poly", pts, color)              # noqa: E731
SH = lambda pts, color: ("shadow", pts, color)
SHP = lambda pts, color: ("shadow_poly", pts, color)
HIP = lambda pts, color: ("highlight_poly", pts, color)           # noqa: E731
HI = lambda pts, color: ("highlight", pts, color)        # noqa: E731
CF = lambda pts, color: ("clip_fill", pts, color)          # noqa: E731
CFP = lambda pts, color: ("clip_fill_poly", pts, color)    # noqa: E731
AS = lambda color, dx=3.0, dy=4.0: ("auto_shadow", color, dx, dy)      # noqa: E731
AH = lambda color, dx=-2.5, dy=-3.0: ("auto_highlight", color, dx, dy)  # noqa: E731
L = lambda pts, color, w=1.8: ("line", pts, color, w)    # noqa: E731
CL = lambda pts, color, w=1.4: ("clip_line", pts, color, w)  # noqa: E731


def part(name, pivot, ops, bone="", z=0, stroke=3.0):
    return Part(name=name, pivot=pivot, ops=ops, bone=bone, z=z, stroke=stroke)


def limb(cfg, side_is_front: bool):
    """Config de membro -> ops com sombra e brilho coerentes (luz de cima/frente)."""
    p0, p1 = cfg["p0"], cfg["p1"]
    w0, w1 = cfg["w0"], cfg["w1"]
    base, sh, hi = cfg["base"], cfg["sh"], cfg["hi"]
    body = capsule(p0, p1, w0, w1, cfg.get("bulge", 0.0))
    # sombra no lado de baixo/trás
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    sgn = 1 if (nx > 0 or (nx == 0 and ny > 0)) else -1
    ops = [F(body, base)]
    ops.append(SH(capsule_offset(p0, p1, w0 * 0.62, w1 * 0.62, sgn), sh))
    if cfg.get("highlight", True):
        ops.append(HI(capsule_offset(p0, p1, w0 * 0.26, w1 * 0.26, -sgn,
                                    shift=-w0 * 0.18), hi))
    for ln in cfg.get("lines", []):
        ops.append(CL(ln, cfg.get("line_color", sh), cfg.get("line_w", 1.3)))
    return ops


def capsule_offset(p0, p1, w0, w1, sgn, shift=0.0):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    off = w0 * 0.30 * sgn + shift
    a = (p0[0] + nx * off, p0[1] + ny * off)
    b = (p1[0] + nx * (off * w1 / max(w0, 0.01)), p1[1] + ny * (off * w1 / max(w0, 0.01)))
    return capsule(a, b, w0, w1)
