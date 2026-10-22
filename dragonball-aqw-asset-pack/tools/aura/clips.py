"""Biblioteca de clipes do primeiro modelo (Goku base).

Convenções: ângulos em graus, positivo = horário na tela (personagem olhando
para a direita). `shoulder_*` negativo levanta o braço à frente.
Ciclos de locomoção são gerados analiticamente para garantir loop perfeito.
"""
from __future__ import annotations

import math

from aura.anim import Clip

FPS = 24

# ------------------------------------------------------------------ helpers


def _k(frames: dict[int, dict], ease: str = "in_out"):
    return [(f, p, ease) for f, p in sorted(frames.items())]


def _cycle(n: int, fn, step: int = 1, ease: str = "in_out"):
    keys = []
    for f in range(0, n + 1, step):
        keys.append((f, fn(f / n), ease))
    return keys


def _merge(*dicts):
    out = {}
    for d in dicts:
        out.update(d)
    return out


# ------------------------------------------------------------------ GUARD
GUARD = {
    "lean": 6.0, "crouch": 4.0, "root_y": 0.0,
    # braco da frente: sobe, dobra e cruza a frente do peito (guarda de luta)
    "shoulder_f": 26.0, "elbow_f": -96.0, "wrist_f": -10.0, "spread_f": -14.0,
    # braco de tras: protege o queixo
    "shoulder_b": 8.0, "elbow_b": -104.0, "wrist_b": 6.0, "spread_b": -6.0,
    "foot_fx": 14.0, "foot_bx": -16.0,
    "head_turn": 4.0, "head_tilt": -2.0,
}

NEUTRAL = {
    "lean": 1.0, "crouch": 0.0,
    "shoulder_f": -2.0, "elbow_f": -10.0, "wrist_f": 0.0, "spread_f": 0.0,
    "shoulder_b": 2.0, "elbow_b": -12.0, "wrist_b": 0.0, "spread_b": 0.0,
    "foot_fx": 0.0, "foot_bx": 0.0,
}


# ------------------------------------------------------------------ IDLE
def idle() -> Clip:
    n = 96

    def fn(t):
        b = math.sin(2 * math.pi * t)          # ciclo de respiração
        b2 = math.sin(2 * math.pi * t - 0.5)
        sway = math.sin(2 * math.pi * t) * 1.0
        return {
            "root_y": -3.4 * b,
            "crouch": 3.0 + 2.6 * b,
            "lean": 2.4 + 1.8 * b,
            "twist": 3.0 * math.sin(2 * math.pi * t + 0.8),
            "spread_f": 3.2 + 2.6 * b,
            "spread_b": 2.2 + 2.0 * b2,
            "shoulder_f": -2.0 - 3.4 * b,
            "shoulder_b": 1.0 + 3.0 * b2,
            "elbow_f": -10.0 - 5.0 * b,
            "elbow_b": -12.0 - 4.4 * b2,
            "head_turn": 3.0 * math.sin(2 * math.pi * t + 1.6) + 1.6,
            "head_tilt": -2.0 + 1.8 * b2,
            "foot_fx": 0.0, "foot_bx": 0.0,
            "foot_fy": 0.0, "foot_by": 0.0,
            "foot_fp": -1.4 * b2, "foot_bp": 1.0 * b2,
            "hair": 3.4 * math.sin(2 * math.pi * t * 1.5 - 0.9),
            "root_x": sway * 1.4,
            "head_tilt": (-2.0 + 1.8 * b2) + 1.2 * math.sin(4 * math.pi * t + 0.4),
        }

    return Clip("idle", n, _cycle(n, fn, step=4), loop=True,
                events=[{"frame": 58, "type": "blink", "duration": 4}], fps=FPS)


def idle_combat() -> Clip:
    n = 72

    def fn(t):
        b = math.sin(2 * math.pi * t)
        b2 = math.sin(4 * math.pi * t)          # bounce duplo
        return {
            "root_y": -1.2 + 2.4 * b2,
            "crouch": 5.0 + 1.6 * b2,
            "lean": 8.0 + 1.6 * b,
            "twist": 4.0 + 3.0 * b,
            "shoulder_f": 26.0 - 3.0 * b,
            "elbow_f": -96.0 - 4.0 * b2,
            "wrist_f": -10.0,
            "spread_f": -14.0 - 2.0 * b,
            "shoulder_b": 8.0 + 3.0 * b,
            "elbow_b": -104.0 + 4.0 * b2,
            "wrist_b": 6.0,
            "spread_b": -6.0,
            "head_turn": 4.0 - 2.0 * b,
            "head_tilt": -2.0 + 1.0 * b2,
            "foot_fx": 14.0, "foot_fy": 0.0,
            "foot_bx": -16.0 - 1.5 * b2, "foot_by": -1.0 - 1.0 * b2,
            "hair": 2.2 * math.sin(2 * math.pi * t - 0.7),
        }

    return Clip("idle_combat", n, _cycle(n, fn, step=3), loop=True,
                events=[{"frame": 40, "type": "blink", "duration": 4}], fps=FPS)


# ------------------------------------------------------------------ WALK
def walk() -> Clip:
    n = 24
    stride = 21.0
    lift = 17.0

    def leg(t):
        t %= 1.0
        x = stride * math.cos(2 * math.pi * t)
        swing = max(0.0, math.sin(2 * math.pi * (t - 0.5)))
        # levanta o pe cedo e baixa rapido (contato "seco" tipico de AQW)
        y = -lift * (swing ** 0.62)
        return x, y

    def fn(t):
        fx, fy = leg(t)
        bx, by = leg(t + 0.5)
        bob = math.cos(4 * math.pi * t)
        return {
            "foot_fx": fx, "foot_fy": fy,
            "foot_bx": bx, "foot_by": by,
            "foot_fp": -9.0 * math.sin(2 * math.pi * (t + 0.12)),
            "foot_bp": -9.0 * math.sin(2 * math.pi * (t + 0.62)),
            "root_y": 1.6 * bob - 0.6,
            "crouch": 9.0 + 1.6 * bob,
            "lean": 7.0 + 1.4 * bob,
            "twist": -5.0 * math.cos(2 * math.pi * t),
            "shoulder_f": 2.0 + 26.0 * math.cos(2 * math.pi * t),
            "elbow_f": -14.0 - 16.0 * max(0.0, math.cos(2 * math.pi * t)),
            "shoulder_b": 2.0 - 26.0 * math.cos(2 * math.pi * t),
            "elbow_b": -14.0 - 16.0 * max(0.0, -math.cos(2 * math.pi * t)),
            "spread_f": -2.0, "spread_b": -2.0,
            "head_turn": -1.0, "head_tilt": 1.2 * bob,
            "hair": 2.6 * math.cos(2 * math.pi * t - 0.8),
            "pelvis_rot": -2.5 * math.cos(2 * math.pi * t),
        }

    return Clip("walk", n, _cycle(n, fn, step=1), loop=True,
                events=[{"frame": 0, "type": "footstep", "foot": "f"},
                        {"frame": 12, "type": "footstep", "foot": "b"}], fps=FPS)


def run() -> Clip:
    n = 16
    stride = 30.0
    lift = 30.0

    def leg(t):
        t %= 1.0
        x = stride * math.cos(2 * math.pi * t)
        swing = max(0.0, math.sin(2 * math.pi * (t - 0.5)))
        y = -lift * swing ** 0.7
        return x, y

    def fn(t):
        fx, fy = leg(t)
        bx, by = leg(t + 0.5)
        bob = math.cos(4 * math.pi * t)
        return {
            "foot_fx": fx, "foot_fy": fy,
            "foot_bx": bx, "foot_by": by,
            "foot_fp": -16.0 * math.sin(2 * math.pi * (t + 0.10)),
            "foot_bp": -16.0 * math.sin(2 * math.pi * (t + 0.60)),
            "root_y": 3.4 * bob - 2.0,
            "crouch": 14.0 + 3.0 * bob,
            "lean": 19.0 + 3.0 * bob,
            "twist": -10.0 * math.cos(2 * math.pi * t),
            "shoulder_f": -8.0 + 40.0 * math.cos(2 * math.pi * t),
            "elbow_f": -52.0 - 18.0 * math.cos(2 * math.pi * t),
            "shoulder_b": -8.0 - 40.0 * math.cos(2 * math.pi * t),
            "elbow_b": -52.0 + 18.0 * math.cos(2 * math.pi * t),
            "spread_f": -8.0, "spread_b": -8.0,
            "head_turn": -2.0, "head_tilt": 4.0 + 1.6 * bob,
            "hair": 5.0 * math.cos(2 * math.pi * t - 1.1),
            "pelvis_rot": -5.0 * math.cos(2 * math.pi * t),
        }

    return Clip("run", n, _cycle(n, fn, step=1), loop=True,
                events=[{"frame": 0, "type": "footstep", "foot": "f"},
                        {"frame": 8, "type": "footstep", "foot": "b"}], fps=FPS)


# ------------------------------------------------------------------ ATTACK
def attack_light() -> Clip:
    keys = {
        0: dict(GUARD),
        3: _merge(GUARD, {"lean": -4, "twist": -16, "crouch": 7,
                          "shoulder_f": -22, "elbow_f": -104, "spread_f": -14,
                          "foot_fx": 6, "foot_bx": -22, "head_turn": -4,
                          "hair": -5, "root_x": -3}),
        6: _merge(GUARD, {"lean": 16, "twist": 26, "crouch": 3,
                          "shoulder_f": -78, "elbow_f": -6, "wrist_f": -4,
                          "spread_f": -2, "foot_fx": 30, "foot_fy": 0,
                          "foot_bx": -24, "foot_by": -3, "head_turn": 8,
                          "hair": 7, "root_x": 8, "root_y": -1}),
        8: _merge(GUARD, {"lean": 17, "twist": 28, "crouch": 3,
                          "shoulder_f": -80, "elbow_f": -3,
                          "foot_fx": 31, "foot_bx": -25, "foot_by": -3,
                          "head_turn": 9, "hair": 9, "root_x": 9, "root_y": -1}),
        11: _merge(GUARD, {"lean": 12, "twist": 18, "crouch": 5,
                           "shoulder_f": -64, "elbow_f": -36,
                           "foot_fx": 26, "foot_bx": -22, "head_turn": 6,
                           "hair": 3, "root_x": 5}),
        14: _merge(GUARD, {"lean": 8, "twist": 8, "crouch": 5,
                           "shoulder_f": -44, "elbow_f": -66,
                           "foot_fx": 18, "foot_bx": -18, "hair": -2, "root_x": 2}),
        18: dict(GUARD),
    }
    return Clip("attack_light_1", 18, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 6, "type": "hit", "power": "light"},
                        {"frame": 7, "type": "hitstop", "ms": 50},
                        {"frame": 7, "type": "fx", "id": "slash_light"}],
                )


def attack_heavy() -> Clip:
    keys = {
        0: dict(GUARD),
        5: _merge(GUARD, {"lean": -14, "twist": -26, "crouch": 12,
                          "shoulder_f": 6, "elbow_f": -128, "spread_f": -18,
                          "shoulder_b": 16, "elbow_b": -60, "spread_b": 18,
                          "foot_fx": 2, "foot_bx": -26, "head_turn": -8,
                          "head_tilt": -6, "hair": -9, "root_x": -8, "root_y": 4}),
        8: _merge(GUARD, {"lean": -16, "twist": -30, "crouch": 14,
                          "shoulder_f": 8, "elbow_f": -132, "spread_f": -20,
                          "shoulder_b": 18, "elbow_b": -64, "spread_b": 20,
                          "foot_fx": 2, "foot_bx": -28, "head_turn": -9,
                          "head_tilt": -7, "hair": -12, "root_x": -9, "root_y": 5}),
        12: _merge(GUARD, {"lean": 26, "twist": 34, "crouch": 2,
                           "shoulder_f": -96, "elbow_f": -4, "wrist_f": 6,
                           "spread_f": 2,
                           "shoulder_b": -40, "elbow_b": -22,
                           "foot_fx": 38, "foot_bx": -26, "foot_by": -5,
                           "head_turn": 12, "head_tilt": 4, "hair": 15,
                           "root_x": 14, "root_y": -2}),
        15: _merge(GUARD, {"lean": 27, "twist": 36, "crouch": 2,
                           "shoulder_f": -99, "elbow_f": -2, "wrist_f": 8,
                           "foot_fx": 39, "foot_bx": -27, "foot_by": -5,
                           "head_turn": 13, "head_tilt": 5, "hair": 17,
                           "root_x": 15, "root_y": -2}),
        19: _merge(GUARD, {"lean": 20, "twist": 22, "crouch": 7,
                           "shoulder_f": -76, "elbow_f": -30,
                           "foot_fx": 32, "foot_bx": -24, "head_turn": 8,
                           "hair": 4, "root_x": 9}),
        24: _merge(GUARD, {"lean": 11, "twist": 8, "crouch": 7,
                           "shoulder_f": -50, "elbow_f": -62,
                           "foot_fx": 22, "foot_bx": -20, "hair": -3, "root_x": 3}),
        30: dict(GUARD),
    }
    return Clip("attack_heavy", 30, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 12, "type": "hit", "power": "heavy"},
                        {"frame": 13, "type": "hitstop", "ms": 83},
                        {"frame": 13, "type": "fx", "id": "impact_heavy"},
                        {"frame": 13, "type": "shake", "level": "heavy"}])


def attack_crit() -> Clip:
    keys = {
        0: dict(GUARD),
        5: _merge(GUARD, {"lean": -18, "twist": -34, "crouch": 16,
                          "shoulder_f": 12, "elbow_f": -140, "spread_f": -22,
                          "shoulder_b": 22, "elbow_b": -52, "spread_b": 24,
                          "foot_fx": 0, "foot_bx": -30, "head_turn": -10,
                          "head_tilt": -8, "hair": -12, "root_x": -10, "root_y": 8}),
        8: _merge(GUARD, {"lean": -12, "twist": -26, "crouch": 4,
                          "shoulder_f": 4, "elbow_f": -120, "spread_f": -18,
                          "foot_fx": -4, "foot_bx": -18, "head_turn": -6,
                          "hair": -14, "root_x": -12, "root_y": -16}),
        10: _merge(GUARD, {"lean": 8, "twist": -10, "crouch": 0,
                           "shoulder_f": -50, "elbow_f": -80,
                           "foot_fx": 6, "foot_bx": -8, "hair": -6,
                           "root_x": -2, "root_y": -26}),
        12: _merge(GUARD, {"lean": 34, "twist": 40, "crouch": 0,
                           "shoulder_f": -112, "elbow_f": 4, "wrist_f": 10,
                           "shoulder_b": -46, "elbow_b": -30,
                           "foot_fx": 44, "foot_bx": -30, "foot_by": -8,
                           "head_turn": 14, "head_tilt": 8, "hair": 22,
                           "root_x": 18, "root_y": 2}),
        15: _merge(GUARD, {"lean": 34, "twist": 42, "crouch": 0,
                           "shoulder_f": -114, "elbow_f": 5,
                           "foot_fx": 45, "foot_bx": -30, "foot_by": -8,
                           "head_turn": 15, "head_tilt": 8, "hair": 24,
                           "root_x": 19, "root_y": 2}),
        19: _merge(GUARD, {"lean": 22, "twist": 22, "crouch": 10,
                           "shoulder_f": -78, "elbow_f": -46,
                           "foot_fx": 34, "foot_bx": -26, "head_turn": 8,
                           "hair": 6, "root_x": 10, "root_y": 4}),
        24: dict(GUARD),
    }
    return Clip("attack_crit", 24, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 12, "type": "hit", "power": "crit"},
                        {"frame": 13, "type": "hitstop", "ms": 133},
                        {"frame": 13, "type": "fx", "id": "impact_crit"},
                        {"frame": 13, "type": "shake", "level": "crit"}])


def attack_whiff() -> Clip:
    keys = {
        0: dict(GUARD),
        4: _merge(GUARD, {"lean": -6, "twist": -18, "crouch": 8,
                          "shoulder_f": -20, "elbow_f": -110, "spread_f": -12,
                          "foot_fx": 8, "foot_bx": -20, "head_turn": -4, "hair": -5}),
        8: _merge(GUARD, {"lean": 20, "twist": 32, "crouch": 2,
                          "shoulder_f": -84, "elbow_f": -2,
                          "foot_fx": 34, "foot_bx": -24, "foot_by": -4,
                          "head_turn": 10, "hair": 10, "root_x": 10}),
        11: _merge(GUARD, {"lean": 30, "twist": 44, "crouch": 1,
                           "shoulder_f": -96, "elbow_f": 14,
                           "foot_fx": 40, "foot_bx": -26, "foot_by": -5,
                           "head_turn": 14, "head_tilt": 6, "hair": 16,
                           "root_x": 15}),
        14: _merge(GUARD, {"lean": 34, "twist": 52, "crouch": 6,
                           "shoulder_f": -70, "elbow_f": -24,
                           "shoulder_b": -40, "elbow_b": -30, "spread_b": 26,
                           "foot_fx": 30, "foot_bx": -30, "head_turn": 16,
                           "head_tilt": 10, "hair": 6, "root_x": 12}),
        17: _merge(GUARD, {"lean": 16, "twist": 24, "crouch": 10,
                           "shoulder_f": -50, "elbow_f": -60,
                           "shoulder_b": -20, "elbow_b": -70,
                           "foot_fx": 22, "foot_bx": -22, "head_turn": 8,
                           "head_tilt": 4, "hair": -6, "root_x": 5}),
        20: dict(GUARD),
    }
    return Clip("attack_whiff", 20, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 8, "type": "miss", "fx": "whoosh"}])


# ------------------------------------------------------------------ SKILL
def cast() -> Clip:
    keys = {
        0: dict(GUARD),
        6: _merge(GUARD, {"lean": -8, "twist": -18, "crouch": 12,
                          "shoulder_f": 10, "elbow_f": -116, "spread_f": -20,
                          "shoulder_b": 14, "elbow_b": -104, "spread_b": -16,
                          "foot_fx": 6, "foot_bx": -22, "head_turn": -10,
                          "head_tilt": -4, "hair": -8, "root_x": -6}),
        12: _merge(GUARD, {"lean": -4, "twist": -26, "crouch": 16,
                           "shoulder_f": 22, "elbow_f": -132, "spread_f": -26,
                           "shoulder_b": 26, "elbow_b": -128, "spread_b": -24,
                           "foot_fx": 4, "foot_bx": -24, "head_turn": -12,
                           "head_tilt": -6, "hair": -12, "root_x": -8, "root_y": 4}),
        18: _merge(GUARD, {"lean": -6, "twist": -30, "crouch": 18,
                           "shoulder_f": 26, "elbow_f": -136, "spread_f": -28,
                           "shoulder_b": 30, "elbow_b": -132, "spread_b": -26,
                           "foot_fx": 4, "foot_bx": -26, "head_turn": -14,
                           "head_tilt": -8, "hair": -14, "root_x": -10, "root_y": 5}),
        22: _merge(GUARD, {"lean": 22, "twist": 10, "crouch": 4,
                           "shoulder_f": -74, "elbow_f": -18, "wrist_f": 6,
                           "spread_f": -4,
                           "shoulder_b": -60, "elbow_b": -40, "spread_b": 4,
                           "foot_fx": 26, "foot_bx": -26, "head_turn": 8,
                           "head_tilt": 2, "hair": 14, "root_x": 10, "root_y": -2}),
        26: _merge(GUARD, {"lean": 24, "twist": 12, "crouch": 3,
                           "shoulder_f": -78, "elbow_f": -14,
                           "shoulder_b": -64, "elbow_b": -36,
                           "foot_fx": 28, "foot_bx": -26, "head_turn": 8,
                           "hair": 16, "root_x": 11}),
        31: _merge(GUARD, {"lean": 14, "twist": 6, "crouch": 6,
                           "shoulder_f": -52, "elbow_f": -52,
                           "shoulder_b": -40, "elbow_b": -70,
                           "foot_fx": 20, "foot_bx": -22, "head_turn": 4, "hair": 2}),
        36: dict(GUARD),
    }
    return Clip("cast", 36, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 20, "type": "charge", "fx": "aura_charge"},
                        {"frame": 23, "type": "release", "fx": "ki_blast"},
                        {"frame": 23, "type": "shake", "level": "light"}])


# ------------------------------------------------------------------ REACT
def hurt_light() -> Clip:
    keys = {
        0: dict(GUARD),
        1: _merge(GUARD, {"lean": -14, "twist": -8, "crouch": 2,
                          "head_turn": -14, "head_tilt": -10,
                          "shoulder_f": -50, "elbow_f": -60, "spread_f": 8,
                          "shoulder_b": -40, "elbow_b": -70, "spread_b": 10,
                          "foot_fx": 10, "foot_bx": -18, "hair": -16,
                          "root_x": -5, "root_y": -2}),
        3: _merge(GUARD, {"lean": -10, "twist": -12, "crouch": 6,
                          "head_turn": -10, "head_tilt": -8,
                          "shoulder_f": -44, "elbow_f": -66,
                          "foot_fx": 8, "foot_bx": -20, "hair": -6,
                          "root_x": -8, "root_y": 0}),
        6: _merge(GUARD, {"lean": 0, "twist": -2, "crouch": 8,
                          "head_turn": -2, "head_tilt": -2,
                          "foot_fx": 10, "foot_bx": -18, "hair": 3,
                          "root_x": -6}),
        9: _merge(GUARD, {"lean": 4, "twist": 2, "crouch": 5,
                          "foot_fx": 12, "foot_bx": -17, "hair": 0,
                          "root_x": -3}),
        12: dict(GUARD),
    }
    return Clip("hurt_light", 12, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 0, "type": "flash", "color": "damage"}])


def hurt_crit() -> Clip:
    keys = {
        0: dict(GUARD),
        1: _merge(GUARD, {"lean": -26, "twist": -16, "crouch": 0,
                          "head_turn": -22, "head_tilt": -18,
                          "shoulder_f": -74, "elbow_f": -40, "spread_f": 22,
                          "shoulder_b": -64, "elbow_b": -44, "spread_b": 26,
                          "foot_fx": 4, "foot_bx": -16, "hair": -28,
                          "root_x": -10, "root_y": -6}),
        4: _merge(GUARD, {"lean": -34, "twist": -20, "crouch": 2,
                          "head_turn": -26, "head_tilt": -22,
                          "shoulder_f": -86, "elbow_f": -30, "spread_f": 28,
                          "shoulder_b": -76, "elbow_b": -36, "spread_b": 32,
                          "foot_fx": -6, "foot_fy": -8, "foot_bx": -26,
                          "foot_by": -6, "hair": -20,
                          "root_x": -26, "root_y": -14}),
        7: _merge(GUARD, {"lean": -22, "twist": -12, "crouch": 14,
                          "head_turn": -16, "head_tilt": -14,
                          "shoulder_f": -60, "elbow_f": -56, "spread_f": 18,
                          "shoulder_b": -50, "elbow_b": -60, "spread_b": 20,
                          "foot_fx": -10, "foot_fy": 0, "foot_bx": -30,
                          "hair": -4, "root_x": -34, "root_y": 6}),
        12: _merge(GUARD, {"lean": -4, "twist": -4, "crouch": 18,
                           "head_turn": -6, "head_tilt": -6,
                           "shoulder_f": -34, "elbow_f": -78,
                           "foot_fx": 2, "foot_bx": -24, "hair": 8,
                           "root_x": -30, "root_y": 10}),
        17: _merge(GUARD, {"lean": 4, "twist": 0, "crouch": 12,
                           "foot_fx": 8, "foot_bx": -20, "hair": 2,
                           "root_x": -20, "root_y": 4}),
        24: dict(GUARD),
    }
    return Clip("hurt_crit", 24, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 0, "type": "flash", "color": "damage"},
                        {"frame": 1, "type": "shake", "level": "crit"},
                        {"frame": 1, "type": "fx", "id": "hit_spark"}])


def death() -> Clip:
    keys = {
        0: _merge(GUARD, {"pelvis_rot": 0}),
        2: _merge(GUARD, {"lean": -24, "twist": -14, "crouch": 0,
                          "head_turn": -18, "head_tilt": -20,
                          "shoulder_f": -80, "elbow_f": -30, "spread_f": 26,
                          "shoulder_b": -70, "elbow_b": -34, "spread_b": 30,
                          "foot_fx": 2, "foot_bx": -16, "hair": -26,
                          "root_x": -8, "root_y": -4, "pelvis_rot": 0}),
        6: _merge(GUARD, {"lean": -18, "twist": -10, "crouch": 16,
                          "head_turn": -14, "head_tilt": -16,
                          "shoulder_f": -66, "elbow_f": -44, "spread_f": 20,
                          "shoulder_b": -58, "elbow_b": -48, "spread_b": 24,
                          "foot_fx": 0, "foot_bx": -18, "hair": -10,
                          "root_x": -14, "root_y": 6, "ik": 1, "pelvis_rot": 0}),
        10: _merge(GUARD, {"lean": -10, "twist": -6, "crouch": 30,
                           "shoulder_f": -40, "elbow_f": -60, "spread_f": 14,
                           "shoulder_b": -30, "elbow_b": -66, "spread_b": 16,
                           "foot_fx": -2, "foot_bx": -14, "hair": -4,
                           "root_x": -16, "root_y": 6, "pelvis_rot": 4,
                           "hip_f": -28, "knee_f": 64, "hip_b": -14, "knee_b": 52}),
        15: _merge(GUARD, {"ik": 0, "pelvis_rot": 34, "lean": -26, "twist": -8,
                           "shoulder_f": -20, "elbow_f": -40, "spread_f": 26,
                           "shoulder_b": -10, "elbow_b": -46, "spread_b": 30,
                           "hip_f": -46, "knee_f": 96, "hip_b": -30, "knee_b": 88,
                           "head_turn": -10, "head_tilt": -18, "hair": -8,
                           "root_x": -22, "root_y": 16}),
        22: _merge(GUARD, {"ik": 0, "pelvis_rot": 72, "lean": -10, "twist": -4,
                           "shoulder_f": 10, "elbow_f": -24, "spread_f": 34,
                           "shoulder_b": 16, "elbow_b": -30, "spread_b": 38,
                           "hip_f": -62, "knee_f": 104, "hip_b": -44, "knee_b": 96,
                           "head_turn": -4, "head_tilt": -12, "hair": -4,
                           "root_x": -30, "root_y": 24}),
        28: _merge(GUARD, {"ik": 0, "pelvis_rot": 84, "lean": 4, "twist": 0,
                           "shoulder_f": 24, "elbow_f": -14, "spread_f": 40,
                           "shoulder_b": 30, "elbow_b": -18, "spread_b": 44,
                           "hip_f": -70, "knee_f": 108, "hip_b": -52, "knee_b": 100,
                           "head_turn": 0, "head_tilt": -6, "hair": 2,
                           "root_x": -34, "root_y": 30}),
        34: _merge(GUARD, {"ik": 0, "pelvis_rot": 86, "lean": 6,
                           "shoulder_f": 26, "elbow_f": -10, "spread_f": 42,
                           "shoulder_b": 32, "elbow_b": -14, "spread_b": 46,
                           "hip_f": -72, "knee_f": 110, "hip_b": -54, "knee_b": 102,
                           "head_tilt": -2, "hair": 0, "root_x": -34, "root_y": 32}),
        40: _merge(GUARD, {"ik": 0, "pelvis_rot": 87, "lean": 6,
                           "shoulder_f": 27, "elbow_f": -9, "spread_f": 43,
                           "shoulder_b": 33, "elbow_b": -13, "spread_b": 47,
                           "hip_f": -73, "knee_f": 110, "hip_b": -55, "knee_b": 102,
                           "head_tilt": -1, "hair": 0, "root_x": -34, "root_y": 33}),
    }
    return Clip("death", 40, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 0, "type": "flash", "color": "damage"},
                        {"frame": 1, "type": "shake", "level": "crit"},
                        {"frame": 15, "type": "face", "id": "dead"}])


# ------------------------------------------------------------------ DEFENSE
def dodge() -> Clip:
    keys = {
        0: dict(GUARD),
        2: _merge(GUARD, {"lean": -12, "crouch": 12,
                          "shoulder_f": -20, "elbow_f": -100, "spread_f": -18,
                          "shoulder_b": -10, "elbow_b": -104, "spread_b": -14,
                          "foot_fx": 8, "foot_bx": -18, "hair": -12,
                          "root_x": 6, "root_y": 4}),
        6: _merge(GUARD, {"lean": -18, "twist": -10, "crouch": 6,
                          "shoulder_f": -30, "elbow_f": -86, "spread_f": -10,
                          "shoulder_b": -20, "elbow_b": -92, "spread_b": -8,
                          "foot_fx": -14, "foot_fy": -12, "foot_bx": -30,
                          "foot_by": -6, "hair": -18,
                          "root_x": -34, "root_y": -20}),
        10: _merge(GUARD, {"lean": -6, "crouch": 14,
                           "shoulder_f": -28, "elbow_f": -90,
                           "shoulder_b": -18, "elbow_b": -96,
                           "foot_fx": 2, "foot_fy": 0, "foot_bx": -24,
                           "hair": 4, "root_x": -46, "root_y": 6}),
        13: _merge(GUARD, {"lean": 2, "crouch": 8,
                           "foot_fx": 8, "foot_bx": -20, "hair": 1,
                           "root_x": -42, "root_y": 2}),
        16: _merge(GUARD, {"root_x": -40}),
    }
    return Clip("evade_backstep", 16, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 2, "type": "fx", "id": "dust_kick"}],
                )


def block_impact() -> Clip:
    keys = {
        0: _merge(GUARD, {"shoulder_f": -52, "elbow_f": -104, "spread_f": -16,
                          "shoulder_b": -36, "elbow_b": -112, "spread_b": -12,
                          "crouch": 8, "lean": 10}),
        1: _merge(GUARD, {"shoulder_f": -46, "elbow_f": -112, "spread_f": -22,
                          "shoulder_b": -30, "elbow_b": -118, "spread_b": -18,
                          "crouch": 14, "lean": 2, "head_tilt": -6,
                          "root_x": -8, "hair": -14, "foot_fx": 8, "foot_bx": -22}),
        4: _merge(GUARD, {"shoulder_f": -50, "elbow_f": -108, "spread_f": -18,
                          "shoulder_b": -34, "elbow_b": -114, "spread_b": -14,
                          "crouch": 12, "lean": 4, "head_tilt": -4,
                          "root_x": -12, "hair": -6, "foot_fx": 6, "foot_bx": -24}),
        7: _merge(GUARD, {"shoulder_f": -52, "elbow_f": -104, "spread_f": -16,
                          "shoulder_b": -36, "elbow_b": -112, "spread_b": -12,
                          "crouch": 9, "lean": 8, "root_x": -6, "hair": 1,
                          "foot_fx": 10, "foot_bx": -20}),
        10: _merge(GUARD, {"shoulder_f": -52, "elbow_f": -104, "spread_f": -16,
                           "shoulder_b": -36, "elbow_b": -112, "spread_b": -12,
                           "crouch": 8, "lean": 9, "foot_fx": 12, "foot_bx": -18}),
    }
    return Clip("block_impact", 10, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 0, "type": "block"},
                        {"frame": 0, "type": "shake", "level": "light"},
                        {"frame": 0, "type": "fx", "id": "guard_spark"}])


# ------------------------------------------------------------------ AIR
def jump_start() -> Clip:
    keys = {
        0: dict(NEUTRAL),
        2: _merge(NEUTRAL, {"crouch": 16, "lean": 10,
                            "shoulder_f": 20, "elbow_f": -20, "spread_f": -10,
                            "shoulder_b": 22, "elbow_b": -22, "spread_b": -8,
                            "foot_fx": 0, "foot_fy": 0, "root_y": 2, "hair": -3}),
        4: _merge(NEUTRAL, {"crouch": 22, "lean": 14,
                            "shoulder_f": 26, "elbow_f": -16, "spread_f": -12,
                            "shoulder_b": 28, "elbow_b": -18, "spread_b": -10,
                            "root_y": 4, "hair": -6}),
        6: _merge(NEUTRAL, {"crouch": -6, "lean": 6,
                            "shoulder_f": -30, "elbow_f": -40, "spread_f": 4,
                            "shoulder_b": -24, "elbow_b": -44, "spread_b": 6,
                            "foot_fx": -2, "foot_fy": -6, "foot_bx": 2, "foot_by": -8,
                            "root_y": -18, "hair": 10}),
        8: _merge(NEUTRAL, {"crouch": -10, "lean": 2,
                            "shoulder_f": -46, "elbow_f": -30, "spread_f": 8,
                            "shoulder_b": -40, "elbow_b": -34, "spread_b": 10,
                            "foot_fx": -4, "foot_fy": -10, "foot_bx": 2, "foot_by": -12,
                            "root_y": -30, "hair": 14}),
    }
    return Clip("jump_start", 8, _k(keys), loop=False, fps=FPS)


def fall() -> Clip:
    n = 8

    def fn(t):
        w = math.sin(2 * math.pi * t)
        return _merge(NEUTRAL, {
            "crouch": -8,
            "lean": 4 + 2 * w,
            "shoulder_f": -52 + 6 * w, "elbow_f": -28, "spread_f": 10,
            "shoulder_b": -46 - 6 * w, "elbow_b": -32, "spread_b": 12,
            "foot_fx": -4, "foot_fy": -10, "foot_bx": 2, "foot_by": -12,
            "hair": 12 + 3 * w,
            "head_tilt": 3,
        })

    return Clip("fall", n, _cycle(n, fn, step=2), loop=True, fps=FPS)


def land() -> Clip:
    keys = {
        0: _merge(NEUTRAL, {"crouch": -6, "lean": 4,
                            "shoulder_f": -44, "elbow_f": -32, "spread_f": 8,
                            "shoulder_b": -38, "elbow_b": -36, "spread_b": 10,
                            "foot_fx": -4, "foot_fy": -8, "foot_bx": 2, "foot_by": -10,
                            "root_y": -10, "hair": 10}),
        2: _merge(NEUTRAL, {"crouch": 26, "lean": 18,
                            "shoulder_f": 16, "elbow_f": -46, "spread_f": -12,
                            "shoulder_b": 18, "elbow_b": -50, "spread_b": -10,
                            "foot_fx": 4, "foot_bx": -8, "root_y": 6, "hair": -14}),
        4: _merge(NEUTRAL, {"crouch": 30, "lean": 20,
                            "shoulder_f": 20, "elbow_f": -40, "spread_f": -14,
                            "shoulder_b": 22, "elbow_b": -44, "spread_b": -12,
                            "foot_fx": 6, "foot_bx": -10, "root_y": 8, "hair": -8}),
        7: _merge(NEUTRAL, {"crouch": 14, "lean": 10,
                            "shoulder_f": 6, "elbow_f": -40, "spread_f": -6,
                            "shoulder_b": 8, "elbow_b": -44, "spread_b": -4,
                            "foot_fx": 2, "foot_bx": -4, "root_y": 3, "hair": 4}),
        10: _merge(NEUTRAL, {"crouch": 0, "lean": 1, "foot_fx": 0, "foot_bx": 0}),
    }
    return Clip("land", 10, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 2, "type": "shake", "level": "light"},
                        {"frame": 2, "type": "fx", "id": "dust_land"}])


def jump_land() -> Clip:
    """Salto completo em um único clipe (26f): antecipação, ar, queda, impacto."""
    keys = {
        0: dict(NEUTRAL),
        2: _merge(NEUTRAL, {"crouch": 16, "lean": 10, "root_y": 2, "hair": -3,
                            "shoulder_f": 20, "elbow_f": -20, "spread_f": -10,
                            "shoulder_b": 22, "elbow_b": -22, "spread_b": -8}),
        4: _merge(NEUTRAL, {"crouch": 24, "lean": 14, "root_y": 4, "hair": -7,
                            "shoulder_f": 28, "elbow_f": -16, "spread_f": -12,
                            "shoulder_b": 30, "elbow_b": -18, "spread_b": -10}),
        7: _merge(NEUTRAL, {"crouch": -8, "lean": 6, "root_y": -20, "hair": 12,
                            "shoulder_f": -34, "elbow_f": -38, "spread_f": 6,
                            "shoulder_b": -28, "elbow_b": -42, "spread_b": 8,
                            "foot_fx": -2, "foot_fy": -8, "foot_bx": 2, "foot_by": -10}),
        10: _merge(NEUTRAL, {"crouch": -10, "lean": 2, "root_y": -32, "hair": 15,
                             "shoulder_f": -50, "elbow_f": -28, "spread_f": 10,
                             "shoulder_b": -44, "elbow_b": -32, "spread_b": 12,
                             "foot_fx": -4, "foot_fy": -10, "foot_bx": 2, "foot_by": -12}),
        14: _merge(NEUTRAL, {"crouch": -8, "lean": 5, "root_y": -26, "hair": 13,
                             "shoulder_f": -46, "elbow_f": -34, "spread_f": 9,
                             "shoulder_b": -40, "elbow_b": -38, "spread_b": 11,
                             "foot_fx": -3, "foot_fy": -8, "foot_bx": 3, "foot_by": -10}),
        17: _merge(NEUTRAL, {"crouch": -4, "lean": 6, "root_y": -10, "hair": 9,
                             "shoulder_f": -40, "elbow_f": -36, "spread_f": 8,
                             "shoulder_b": -34, "elbow_b": -40, "spread_b": 10,
                             "foot_fx": -2, "foot_fy": -4, "foot_bx": 2, "foot_by": -6}),
        19: _merge(NEUTRAL, {"crouch": 28, "lean": 20, "root_y": 6, "hair": -16,
                             "shoulder_f": 18, "elbow_f": -44, "spread_f": -12,
                             "shoulder_b": 20, "elbow_b": -48, "spread_b": -10,
                             "foot_fx": 5, "foot_bx": -9, "head_tilt": -6}),
        21: _merge(NEUTRAL, {"crouch": 32, "lean": 22, "root_y": 8, "hair": -9,
                             "shoulder_f": 22, "elbow_f": -38, "spread_f": -14,
                             "shoulder_b": 24, "elbow_b": -42, "spread_b": -12,
                             "foot_fx": 7, "foot_bx": -11, "head_tilt": -7}),
        24: _merge(NEUTRAL, {"crouch": 10, "lean": 8, "root_y": 2, "hair": 4,
                             "shoulder_f": 6, "elbow_f": -40, "spread_f": -6,
                             "shoulder_b": 8, "elbow_b": -44, "spread_b": -4,
                             "foot_fx": 2, "foot_bx": -4}),
        26: _merge(NEUTRAL, {"crouch": 0, "lean": 1, "hair": 1}),
    }
    return Clip("jump_land", 26, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 19, "type": "shake", "level": "light"},
                        {"frame": 19, "type": "fx", "id": "dust_land"},
                        {"frame": 19, "type": "face", "id": "strain"}])


# ------------------------------------------------------------------ TURN
def turn_180() -> Clip:
    keys = {
        0: dict(NEUTRAL),
        2: _merge(NEUTRAL, {"crouch": 10, "lean": 6, "twist": -14,
                            "shoulder_f": 10, "elbow_f": -20, "spread_f": -10,
                            "shoulder_b": -14, "elbow_b": -30, "spread_b": 8,
                            "foot_fx": 4, "foot_bx": -6, "hair": -8,
                            "root_y": 3, "head_turn": -18}),
        5: _merge(NEUTRAL, {"crouch": 14, "lean": 2, "twist": -26,
                            "shoulder_f": 16, "elbow_f": -14, "spread_f": -14,
                            "shoulder_b": -20, "elbow_b": -36, "spread_b": 12,
                            "foot_fx": -2, "foot_fy": -6, "foot_bx": -2,
                            "foot_by": -4, "hair": -14, "root_y": 4,
                            "head_turn": -30, "pelvis_rot": -8}),
        7: _merge(NEUTRAL, {"crouch": 6, "lean": 0, "twist": 22,
                            "shoulder_f": -16, "elbow_f": -30, "spread_f": 6,
                            "shoulder_b": -24, "elbow_b": -34, "spread_b": 10,
                            "foot_fx": 6, "foot_fy": -3, "foot_bx": -8,
                            "hair": 12, "root_y": 1, "head_turn": 16,
                            "pelvis_rot": 6}),
        9: _merge(NEUTRAL, {"crouch": 4, "twist": 10,
                            "shoulder_f": -8, "elbow_f": -24, "spread_f": 2,
                            "shoulder_b": -14, "elbow_b": -28, "spread_b": 6,
                            "hair": 5, "head_turn": 6, "root_y": 0}),
        12: dict(NEUTRAL),
    }
    return Clip("turn_180", 12, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 6, "type": "facing", "value": -1}])


# ------------------------------------------------------------------ COMBO / MONTAGE
def combo_light_3() -> Clip:
    """Três golpes encadeados: cada um começa da recuperação do anterior."""
    parts = [attack_light(), attack_light_2(), attack_light_3()]
    keys, events, off = [], [], 0
    for i, c in enumerate(parts):
        for f, p, e in c.keys:
            keys.append((off + f, p, e))
        for ev in c.events:
            ev = dict(ev)
            ev["frame"] = ev["frame"] + off
            events.append(ev)
        off += c.frames
        if i < len(parts) - 1:
            # breakdown de 2f que "amarra" o fim do golpe ao inicio do próximo
            last = parts[i].keys[-1][1]
            nxt = parts[i + 1].keys[0][1]
            blend = {k: round((last.get(k, 0.0) * 0.55 + nxt.get(k, 0.0) * 0.45), 2)
                     for k in set(last) | set(nxt)}
            keys.append((off - 2, dict(blend), "in_out"))
    out = Clip("combo_light_3", off, sorted(keys, key=lambda k: k[0]), loop=False,
               fps=FPS, events=events)
    out.seams = [18, 38]
    return out


def attack_light_2() -> Clip:
    """Cruzado de esquerda (20f)."""
    base = attack_light()
    keys = []
    for f, p, e in base.keys:
        p = dict(p)
        # espelha os braços: o golpe vem do braço de trás
        p["shoulder_b"] = p.get("shoulder_f", 0)
        p["elbow_b"] = p.get("elbow_f", -10)
        p["shoulder_f"] = -20.0
        p["elbow_f"] = -92.0
        if f in (6, 8):
            p["twist"] = -20.0
        keys.append((round(f * 20 / 18), p, e))
    return Clip("attack_light_2", 20, keys, loop=False, fps=FPS)


def attack_light_3() -> Clip:
    """Gancho ascendente (22f)."""
    keys = {
        0: dict(GUARD),
        4: _merge(GUARD, {"lean": -10, "twist": -22, "crouch": 14,
                          "shoulder_f": 14, "elbow_f": -124, "spread_f": -20,
                          "foot_fx": 8, "foot_bx": -24, "head_turn": -6,
                          "hair": -8, "root_x": -5}),
        8: _merge(GUARD, {"lean": -16, "twist": -28, "crouch": 20,
                          "shoulder_f": 18, "elbow_f": -128, "spread_f": -22,
                          "foot_fx": 6, "foot_bx": -26, "head_turn": -8,
                          "hair": -12, "root_x": -7, "root_y": 6}),
        11: _merge(GUARD, {"lean": 6, "twist": 34, "crouch": -4,
                           "shoulder_f": -128, "elbow_f": -34, "wrist_f": 8,
                           "spread_f": -6,
                           "foot_fx": 28, "foot_fy": -4, "foot_bx": -26,
                           "foot_by": -8, "head_turn": 12, "head_tilt": 8,
                           "hair": 16, "root_x": 10, "root_y": -8}),
        14: _merge(GUARD, {"lean": 8, "twist": 36, "crouch": -4,
                           "shoulder_f": -132, "elbow_f": -30, "wrist_f": 10,
                           "foot_fx": 30, "foot_fy": -4, "foot_bx": -26,
                           "foot_by": -8, "head_turn": 13, "head_tilt": 9,
                           "hair": 18, "root_x": 11, "root_y": -8}),
        18: _merge(GUARD, {"lean": 10, "twist": 16, "crouch": 6,
                           "shoulder_f": -66, "elbow_f": -58,
                           "foot_fx": 22, "foot_bx": -22, "head_turn": 6,
                           "hair": 4, "root_x": 5, "root_y": 2}),
        22: dict(GUARD),
    }
    return Clip("attack_light_3", 22, _k(keys), loop=False, fps=FPS,
                events=[{"frame": 11, "type": "hit", "power": "light"},
                        {"frame": 12, "type": "hitstop", "ms": 50},
                        {"frame": 12, "type": "fx", "id": "slash_light"},
                        {"frame": 12, "type": "shake", "level": "light"}])


CLIPS = {
    "idle": idle,
    "idle_combat": idle_combat,
    "walk": walk,
    "run": run,
    "turn_180": turn_180,
    "jump_start": jump_start,
    "fall": fall,
    "land": land,
    "jump_land": jump_land,
    "dodge": dodge,
    "evade_backstep": dodge,
    "block_impact": block_impact,
    "attack_light_1": attack_light,
    "attack_light_2": attack_light_2,
    "attack_light_3": attack_light_3,
    "combo_light_3": combo_light_3,
    "attack_heavy": attack_heavy,
    "attack_crit": attack_crit,
    "attack_whiff": attack_whiff,
    "cast": cast,
    "hurt_light": hurt_light,
    "hurt_crit": hurt_crit,
    "death": death,
}


def get(name: str) -> Clip:
    return CLIPS[name]()
