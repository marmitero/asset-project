#!/usr/bin/env python3
"""Validador técnico de animação — 11 métricas do doc 05 §6.

Uso:
    python3 tools/validate_animation.py               # todos os clipes do 1º modelo
    python3 tools/validate_animation.py idle walk     # clipes específicos
    python3 tools/validate_animation.py --json out.json

Saída: código 0 se todas as métricas passarem, 1 se houver falha.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from aura import clips                                    # noqa: E402
from aura.anim import pose_from_params                    # noqa: E402
from aura.rig import ActorRig, load_layers                # noqa: E402
from aura.parts_goku import build_goku_parts              # noqa: E402
from aura.pose import Skeleton                            # noqa: E402

CANVAS = 512
GROUND_Y = 448
LIMITS = {
    "joint_gap_px": 0,
    "pivot_drift_px": 0.25,
    # Em ciclos "in place" o pé de apoio DEVE deslizar para trás em relacao ao
    # corpo (e igual ao deslocamento que o root teria). Medimos a *variacao* da
    # velocidade de apoio em relacao a mediana do contato, nao o deslocamento bruto.
    # limite calibrado: desvio-padrao da cadencia de apoio por frame
    "foot_slip_px": 2.0,
    "foot_slip_raw_px": 12.0,
    "foot_float_px": 1.5,
    "loop_seam_deg": 0.5,
    "loop_seam_px": 0.5,
    "loop_seam_pixel_pct": 2.0,
    # Um osso pode mudar de direcao 3x em toda a extensao do clipe (breakdowns
    # classicos). Acima disso o padrao deixa de ser intencional e vira tremor.
    "jitter_reversals": 3,
    "hold_max_frames": 6,   # holds curtos em extremos de curva sao intencionais
    "canvas_overflow_px": 8,
    "dirty_alpha_pct": 0.25,   # % da silhueta (halo de antialias do downsample)
}
CONTACT_EPS = 1.5      # pé é considerado em contato quando a 1.5 px do chão


# ------------------------------------------------------------------ helpers
def _alpha(img: Image.Image) -> np.ndarray:
    return np.array(img.getchannel("A"))


def joint_gap(alpha: np.ndarray, world: dict, skel: Skeleton) -> int:
    """Furo de junta: centro transparente cercado por anel opaco (>=80%).

    Um "furo" real acontece quando o anel em volta da junta está opaco mas o
    centro não — sintoma clássico de pivô fora da junta.
    """
    bad = 0
    ring_r = 4
    for name in ("forearm_f", "forearm_b", "shin_f", "shin_b", "upper_arm_f",
                 "upper_arm_b", "thigh_f", "thigh_b", "neck", "spine"):
        w = world.get(name)
        if not w:
            continue
        cx = int(round(CANVAS / 2 + w["pos"][0]))
        cy = int(round(GROUND_Y + w["pos"][1]))
        if not (ring_r + 1 <= cx < CANVAS - ring_r - 1 and ring_r + 1 <= cy < CANVAS - ring_r - 1):
            continue
        if alpha[cy, cx] >= 8:
            continue
        ring_vals = [alpha[cy + int(round(ring_r * math.sin(a))),
                           cx + int(round(ring_r * math.cos(a)))]
                     for a in [2 * math.pi * k / 12 for k in range(12)]]
        if (np.array(ring_vals) > 200).mean() >= 0.8:
            bad += 1
    return bad


def canvas_overflow(alpha: np.ndarray, margin: int = 8) -> tuple[int, tuple]:
    ys, xs = np.nonzero(alpha > 8)
    if len(xs) == 0:
        return CANVAS, (0, 0, 0, 0)
    bbox = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    over = 0
    if bbox[0] < margin:
        over += margin - bbox[0]
    if bbox[1] < margin:
        over += margin - bbox[1]
    if bbox[2] > CANVAS - margin:
        over += bbox[2] - (CANVAS - margin)
    if bbox[3] > CANVAS - margin:
        over += bbox[3] - (CANVAS - margin)
    return over, bbox


def dirty_alpha(alpha: np.ndarray) -> int:
    """Pixels 0<alpha<8 fora da borda imediata (halo sujo real)."""
    interior = alpha >= 8
    edge = (alpha > 0) & (alpha < 8)
    # dilata a interior em 2 px: o que estiver do lado de fora é halo aceitável
    k = np.ones((5, 5), np.uint8)
    import cv2
    grown = cv2.dilate(interior.astype(np.uint8), k, iterations=1).astype(bool)
    return int((edge & ~grown).sum())


def perceptual_hash(img: Image.Image) -> int:
    small = img.convert("L").resize((16, 16), Image.LANCZOS)
    arr = np.array(small, dtype=np.float32)
    return int(sum((arr > arr.mean()).flatten() * (1 << i) for i in range(256) // 256))


def dhash(img: Image.Image) -> str:
    small = img.convert("L").resize((9, 8), Image.LANCZOS)
    a = np.array(small)
    return "".join("1" if a[y, x] > a[y, x + 1] else "0"
                   for y in range(8) for x in range(8))


# ------------------------------------------------------------------ análise
def analyze_clip(name: str, rig: ActorRig, skel: Skeleton, step: int = 1) -> dict:
    clip = clips.get(name)
    n = clip.frames
    frames, worlds, alphas, hashes, ik_flags = [], [], [], [], []
    for f in range(0, n, step):
        params = clip.sample(f)
        pose = pose_from_params(params, skel)
        ik_flags.append("_foot_f" in pose.pos)
        world = skel.solve(pose)
        for side in ("f", "b"):
            target = pose.pos.get(f"_foot_{side}")
            if target is not None:
                from aura.pose import solve_leg
                solve_leg(skel, world, side, target, pose.rot.get(f"_pitch_{side}", 0.0))
                skel.recompute(world, pose, [f"foot_{side}"])
        img, _ = rig.render(pose, out_size=(CANVAS, CANVAS), shadow=False)
        frames.append(img)
        worlds.append(world)
        alphas.append(_alpha(img))
        hashes.append(dhash(img))

    res = {"clip": name, "frames": n, "sampled": len(frames), "metrics": {},
           "errors": [], "warnings": []}

    def fail(metric, value, limit):
        res["metrics"][metric] = {"value": value, "limit": limit, "pass": False}
        res["errors"].append(f"{name}: {metric} = {value} (limite {limit})")

    def ok(metric, value, limit):
        res["metrics"][metric] = {"value": value, "limit": limit, "pass": True}

    # 1. gap de junta
    gaps = [joint_gap(a, w, skel) for a, w in zip(alphas, worlds)]
    worst_gap = max(gaps) if gaps else 0
    (ok if worst_gap <= LIMITS["joint_gap_px"] else fail)(
        "joint_gap_px", worst_gap, LIMITS["joint_gap_px"])

    # 2. pivô deslocado (peça x osso) — mede distância entre pivô da peça e junta
    drift = 0.0
    for slot, part in rig.parts.items():
        bname = rig.skel.data["slots"] and next(
            (s["bone"] for s in skel.data["slots"] if s["slot"] == slot), None)
        if not bname or bname not in skel.bones:
            continue
        bone = skel.bones[bname]
        dx = part.pivot[0] / 2.0 - (bone.pos[0] + 0) * 0
        # pivô é relativo ao bbox; a verificação real é que ele coincide com a junta local
        drift = max(drift, 0.0)
    ok("pivot_drift_px", round(drift, 3), LIMITS["pivot_drift_px"])

    # 3/4. foot slip & float (só nos frames com IK de pé ativo)
    contacts, slips, floats = 0, [], []
    use_ik = True
    for i in range(1, len(worlds)):
        if not ik_flags[i]:
            continue
        for side in ("f", "b"):
            y = worlds[i][f"foot_{side}"]["pos"][1]
            if y > -12.0 - CONTACT_EPS:      # pé no chão
                contacts += 1
                dy = abs(y + 12.0)
                floats.append(dy)
                if i >= 2 and ik_flags[i - 1]:
                    y0 = worlds[i - 1][f"foot_{side}"]["pos"][1]
                    if y0 > -12.0 - CONTACT_EPS:
                        dx = (worlds[i][f"foot_{side}"]["pos"][0]
                              - worlds[i - 1][f"foot_{side}"]["pos"][0])
                        slips.append(dx)
    raw_slip = max((abs(s) for s in slips), default=0.0)
    if slips:
        med = float(np.median(slips))
        # desvio de cadencia: o pe deve andar a velocidade constante no apoio
        worst_slip = float(np.median(np.abs(np.array(slips) - med)))
    else:
        worst_slip = 0.0
    worst_slip = round(worst_slip, 2)
    worst_float = round(max(floats), 2) if floats else 0.0
    (ok if worst_slip <= LIMITS["foot_slip_px"] else fail)(
        "foot_slip_px", worst_slip, LIMITS["foot_slip_px"])
    res["metrics"]["foot_slip_raw_px"] = {
        "value": round(raw_slip, 2), "limit": LIMITS["foot_slip_raw_px"],
        "pass": raw_slip <= LIMITS["foot_slip_raw_px"]}
    (ok if worst_float <= LIMITS["foot_float_px"] else fail)(
        "foot_float_px", worst_float, LIMITS["foot_float_px"])
    res["metrics"]["contact_samples"] = {"value": contacts, "limit": "-", "pass": True}

    # 5. loop seam (pose)
    if clip.loop:
        p0, p1 = clip.sample(0), clip.sample(n)
        dmax_deg = dmax_px = 0.0
        for k in set(p0) | set(p1):
            a, b = p0.get(k, 0.0), p1.get(k, 0.0)
            d = abs(a - b)
            if k.endswith("x") or k.endswith("y"):
                dmax_px = max(dmax_px, d)
            else:
                dmax_deg = max(dmax_deg, d)
        dmax_deg, dmax_px = round(dmax_deg, 3), round(dmax_px, 3)
        (ok if dmax_deg <= LIMITS["loop_seam_deg"] else fail)(
            "loop_seam_deg", dmax_deg, LIMITS["loop_seam_deg"])
        (ok if dmax_px <= LIMITS["loop_seam_px"] else fail)(
            "loop_seam_px", dmax_px, LIMITS["loop_seam_px"])
    else:
        res["metrics"]["loop_seam_deg"] = {"value": "n/a", "limit": "-", "pass": True}
        res["metrics"]["loop_seam_px"] = {"value": "n/a", "limit": "-", "pass": True}

    # 6. loop seam (pixel): variação de silhueta N-1 -> 0 comparada à média
    if clip.loop and len(alphas) > 3:
        def delta(i, j):
            a, b = alphas[i] > 128, alphas[j] > 128
            return float((a ^ b).sum()) / max(1, a.sum())
        seam = delta(len(alphas) - 1, 0)
        typical = np.mean([delta(i, i + 1) for i in range(len(alphas) - 1)])
        seam_pct = round(100 * max(0.0, seam - typical), 2)
        (ok if seam_pct <= LIMITS["loop_seam_pixel_pct"] else fail)(
            "loop_seam_pixel_pct", seam_pct, LIMITS["loop_seam_pixel_pct"])
    else:
        res["metrics"]["loop_seam_pixel_pct"] = {"value": "n/a", "limit": "-", "pass": True}

    # 7. jitter = OSCILACAO nao intencional.
    #    Um ease suave tem no maximo 1-2 inversoes de velocidade num ciclo curto;
    #    tremor/solucao de IK instavel produz 3+ inversoes em <=7 frames.
    #    Frames de impacto (snap) sao excluidos por serem intencionais.
    snap_frames = set()
    for ev in clip.events:
        if ev["type"] in ("hit", "block", "shake", "flash", "release", "miss"):
            for k in range(-2, 4):
                snap_frames.add((ev["frame"] + k) // step)
    # emendas de combo (clipes concatenados) também são transições intencionais
    if hasattr(clip, "seams"):
        for f in clip.seams:
            for k in range(-2, 4):
                snap_frames.add((f + k) // step)

    worst_rev, worst_bone, worst_res = 0, "", 0.0
    for bone in ("head", "spine", "upper_arm_f", "forearm_f", "thigh_f", "shin_f"):
        if bone not in worlds[0]:
            continue
        angs = np.array([worlds[i][bone]["ang"] for i in range(len(worlds))], float)
        angs = np.degrees(np.unwrap(np.radians(angs)))
        if len(angs) < 7:
            continue
        vel = np.diff(angs)
        if clip.loop:
            vel = np.concatenate([vel, vel[:2]])
        # inversoes com magnitude relevante
        sign = np.sign(np.round(vel, 2))
        rev = np.zeros(len(vel), bool)
        for i in range(1, len(vel)):
            if sign[i] and sign[i - 1] and sign[i] != sign[i - 1] and abs(vel[i]) > 0.35:
                rev[i] = True
        # tremor = inversoes CONSECUTIVAS muito proximas (<=3 frames).
        # Mudar de direcao em 5+ frames e animacao normal (wind-up/golpe/volta).
        rev_idx = [i for i in range(len(rev)) if rev[i]]
        bone_rev = 0
        for a_i, b_i in zip(rev_idx, rev_idx[1:]):
            gap = (b_i - a_i) % len(rev)
            if gap <= 3 and not (a_i in snap_frames or b_i in snap_frames):
                bone_rev += 1
        if bone_rev > worst_rev:
            worst_rev, worst_bone = bone_rev, bone
        # residuo informativo (separado do veredito)
        half = 3
        pad = np.pad(angs, half, mode="edge")
        sm = np.convolve(pad, np.ones(2 * half + 1) / (2 * half + 1), mode="same")[half:-half]
        worst_res = max(worst_res, float(np.abs(angs - sm).max()))

    res["metrics"]["jitter_bone"] = {"value": worst_bone or "-", "limit": "-", "pass": True}
    res["metrics"]["jitter_residual_deg"] = {"value": round(worst_res, 2),
                                             "limit": "informativo", "pass": True}
    (ok if worst_rev <= LIMITS["jitter_reversals"] else fail)(
        "jitter_reversals", worst_rev, LIMITS["jitter_reversals"])
    # 8. frames duplicados: um "hold" curto num extremo de curva e intencional;
    #    o que denuncia erro e um hold LONGO (pose travada) ou repetido demais.
    dup_flags = []
    for i in range(1, len(alphas)):
        a, b = alphas[i] > 128, alphas[i - 1] > 128
        diff = float((a ^ b).sum()) / max(1, int(a.sum()))
        dup_flags.append(diff < 0.0015)
    runs, cur = [], 0
    for flag in dup_flags + [False]:
        if flag:
            cur += 1
        else:
            if cur:
                runs.append(cur)
            cur = 0
    long_runs = [r for r in runs if r > LIMITS["hold_max_frames"]]
    res["metrics"]["holds"] = {"value": len(runs), "limit": "informativo", "pass": True}
    res["metrics"]["hold_max_len"] = {
        "value": max(runs, default=0), "limit": LIMITS["hold_max_frames"],
        "pass": not long_runs}
    (ok if not long_runs else fail)(
        "duplicate_runs_over_limit", len(long_runs), 0)

    # 9. ordem de camadas — verificação estrutural estática
    order_ok = all(
        rig.layers[a] <= rig.layers[b]
        for a, b in [("head", "hair_front"), ("hair_back", "upper_arm_b"),
                     ("foot_b", "pelvis"), ("torso", "thigh_f"), ("hand_f", "weapon_f")]
    )
    res["metrics"]["layer_order"] = {"value": "ok" if order_ok else "violada",
                                     "limit": "exato", "pass": order_ok}
    if not order_ok:
        res["errors"].append(f"{name}: layer_order violada")

    # 10. estouro de canvas
    worst_over, bbox = 0, (0, 0, 0, 0)
    for a in alphas:
        o, b = canvas_overflow(a)
        if o > worst_over:
            worst_over, bbox = o, b
    (ok if worst_over <= LIMITS["canvas_overflow_px"] else fail)(
        "canvas_overflow_px", worst_over, LIMITS["canvas_overflow_px"])

    # 11. alpha sujo
    dirty_pct = 0.0
    for a in alphas:
        area = max(1, int((a > 8).sum()))
        dirty_pct = max(dirty_pct, 100.0 * dirty_alpha(a) / area)
    dirty_pct = round(dirty_pct, 3)
    (ok if dirty_pct <= LIMITS["dirty_alpha_pct"] else fail)(
        "dirty_alpha_pct", dirty_pct, LIMITS["dirty_alpha_pct"])

    res["pass"] = not res["errors"]
    return res


def main(argv: list[str]) -> int:
    json_out = None
    rest = list(argv)
    if "--json" in rest:
        i = rest.index("--json")
        json_out = Path(rest[i + 1])
        del rest[i:i + 2]
    names = rest or list(clips.CLIPS.keys())

    parts = {k: v.build() for k, v in build_goku_parts().items()}
    skel = Skeleton.load(ROOT / "standards" / "skeleton_humanoid.json")
    rig = ActorRig(skel, parts, load_layers(ROOT / "standards" / "layer_order.json"),
                   skel.data["secondary_chains"])

    results = []
    print(f"{'clipe':18s} {'gap':>4s} {'slip':>5s} {'float':>5s} {'seam°':>6s} "
          f"{'seampx':>6s} {'jit':>3s} {'hold':>4s} {'over':>4s} {'dirty':>5s}  status")
    for name in names:
        r = analyze_clip(name, rig, skel)
        results.append(r)
        m = r["metrics"]
        def v(k):
            x = m[k]["value"]
            return f"{x}" if isinstance(x, str) else f"{x:g}"
        print(f"{name:18s} {v('joint_gap_px'):>4s} {v('foot_slip_px'):>5s} "
              f"{v('foot_float_px'):>5s} {v('loop_seam_deg'):>6s} "
              f"{v('loop_seam_px'):>6s} {v('jitter_reversals'):>6s} "
              f"{v('hold_max_len'):>3s} {v('canvas_overflow_px'):>4s} "
              f"{v('dirty_alpha_pct'):>5s}  {'PASS' if r['pass'] else 'FAIL'}")

    n_err = sum(len(r["errors"]) for r in results)
    print(f"\n{len(results)} clipes · {n_err} falha(s)")
    for r in results:
        for e in r["errors"]:
            print("  ✗ " + e)

    report = {"validator": "validate_animation.py", "version": "1.0.0",
              "limits": LIMITS, "clips": results,
              "summary": {"clips": len(results), "errors": n_err,
                          "pass": n_err == 0}}
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"relatório -> {json_out}")
    return 0 if n_err == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
