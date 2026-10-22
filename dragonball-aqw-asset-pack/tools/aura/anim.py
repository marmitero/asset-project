"""Sistema de animação: controles de alto nível -> pose do esqueleto.

Cada clipe é uma lista de keyframes sobre CONTROLES (lean, ângulos, alvos de pé),
não sobre ossos. Isso mantém a autoria legível e garante que a matriz de clipes
possa ser reescrita sem tocar nas peças.
"""
from __future__ import annotations

import math

from aura.pose import Pose

DEFAULTS: dict[str, float] = {
    # root
    "root_x": 0.0, "root_y": 0.0, "root_scale": 1.0,
    # tronco / cabeca
    "lean": 0.0, "twist": 0.0, "crouch": 0.0,
    "head_turn": 0.0, "head_tilt": 0.0,
    # bracos (delta em graus, horario positivo)
    "shoulder_f": 0.0, "elbow_f": 0.0, "wrist_f": 0.0, "spread_f": 0.0,
    "shoulder_b": 0.0, "elbow_b": 0.0, "wrist_b": 0.0, "spread_b": 0.0,
    # pernas
    "hip_f": 0.0, "hip_b": 0.0, "knee_f": 0.0, "knee_b": 0.0,
    "pelvis_rot": 0.0,
    "foot_fx": 0.0, "foot_fy": 0.0, "foot_bx": 0.0, "foot_by": 0.0,
    "foot_fp": 0.0, "foot_bp": 0.0,
    "ik": 1.0,
    # secundarias
    "hair": 0.0, "impulse": 0.0,
}

POSE_MAP = {
    "root": ("root_x", "root_y"),
}


from aura.easing import ease  # noqa: E402


class Clip:
    def __init__(self, name: str, frames: int, keys: list, loop: bool = False,
                 events: list | None = None, fps: int = 24):
        self.name = name
        self.frames = frames
        self.keys = sorted(keys, key=lambda k: k[0])
        self.loop = loop
        self.events = events or []
        self.fps = fps
        self.seams: list[int] = []

    def sample(self, frame: float) -> dict[str, float]:
        params = dict(DEFAULTS)
        if self.loop:
            frame = frame % self.frames
        else:
            frame = max(0.0, min(self.frames - 0.001, frame))
        names = set()
        for _, p, _ in self.keys:
            names.update(p.keys())
        for name in names:
            prev_f, prev_v, prev_ease = 0.0, DEFAULTS.get(name, 0.0), "in_out"
            nxt = None
            for f, p, e in self.keys:
                if name not in p:
                    continue
                if f <= frame:
                    prev_f, prev_v = f, p[name]
                else:
                    nxt = (f, p[name], e)
                    break
            if nxt is None:
                params[name] = prev_v
            else:
                span = nxt[0] - prev_f
                t = 0.0 if span <= 0 else (frame - prev_f) / span
                params[name] = prev_v + (nxt[1] - prev_v) * ease(t, prev_ease if span else "linear")
        return params


def pose_from_params(p: dict[str, float], skel) -> Pose:
    pose = Pose()
    lean = p["lean"]
    twist = p["twist"]
    crouch = p["crouch"]

    pose.pos["root"] = (p["root_x"], p["root_y"] + crouch)
    pose.rot["pelvis"] = -lean * 0.18 + twist * 0.06 + p["pelvis_rot"]
    pose.rot["spine"] = lean * 0.52
    pose.rot["chest"] = lean * 0.36 + twist * 0.10
    pose.rot["neck"] = -lean * 0.30 + p["head_turn"] * 0.35
    pose.rot["head"] = -lean * 0.18 + p["head_turn"] * 0.65 + p["head_tilt"]

    pose.rot["clavicle_f"] = p["spread_f"] * 0.25 - lean * 0.10
    pose.rot["upper_arm_f"] = p["shoulder_f"] + p["spread_f"]
    pose.rot["forearm_f"] = p["elbow_f"]
    pose.rot["hand_f"] = p["wrist_f"]

    pose.rot["clavicle_b"] = p["spread_b"] * 0.25 - lean * 0.10
    pose.rot["upper_arm_b"] = p["shoulder_b"] + p["spread_b"]
    pose.rot["forearm_b"] = p["elbow_b"]
    pose.rot["hand_b"] = p["wrist_b"]

    hf = skel.bones["foot_f"].pos
    hb = skel.bones["foot_b"].pos
    # o pelvis desce com crouch, entao os alvos de pe seguem o chao (nao o root)
    pose.pos["_foot_f"] = (hf[0] + p["foot_fx"], -hf[1] + p["foot_fy"])
    pose.pos["_foot_b"] = (hb[0] + p["foot_bx"], -hb[1] + p["foot_by"])
    pose.rot["_pitch_f"] = p["foot_fp"]
    pose.rot["_pitch_b"] = p["foot_bp"]
    if p["ik"] < 0.5:
        pose.pos.pop("_foot_f", None)
        pose.pos.pop("_foot_b", None)
        pose.rot["thigh_f"] = p["hip_f"]
        pose.rot["thigh_b"] = p["hip_b"]
        pose.rot["shin_f"] = p["knee_f"]
        pose.rot["shin_b"] = p["knee_b"]

    pose.rot["hair_back_01"] = p["hair"]
    return pose
