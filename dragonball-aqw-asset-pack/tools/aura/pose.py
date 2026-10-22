"""Esqueleto, cinemática direta, IK e molas secundárias."""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path


def rot(x: float, y: float, deg: float) -> tuple[float, float]:
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return (x * c - y * s, x * s + y * c)


@dataclass
class Bone:
    name: str
    parent: str | None
    pos: tuple[float, float]      # world y-up (autorais)
    dir_deg: float               # y-up
    length: float
    limit: tuple[float, float] = (-180.0, 180.0)

    @property
    def screen_pos(self):
        return (self.pos[0], -self.pos[1])

    @property
    def rest_screen_deg(self):
        return -self.dir_deg


@dataclass
class Pose:
    rot: dict[str, float] = field(default_factory=dict)     # delta horário na tela
    pos: dict[str, tuple[float, float]] = field(default_factory=dict)  # screen px
    scale: dict[str, tuple[float, float]] = field(default_factory=dict)

    def r(self, bone: str, fallback: float = 0.0) -> float:
        return self.rot.get(bone, fallback)

    def p(self, bone: str) -> tuple[float, float]:
        return self.pos.get(bone, (0.0, 0.0))

    def s(self, bone: str) -> tuple[float, float]:
        return self.scale.get(bone, (1.0, 1.0))


class Skeleton:
    def __init__(self, data: dict):
        self.data = data
        self.bones: dict[str, Bone] = {}
        for b in data["bones"]:
            self.bones[b["name"]] = Bone(
                name=b["name"], parent=b["parent"], pos=tuple(b["pos"]),
                dir_deg=b["dir_deg"], length=b["length_px"],
                limit=tuple(b.get("limit_deg", (-180, 180))),
            )
        self.order = [b["name"] for b in data["bones"]]
        self.rest_world: dict[str, float] = {}
        for name in self.order:
            b = self.bones[name]
            local = b.rest_screen_deg - (self.rest_world.get(b.parent, 0.0) if b.parent else 0.0)
            self.rest_world[name] = (self.rest_world.get(b.parent, 0.0) if b.parent else 0.0) + local
            self._local_rest = getattr(self, "_local_rest", {})
            self._local_rest[name] = local

    @classmethod
    def load(cls, path: str | Path) -> "Skeleton":
        return cls(json.loads(Path(path).read_text(encoding="utf-8")))

    def solve(self, pose: Pose) -> dict[str, dict]:
        world: dict[str, dict] = {}
        for name in self.order:
            b = self.bones[name]
            if b.parent is None:
                pos = b.screen_pos
                ang = b.rest_screen_deg
                sc = 1.0
                pos = (pos[0] + pose.p(name)[0], pos[1] + pose.p(name)[1])
            else:
                p = world[b.parent]
                d_ang = p["ang"] - self.rest_world[b.parent]
                off = (b.pos[0] - self.bones[b.parent].pos[0],
                       -(b.pos[1] - self.bones[b.parent].pos[1]))
                off = rot(off[0], off[1], d_ang)
                ox, oy = pose.p(name)
                pos = (p["pos"][0] + off[0] * p["sc"] + ox * p["sc"],
                       p["pos"][1] + off[1] * p["sc"] + oy * p["sc"])
                ang = p["ang"] + self._local_rest[name] + pose.r(name)
                sc = p["sc"]
            sx, sy = pose.s(name)
            sc = sc * (sx + sy) / 2.0
            world[name] = {"pos": pos, "ang": ang, "sc": sc}
        return world

    def recompute(self, world: dict, pose: Pose, roots: list[str]) -> None:
        """Recalcula descendentes depois de um IK ter reposicionado um osso."""
        targets: set[str] = set()
        for name in self.order:
            b = self.bones[name]
            if b.parent in roots or b.parent in targets:
                targets.add(b.name)
        for name in self.order:
            if name not in targets or self.bones[name].parent is None:
                continue
            b = self.bones[name]
            p = world[b.parent]
            d_ang = p["ang"] - self.rest_world[b.parent]
            off = (b.pos[0] - self.bones[b.parent].pos[0],
                   -(b.pos[1] - self.bones[b.parent].pos[1]))
            off = rot(off[0], off[1], d_ang)
            ox, oy = pose.p(name)
            world[name] = {
                "pos": (p["pos"][0] + off[0] * p["sc"] + ox * p["sc"],
                        p["pos"][1] + off[1] * p["sc"] + oy * p["sc"]),
                "ang": p["ang"] + self._local_rest[name] + pose.r(name),
                "sc": p["sc"],
            }


# ------------------------------------------------------------------ IK
def solve_leg(skel: Skeleton, world: dict, side: str, target: tuple[float, float],
              pitch: float = 0.0) -> None:
    """IK de 2 ossos: posiciona joelho e tornozelo para o alvo do pé (screen px)."""
    thigh = skel.bones[f"thigh_{side}"]
    shin = skel.bones[f"shin_{side}"]
    hip = world[f"thigh_{side}"]["pos"]
    l1, l2 = thigh.length, shin.length
    dx, dy = target[0] - hip[0], target[1] - hip[1]
    # evita a singularidade da perna esticada (dist ~= l1+l2), que faz o joelho
    # "estalar" entre as duas solucoes de IK
    dist = max(1e-3, min(math.hypot(dx, dy), (l1 + l2) * 0.975))
    base = math.degrees(math.atan2(dy, dx))
    cos_a = (l1 * l1 + dist * dist - l2 * l2) / (2 * l1 * dist)
    a = math.degrees(math.acos(max(-1.0, min(1.0, cos_a))))
    # joelho dobra para a FRENTE (+x): subtrai o angulo do quadril
    knee_ang = base - a
    knee = (hip[0] + l1 * math.cos(math.radians(knee_ang)),
            hip[1] + l1 * math.sin(math.radians(knee_ang)))
    ankle_ang = math.degrees(math.atan2(target[1] - knee[1], target[0] - knee[0]))
    world[f"thigh_{side}"] = {"pos": hip, "ang": knee_ang, "sc": world[f"thigh_{side}"]["sc"]}
    world[f"shin_{side}"] = {"pos": knee, "ang": ankle_ang, "sc": world[f"shin_{side}"]["sc"]}
    # o pe e desenhado na pose de repouso: mantem o angulo de repouso (+ pitch)
    world[f"foot_{side}"] = {
        "pos": target,
        "ang": skel.rest_world[f"foot_{side}"] + pitch,
        "sc": world[f"foot_{side}"]["sc"],
    }


class Spring:
    __slots__ = ("k", "c", "theta", "omega")

    def __init__(self, stiffness: float, damping: float):
        self.k = stiffness * 120.0
        self.c = damping * 18.0
        self.theta = 0.0
        self.omega = 0.0

    def step(self, target: float, dt: float) -> float:
        a = -self.k * (self.theta - target) - self.c * self.omega
        self.omega += a * dt
        self.theta += self.omega * dt
        return self.theta


class Secondary:
    """Cadeia de molas para cabelo, capa, cauda e faixa."""

    def __init__(self, skel: Skeleton, chains: dict):
        self.skel = skel
        self.chains = chains
        self.springs: dict[str, list[Spring]] = {}
        for name, cfg in chains.items():
            self.springs[name] = [Spring(cfg.get("stiffness", 0.5), cfg.get("damping", 0.2))
                                  for _ in cfg.get("bones", [])]

    def apply(self, world: dict, pose: Pose, dt: float, gain: float = 1.0,
              impulse: float = 0.0) -> None:
        for name, cfg in self.chains.items():
            bones = cfg.get("bones", [])
            if not bones:
                continue
            max_deg = cfg.get("max_deg", 20.0)
            parent_name = self.skel.bones[bones[0]].parent
            base_delta = world[parent_name]["ang"] - self.skel.rest_world[parent_name]
            springs = self.springs[name]
            for i, bone in enumerate(bones):
                target = base_delta * gain if i == 0 else 0.0
                theta = springs[i].step(target, dt)
                if impulse:
                    springs[i].omega += impulse * (1.0 + i * 0.4)
                theta = max(-max_deg, min(max_deg, theta))
                delta = base_delta - theta
                lo, hi = self.skel.bones[bone].limit
                delta = max(lo, min(hi, delta))
                world[bone]["ang"] = self.skel.rest_world[bone] + delta
