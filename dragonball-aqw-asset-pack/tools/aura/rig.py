"""Montagem do ator: esqueleto + peças + ordem de camadas."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image

from aura.core import PartImage, draw_ellipse, _warp_onto
from aura.pose import Pose, Secondary, Skeleton, solve_leg

BACK_SLOTS = {"upper_arm_b", "forearm_b", "hand_b", "thigh_b", "shin_b", "foot_b", "weapon_back"}


class ActorRig:
    def __init__(self, skeleton: Skeleton, parts: dict[str, PartImage],
                 layers: list[dict], secondary_cfg: dict | None = None,
                 back_darken: float = 0.82, attachments: dict[str, str] | None = None):
        self.skel = skeleton
        self.parts = parts
        self.attachments = dict(attachments or {})
        self.layers = {row["slot"]: row["z"] for row in layers}
        self.slots = [row["slot"] for row in sorted(layers, key=lambda r: r["z"])]
        self.secondary = Secondary(skeleton, secondary_cfg or {})
        self.back_darken = back_darken

    # ---------------------------------------------------------------- render
    def render(self, pose: Pose, facing: int = 1, zoom: float = 1.0,
               out_size: tuple[int, int] = (512, 512), shadow: bool = True,
               dt: float = 1 / 60, use_ik: bool = True,
               shadow_scale: float = 1.0, shadow_alpha: int = 88,
               ground_clamp: bool = True) -> tuple[Image.Image, dict]:
        world = self.skel.solve(pose)

        if use_ik:
            for side in ("f", "b"):
                target = pose.pos.get(f"_foot_{side}")
                if target is not None:
                    pitch = pose.rot.get(f"_pitch_{side}", 0.0)
                    solve_leg(self.skel, world, side, target, pitch)
                    self.skel.recompute(world, pose, [f"foot_{side}"])

        # trava de chão: pés nunca penetram o piso (12 px = altura do tornozelo)
        if ground_clamp:
            for side in ("f", "b"):
                foot = world.get(f"foot_{side}")
                if foot and foot["pos"][1] > -12.0:
                    dy = foot["pos"][1] + 12.0
                    foot["pos"] = (foot["pos"][0], -12.0)
                    self.skel.recompute(world, pose, [f"foot_{side}"])
                    toe = world.get(f"toe_{side}")
                    if toe and toe["pos"][1] > -12.0:
                        toe["pos"] = (toe["pos"][0], -12.0)

        # secundárias (cabelo, capa, cauda)
        if self.secondary.chains:
            self.secondary.apply(world, pose, dt)

        S = 2 * zoom
        W = int(round(out_size[0] * S))
        H = int(round(out_size[1] * S))
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cx, gy = W / 2.0, H * (448.0 / 512.0)

        if shadow:
            _soft_shadow(canvas, cx, gy, 44 * zoom * 2 * shadow_scale,
                         10 * zoom * 2 * shadow_scale, shadow_alpha)

        for slot in self.slots:
            key = self.attachments.get(slot, slot)
            part = self.parts.get(key)
            if part is None:
                continue
            bone = self._bone_of(slot)
            w = world.get(bone)
            if w is None:
                continue
            px = (cx + w["pos"][0] * zoom * 2, gy + w["pos"][1] * zoom * 2)
            darken = self.back_darken if slot in BACK_SLOTS else 1.0
            delta = w["ang"] - self.skel.rest_world[bone]
            _warp_onto(canvas, part, px, delta, darken, scale=zoom)

        if facing < 0:
            canvas = canvas.transpose(Image.FLIP_LEFT_RIGHT)

        out = canvas.resize(out_size, Image.LANCZOS)

        sockets = {}
        for sock in self.skel.data.get("sockets", []):
            w = world.get(sock["bone"])
            if not w:
                continue
            ang = math.radians(w["ang"])
            ox, oy = sock["offset"]
            wx = w["pos"][0] + ox * math.cos(ang) - oy * math.sin(ang)
            wy = w["pos"][1] + ox * math.sin(ang) + oy * math.cos(ang)
            x = cx + wx * zoom * 2
            if facing < 0:
                x = W - x
            sockets[sock["name"]] = (x / S, (gy + wy * zoom * 2) / S)
        return out, sockets

    def _bone_of(self, slot: str) -> str:
        if not hasattr(self, "_bone_map"):
            self._bone_map = {row["slot"]: row["bone"] for row in self.skel.data["slots"]}
        return self._bone_map[slot]


def _soft_shadow(canvas: Image.Image, cx: float, cy: float, rx: float, ry: float,
                 alpha: int = 90) -> None:
    """Elipse com queda radial — evita o aspecto de 'disco' chapado."""
    from PIL import ImageDraw, ImageFilter
    w, h = int(rx * 2 + 8), int(ry * 2 + 8)
    if w <= 0 or h <= 0:
        return
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse([2, 2, w - 2, h - 2], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(max(1.0, ry * 0.55)))
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    layer.putalpha(mask.point(lambda v: int(v * alpha / 255)))
    canvas.alpha_composite(layer, (int(cx - w / 2), int(cy - h / 2)))


def load_layers(path: str | Path) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))["layers"]
