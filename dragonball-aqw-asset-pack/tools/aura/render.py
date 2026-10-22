"""Renderizador de clipes: clipe -> lista de frames RGBA de 512x512."""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from PIL import Image

from aura.anim import Clip, pose_from_params
from aura.dummy import draw_dummy, popup_text
from aura.rig import ActorRig
from aura.scene import (GROUND_Y, H, W, dust_puff, fx_charge, fx_impact, fx_impact_at, fx_slash,
                        hud_label, make_background, motion_trail, screen_shake,
                        timeline_strip, vignette)
from aura.easing import ease

GIF_FPS = 25
BASE_FPS = 24


@dataclass
class ShowConfig:
    background: str = "grid"
    zoom: float = 1.0
    show_hud: bool = True
    show_shadow: bool = True
    show_fx: bool = True
    show_timeline: bool = False
    motion_trail: bool = True
    caption: str = ""
    loop_pause: int = 0
    camera_follow: bool = True
    facing: int = 1
    vignette: bool = True
    # cena de combate: dummy + feedback (doc 05 §4.1)
    dummy: bool = False
    dummy_x: float = 0.79
    dummy_scale: float = 1.0
    feedback: bool = False


@dataclass
class RenderedClip:
    name: str
    frames: list[Image.Image]
    events: list = field(default_factory=list)
    duration_ms: int = 0
    meta: dict = field(default_factory=dict)


def _face_for(events, frame, default="neutral"):
    face = default
    for ev in events:
        if ev["type"] == "face" and ev["frame"] <= frame:
            face = ev["id"]
    for ev in events:
        if ev["type"] == "blink":
            f0 = ev["frame"]
            dur = ev.get("duration", 4)
            if f0 <= frame < f0 + dur:
                return "blink"
    return face


def _event_progress(events, frame, kinds, span):
    """Progresso 0..1 do FX mais recente do tipo, com janela em frames."""
    best = None
    for ev in events:
        if ev["type"] in kinds and ev["frame"] <= frame:
            best = ev
    if best is None:
        return None, 0.0
    p = (frame - best["frame"]) / span
    if p < 0 or p > 1:
        return None, 0.0
    return best, p


def _shake_offset(events, frame, fps):
    amt = 0.0
    for ev in events:
        if ev["type"] != "shake":
            continue
        level = ev.get("level", "light")
        dur_ms = {"light": 120, "heavy": 180, "crit": 260, "ultimate": 350}[level]
        amp = {"light": 3, "heavy": 6, "crit": 10, "ultimate": 14}[level]
        dur_f = dur_ms / 1000 * fps
        dt = frame - ev["frame"]
        if 0 <= dt < dur_f:
            k = 1 - dt / dur_f
            amt += amp * k * math.sin(dt * 2.9 + 0.7)
    return amt


def _hp_bar(canvas, cx: float, y: float, scale: float, hp: float = 1.0) -> None:
    from PIL import ImageDraw as _ID
    d = _ID.Draw(canvas)
    w, h = 86 * scale, 9 * scale
    x0, x1 = cx - w / 2, cx + w / 2
    y0, y1 = y, y + h
    d.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], fill=(10, 10, 14, 210))
    if hp > 0.01:
        d.rectangle([x0, y0, x0 + w * max(0.02, hp), y1], fill=(214, 62, 54, 255))
        d.rectangle([x0, y0, x0 + w * hp * 0.6, y0 + h * 0.45],
                    fill=(246, 120, 104, 255))


class ClipRenderer:
    def __init__(self, rig: ActorRig, skel, faces: list[str] | None = None):
        self.rig = rig
        self.skel = skel
        self.trail: list[tuple[float, float]] = []
        self.faces = faces or ["neutral"]
        self._bg_cache: dict[str, Image.Image] = {}

    def background(self, kind: str) -> Image.Image:
        if kind not in self._bg_cache:
            bg = make_background(kind, (W, H))
            if True:
                bg = vignette(bg, 0.35)
            self._bg_cache[kind] = bg
        return self._bg_cache[kind].copy()

    # ------------------------------------------------------------------
    def frame(self, clip: Clip, clip_frame: float, cfg: ShowConfig) -> Image.Image:
        params = clip.sample(clip_frame)
        pose = pose_from_params(params, self.skel)

        # IK targets seguem o root para que o corpo nao "descole" dos pes
        facing = cfg.facing
        for ev in clip.events:
            if ev["type"] == "facing" and clip_frame >= ev["frame"]:
                facing = ev["value"]
        # flip horizontal: espelha o alvo de IK quando o personagem vira
        if facing < 0:
            for k in list(pose.pos.keys()):
                if k.startswith("_foot"):
                    x, y = pose.pos[k]
                    pose.pos[k] = (-x, y)

        face = _face_for(clip.events, clip_frame)
        self.rig.attachments["face"] = f"face_{face}"

        actor, sockets = self.rig.render(pose, facing=facing, zoom=cfg.zoom,
                                         out_size=(W, H), shadow=cfg.show_shadow)
        canvas = self.background(cfg.background)

        hit_event = None
        for ev in clip.events:
            if ev["type"] in ("hit", "miss", "block") and ev["frame"] <= clip_frame:
                hit_event = ev

        # ---------------- dummy: encostado na mao no frame de impacto
        dummy_cx = W * cfg.dummy_x
        if cfg.dummy:
            hand = sockets.get("hand_f")
            if hit_event and hand:
                dummy_cx = max(dummy_cx, hand[0] + 30 * cfg.dummy_scale)
            else:
                dummy_cx = max(dummy_cx, W * 0.78)
            dummy_cx = min(dummy_cx, W - 46 * cfg.dummy_scale)
            lean = squash = flash = 0.0
            if hit_event:
                dt = clip_frame - hit_event["frame"]
                power = {"light": 6, "heavy": 13, "crit": 20}.get(
                    hit_event.get("power", "light"), 6)
                if 0 <= dt <= 10:
                    k = math.exp(-dt / 4.0)
                    lean = power * k * (1 if hit_event["type"] == "hit" else 0.35)
                    squash = 0.9 * k
                    flash = k if hit_event["type"] != "miss" else 0.0
            draw_dummy(canvas, dummy_cx, GROUND_Y, cfg.dummy_scale, lean=lean,
                       squash=squash, flash=flash)
            hp = 1.0
            if hit_event and hit_event["type"] != "miss":
                hp = max(0.0, 1.0 - (0.42 if hit_event.get("power") == "crit" else 0.16))
            _hp_bar(canvas, dummy_cx, GROUND_Y - 214 * cfg.dummy_scale,
                    cfg.dummy_scale * 0.9, hp)

        # rastro de movimento do punho (fluidez percebida)
        hand = sockets.get("hand_f")
        trail_on = cfg.motion_trail and any(
            e["type"] in ("hit", "release", "miss") for e in clip.events)
        if cfg.show_fx and trail_on and hand:
            self.trail.append(hand)
            self.trail = self.trail[-7:]
            if len(self.trail) >= 3:
                pts = [(x, y) for x, y in self.trail[:-1]]
                canvas.alpha_composite(motion_trail((W, H), pts, width=13, alpha=120))

        canvas.alpha_composite(actor)

        fx_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if cfg.show_fx:
            ev, p = _event_progress(clip.events, clip_frame, {"fx", "hit"}, 9)
            if ev is not None:
                ident = ev.get("id", "")
                # impacto: nasce no ponto de contato (entre punho e dummy)
                contact = hand or (W * 0.7, H * 0.5)
                if cfg.dummy:
                    contact = (min(contact[0] + 26 * cfg.dummy_scale, dummy_cx - 6),
                               contact[1])
                if "slash" in ident:
                    org = ((hand or (W * 0.7, H * 0.5))[0] / W,
                           (hand or (W * 0.7, H * 0.5))[1] / H)
                    fx_layer.alpha_composite(fx_slash((W, H), p, origin=org, facing=facing))
                elif "impact" in ident:
                    lvl = "crit" if "crit" in ident else "heavy"
                    fx_layer.alpha_composite(fx_impact_at((W, H), contact, p, lvl))
                elif "guard" in ident or "spark" in ident:
                    fx_layer.alpha_composite(fx_impact_at((W, H), contact, p, "light"))
                elif "dust" in ident:
                    fx_layer.alpha_composite(dust_puff((W, H), p))
            ev, p = _event_progress(clip.events, clip_frame, {"charge", "release"}, 14)
            if ev is not None:
                fx_layer.alpha_composite(fx_charge((W, H), p))
        # ---------------- feedback de combate
        if cfg.feedback and hit_event:
            dt = clip_frame - hit_event["frame"]
            total = 26
            if 0 <= dt < total:
                prog = dt / total
                kind = hit_event["type"]
                px = dummy_cx + 10
                if kind == "miss":
                    popup_text(canvas, "MISS", px, GROUND_Y - 244, prog, "miss")
                elif kind == "block":
                    popup_text(canvas, "BLOCK", px, GROUND_Y - 244, prog, "miss")
                else:
                    power = hit_event.get("power", "light")
                    dmg = {"light": 148, "heavy": 612, "crit": 1840}.get(power, 148)
                    if power == "crit":
                        popup_text(canvas, f"CRIT {dmg}", px, GROUND_Y - 246, prog, "crit")
                    else:
                        popup_text(canvas, str(dmg), px, GROUND_Y - 240, prog, "damage")

        if cfg.show_hud:
            total = clip.frames
            f = int(clip_frame)
            hud_label(canvas, cfg.caption or clip.name,
                      right=f"f {f:02d}/{total}   {int(1000 * f / BASE_FPS)} ms",
                      sub=f"{clip.frames} frames @ {BASE_FPS} fps autorais  |  "
                          f"GIF {GIF_FPS} fps  |  loop={'sim' if clip.loop else 'nao'}")
            if cfg.show_timeline:
                hits = [e["frame"] for e in clip.events if e["type"] in ("hit", "release")]
                timeline_strip(canvas, f, total, hits)
        return canvas


def clip_to_gif_frames(clip: Clip, renderer: ClipRenderer, cfg: ShowConfig,
                       max_frames: int | None = None,
                       loop_hold: int = 0) -> RenderedClip:
    """Amostra o clipe na taxa do GIF (25 fps) preservando a duracao autoral."""
    n_gif = round(clip.frames * GIF_FPS / BASE_FPS)
    if max_frames:
        n_gif = min(n_gif, max_frames)
    frames = []
    renderer.trail = []
    step = BASE_FPS / GIF_FPS
    for i in range(n_gif):
        t = i * step
        frames.append(renderer.frame(clip, t, cfg))
    if loop_hold:
        frames.extend([frames[-1]] * loop_hold)
    dur = int(round(1000 * clip.frames / BASE_FPS))
    if loop_hold:
        dur += loop_hold * int(1000 / GIF_FPS)
    return RenderedClip(name=clip.name, frames=frames, events=clip.events,
                        duration_ms=dur, meta={"src_frames": clip.frames})
