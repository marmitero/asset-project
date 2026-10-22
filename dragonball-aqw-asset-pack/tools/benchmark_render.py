#!/usr/bin/env python3
"""
AURA — benchmark do pipeline de render.

Compara o custo de transformar/compor N pecas em um canvas 512^2.
Cena sintetica; nao grava arquivos.

Uso:
    python3 tools/benchmark_render.py --parts 24 --frames 120
"""
from __future__ import annotations

import argparse
import time

import numpy as np
from PIL import Image, ImageDraw

try:
    import cv2
except ImportError:  # pragma: no cover
    cv2 = None


def make_parts(count: int, supersample: int) -> list[np.ndarray]:
    scale = supersample
    parts = []
    for i in range(count):
        w, h = 200 * scale, 300 * scale
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle(
            [8 * scale, 8 * scale, w - 8 * scale, h - 8 * scale],
            radius=22 * scale,
            fill=(240, 138, 46, 255),
            outline=(14, 11, 18, 255),
            width=3 * scale,
        )
        draw.ellipse(
            [30 * scale, h - 70 * scale, w - 30 * scale, h - 24 * scale],
            fill=(194, 94, 22, 255),
        )
        parts.append(np.array(img))
    return parts


def frame_cv2(parts, canvas_px: int, t: float) -> Image.Image:
    canvas = Image.new("RGBA", (canvas_px, canvas_px), (0, 0, 0, 0))
    for j, src in enumerate(parts):
        h, w = src.shape[:2]
        angle = 7.0 * (j % 5) * (0.5 - t)
        matrix = cv2.getRotationMatrix2D((w / 2, h / 2), -angle, 1.0)
        matrix[0, 2] += canvas_px / 2 - w / 2 + 30 * (j % 3 - 1)
        matrix[1, 2] += canvas_px / 2 - h / 2 + 20 * (j % 4 - 2)
        corners = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32)
        dst = (matrix @ np.hstack([corners, np.ones((4, 1), np.float32)]).T).T
        x0, y0 = np.floor(dst.min(axis=0)).astype(int)
        x1, y1 = np.ceil(dst.max(axis=0)).astype(int)
        x0, y0 = max(x0, 0), max(y0, 0)
        x1, y1 = min(x1, canvas_px), min(y1, canvas_px)
        if x1 <= x0 or y1 <= y0:
            continue
        local = matrix.copy()
        local[0, 2] -= x0
        local[1, 2] -= y0
        warped = cv2.warpAffine(
            src, local, (x1 - x0, y1 - y0),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0, 0),
        )
        canvas.alpha_composite(Image.fromarray(warped), (int(x0), int(y0)))
    rgba = np.array(canvas)
    bgra = cv2.cvtColor(rgba, cv2.COLOR_RGBA2BGRA)
    small = cv2.resize(bgra, (canvas_px // 2, canvas_px // 2), interpolation=cv2.INTER_AREA)
    return Image.fromarray(cv2.cvtColor(small, cv2.COLOR_BGRA2RGBA))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--parts", type=int, default=24)
    ap.add_argument("--frames", type=int, default=120)
    ap.add_argument("--supersample", type=int, default=2)
    args = ap.parse_args()

    if cv2 is None:
        print("OpenCV ausente. Instale opencv-python-headless.")
        return 2

    canvas_px = 512 * args.supersample
    parts = make_parts(args.parts, args.supersample)

    frame_cv2(parts, canvas_px, 0.0)  # warmup
    start = time.perf_counter()
    for i in range(args.frames):
        frame_cv2(parts, canvas_px, i / args.frames)
    elapsed = time.perf_counter() - start
    per_frame = elapsed / args.frames * 1000

    print("AURA render benchmark")
    print(f"  pecas: {args.parts} | canvas: 512x512 | supersample: {args.supersample}x")
    print(f"  frames: {args.frames} | tempo: {elapsed:.2f}s")
    print(f"  {per_frame:.1f} ms/frame  ({1000/per_frame:.1f} fps single-core)")
    print(f"  clipe de 96 frames: {per_frame*96/1000:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
