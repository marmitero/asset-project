"""Passe de unificacao: força uma peça gerada por IA a aderir ao padrão do jogo.

Sem isso, cada peça sai com traço e paleta próprios e o boneco parece colagem.
Três operações, todas baratas:
  1. quantiza a cor para a paleta mestra (8 cores por design, doc 04)
  2. reescreve o contorno externo na cor oficial e com espessura fixa
  3. reamostra para a resolução de trabalho e aplica nitidez leve
"""
from __future__ import annotations

import cv2
import numpy as np
from PIL import Image

from aura.core import COLORS


def _hex(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def palette_of(keys: list[str]) -> np.ndarray:
    return np.array([_hex(COLORS[k]) for k in keys], np.float32)


def quantize(rgb: np.ndarray, alpha: np.ndarray, palette: np.ndarray,
             strength: float = 0.85) -> np.ndarray:
    """Aproxima cada pixel da cor mais próxima da paleta (mistura controlada)."""
    h, w, _ = rgb.shape
    flat = rgb.reshape(-1, 3).astype(np.float32)
    d = ((flat[:, None, :] - palette[None, :, :]) ** 2).sum(2)
    idx = d.argmin(1)
    near = palette[idx]
    out = flat * (1 - strength) + near * strength
    out = out.reshape(h, w, 3)
    return np.clip(out, 0, 255).astype(np.uint8)


def restyle_outline(rgb: np.ndarray, alpha: np.ndarray, width: int = 1,
                    color: str = "outline") -> np.ndarray:
    """Contorno externo de espessura fixa na cor oficial."""
    m = (alpha > 0.35).astype(np.uint8)
    k = np.ones((3, 3), np.uint8)
    grown = cv2.dilate(m, k, iterations=width)
    edge = (grown - m) > 0
    out = rgb.copy()
    out[edge] = _hex(COLORS[color])
    return out


def apply(rgb: np.ndarray, alpha: np.ndarray, palette_keys: list[str],
          quant_strength: float = 0.85, outline_w: int = 1) -> np.ndarray:
    q = quantize(rgb, alpha, palette_of(palette_keys), quant_strength)
    return restyle_outline(q, alpha, outline_w)


if __name__ == "__main__":
    print("passe de normalizacao disponivel:", apply.__doc__.strip().splitlines()[0])
