"""Registro por perfil de largura (DTW por linha).

A escala anisotropica global alinha a CAIXA da silhueta, nao as JUNTAS. Resultado:
a mascara do braco cai sobre o tronco da arte gerada. Aqui cada linha do rig e
mapeada para a linha correspondente da arte (DTW sobre o perfil de largura) e,
dentro da linha, a arte e esticada para o intervalo x do rig.

Isso alinha ombro, cintura, quadril e tornozelo sem precisar de deteccao de junta.
"""
from __future__ import annotations

import cv2
import numpy as np


def _width_profile(mask: np.ndarray):
    """Para cada linha: (xmin, xmax) ou (-1,-1) se vazia."""
    h = mask.shape[0]
    xs0 = np.full(h, -1, np.int32)
    xs1 = np.full(h, -1, np.int32)
    for y in range(h):
        row = np.where(mask[y] > 0)[0]
        if len(row):
            xs0[y], xs1[y] = row[0], row[-1]
    return xs0, xs1


def _dtw_path(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """DTW 1D entre perfis de largura normalizados; devolve mapa i->j."""
    a = a.astype(np.float64)
    b = b.astype(np.float64)
    a = (a - a.mean()) / (a.std() + 1e-6)
    b = (b - b.mean()) / (b.std() + 1e-6)
    n, m = len(a), len(b)
    D = np.full((n, m), np.inf)
    D[0, 0] = abs(a[0] - b[0])
    for i in range(1, n):
        D[i, 0] = D[i - 1, 0] + abs(a[i] - b[0])
    for j in range(1, m):
        D[0, j] = D[0, j - 1] + abs(a[0] - b[j])
    for i in range(1, n):
        for j in range(1, m):
            D[i, j] = abs(a[i] - b[j]) + min(D[i - 1, j], D[i, j - 1], D[i - 1, j - 1])
    i, j = n - 1, m - 1
    path = [(i, j)]
    while i > 0 or j > 0:
        opts = []
        if i > 0 and j > 0:
            opts.append((D[i - 1, j - 1], i - 1, j - 1))
        if i > 0:
            opts.append((D[i - 1, j], i - 1, j))
        if j > 0:
            opts.append((D[i, j - 1], i, j - 1))
        _, i, j = min(opts, key=lambda t: t[0])
        path.append((i, j))
    path.reverse()
    mapping = np.zeros(n, np.float64)
    for i, j in path:
        mapping[i] = j
    # preenche linhas que o caminho pulou e suaviza
    last = 0.0
    for i in range(n):
        if mapping[i] == 0 and i > 0:
            mapping[i] = last
        last = mapping[i]
    k = 9
    pad = np.pad(mapping, (k, k), mode="edge")
    mapping = np.convolve(pad, np.ones(2 * k + 1) / (2 * k + 1), mode="valid")
    return mapping


def landmark_register(art_rgb: np.ndarray, art_a: np.ndarray,
                      rig_mask: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """Reamostra a arte no enquadramento do rig por alinhamento de perfil."""
    H, W = rig_mask.shape
    art_m = (art_a > 0.35).astype(np.uint8)
    rig_m = (rig_mask > 20).astype(np.uint8)
    ax0, ax1 = _width_profile(art_m)
    rx0, rx1 = _width_profile(rig_m)
    arows = np.where(ax1 >= 0)[0]
    rrows = np.where(rx1 >= 0)[0]
    if not len(arows) or not len(rrows):
        raise ValueError("silhueta vazia")
    ay0, ay1 = arows[0], arows[-1]
    ry0, ry1 = rrows[0], rrows[-1]

    aw = (ax1 - ax0)[ay0:ay1 + 1].astype(np.float64)
    rw = (rx1 - rx0)[ry0:ry1 + 1].astype(np.float64)
    jmap = _dtw_path(rw, aw)                      # linha do rig -> linha da arte
    art_row = np.clip(ay0 + jmap, ay0, ay1)       # em coords da arte

    # mapa de reamostragem
    map_x = np.zeros((H, W), np.float32)
    map_y = np.zeros((H, W), np.float32)
    for y in range(H):
        if y < ry0 or y > ry1:
            map_y[y] = -1
            map_x[y] = -1
            continue
        src_y = int(round(art_row[y - ry0]))
        src_y = min(max(src_y, 0), H - 1)
        map_y[y] = src_y
        a0, a1 = ax0[src_y], ax1[src_y]
        r0, r1 = rx0[y], rx1[y]
        span_a = max(a1 - a0, 1)
        span_r = max(r1 - r0, 1)
        xs = np.arange(W, dtype=np.float32)
        map_x[y] = a0 + (xs - r0) * span_a / span_r

    # reamostra em premultiplied para nao puxar cor do fundo
    prem = art_rgb.astype(np.float32) * art_a[..., None]
    warped_rgb = cv2.remap(prem, map_x, map_y, cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    warped_a = cv2.remap((art_a * 255).astype(np.float32), map_x, map_y,
                         cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    warped_a = np.clip(warped_a / 255.0, 0, 1)
    safe = np.maximum(warped_a, 1e-5)[..., None]
    out_rgb = np.clip(warped_rgb / safe, 0, 255)
    coverage = float(((warped_a > 0.5) & (rig_m > 0)).sum()) / max(rig_m.sum(), 1)
    return out_rgb.astype(np.uint8), warped_a, coverage
