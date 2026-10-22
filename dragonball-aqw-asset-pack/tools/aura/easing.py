"""Avaliador de curvas de easing — lê standards/easing_library.json."""
from __future__ import annotations

import json
import math
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_LIB: dict | None = None


def _load() -> dict:
    global _LIB
    if _LIB is None:
        _LIB = {}
        p = _ROOT / "standards" / "easing_library.json"
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(data.get("curves"), dict):
                    _LIB = data["curves"]
            except Exception:
                _LIB = {}
    return _LIB


_ALIASES = {
    "linear": "linear",
    "in": "ease_in_cubic",
    "out": "ease_out_cubic",
    "in_out": "smoothstep",
    "back": "ease_out_back",
    "elastic": "ease_out_elastic",
    "sine": "smoothstep",
}


def _power(t: float, p: float, direction: str) -> float:
    if direction == "in":
        return t ** p
    if direction == "out":
        return 1 - (1 - t) ** p
    return 0.5 * (2 * t) ** p if t < 0.5 else 1 - 0.5 * (2 - 2 * t) ** p


def _back(t: float, s: float, direction: str) -> float:
    if direction == "in":
        return t * t * ((s + 1) * t - s)
    if direction == "out":
        return 1 + (t - 1) ** 2 * ((s + 1) * (t - 1) + s)
    if t < 0.5:
        return 0.5 * ((2 * t) ** 2 * ((s + 1) * 2 * t - s))
    return 0.5 * ((2 * t - 2) ** 2 * ((s + 1) * (2 * t - 2) + s) + 2)


def _elastic(t: float, amp: float, period: float) -> float:
    if t in (0.0, 1.0):
        return t
    s = period / (2 * math.pi) * math.asin(min(1.0, 1 / amp))
    return amp * 2 ** (-10 * t) * math.sin((t - s) * (2 * math.pi) / period) + 1


def ease(t: float, name: str = "smoothstep") -> float:
    t = max(0.0, min(1.0, float(t)))
    key = _ALIASES.get(name, name)
    c = _load().get(key)
    if not isinstance(c, dict):
        return 3 * t * t - 2 * t * t * t
    kind = c.get("type", "smoothstep")
    if kind == "linear":
        return t
    if kind == "power":
        return _power(t, float(c.get("power", 2)), c.get("direction", "in_out"))
    if kind == "back":
        return _back(t, float(c.get("overshoot", 1.70158)), c.get("direction", "out"))
    if kind == "elastic":
        return _elastic(t, float(c.get("amplitude", 1.0)), float(c.get("period", 0.3)))
    if kind == "cubic_hermite":
        p0, p1 = float(c.get("p0", 0.0)), float(c.get("p1", 0.0))
        p2, p3 = float(c.get("p2", 1.0)), float(c.get("p3", 1.0))
        t2, t3 = t * t, t * t * t
        return ((2 * t3 - 3 * t2 + 1) * p0 + (t3 - 2 * t2 + t) * p1
                + (-2 * t3 + 3 * t2) * p2 + (t3 - t2) * p3)
    return 3 * t * t - 2 * t * t * t
