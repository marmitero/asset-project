"""Peças do Goku base (gi laranja + camisa azul). y para baixo, chão = 0.

Silhueta v1.2: cabeça 46 px, tronco alongado (76 px), pernas 80 px,
mãos e pés grandes. Toda peça é desenhada na pose de repouso do esqueleto.
"""
from __future__ import annotations

from aura.shapes import (AH, AS, CF, CFP, CL, F, HI, HIP, L, P, SH, SHP, box, capsule,
                         oval, part)

J = {
    "head": (0, -166), "neck": (0, -158), "chest": (0, -126), "spine": (0, -108),
    "pelvis": (0, -92),
    "shoulder_f": (25, -156), "elbow_f": (34.1, -124.3), "wrist_f": (43.7, -98.0),
    "shoulder_b": (-19, -156), "elbow_b": (-27.9, -125.9), "wrist_b": (-37.5, -100.0),
    "hip_f": (12, -92), "knee_f": (13.5, -50), "ankle_f": (15, -12), "toe_f": (35, -4),
    "hip_b": (-12, -92), "knee_b": (-13.5, -50), "ankle_b": (-15, -12), "toe_b": (-35, -4),
    "cape": (0, -156), "hair_back": (0, -198),
}

HEAD_TOP = -212.0
HEAD_BOTTOM = -166.0
EYE_Y = -184.5


def _head():
    skull = [(0.0, -212.0), (9.2, -210.8), (15.2, -205.0), (17.6, -196.0),
             (16.8, -185.0), (13.4, -177.0), (7.6, -170.6), (0.0, -168.8),
             (-7.0, -170.4), (-12.8, -176.0), (-16.2, -185.0), (-16.8, -195.0),
             (-13.6, -205.0), (-7.2, -210.4)]
    ops = [
        F(skull, "skin"),
        F(oval(16.0, -184.0, 3.6, 5.6), "skin"),
        CL([(15.4, -188.0), (16.0, -184.6), (15.4, -180.6)], "skin_sh", 1.5),
        CF(capsule((-10.2, -172.0), (-3.4, -169.6), 8.6, 6.8), "skin_sh"),
        AS("skin_sh", 2.6, 3.6),
        AH("skin_hi", -2.6, -3.0),
        CL([(7.0, -170.2), (11.6, -173.2)], "skin_sh", 1.3),
        CL([(-12.0, -195.0), (-9.0, -204.0)], "skin_sh", 1.1),
    ]
    return part("head", J["head"], ops, bone="head", z=110)


def _face(kind: str = "neutral"):
    y = EYE_Y
    closed = kind == "blink"
    dead = kind == "dead"
    squint = kind in ("angry", "crit", "strain", "hurt")
    eye_l = (3.4, y)
    eye_r = (-8.2, y)
    ops = []

    def sclera(cx, w=3.5, h=4.3):
        return [(cx - w, y + 0.2), (cx - w * 0.66, y - h * 0.86), (cx + w * 0.34, y - h),
                (cx + w * 0.94, y - h * 0.34), (cx + w * 0.72, y + h * 0.66),
                (cx - w * 0.42, y + h * 0.80)]

    if not dead:
        ops.append(F(sclera(eye_r[0], 3.4, 4.2), "eye_white"))
        ops.append(F(sclera(eye_l[0], 3.6, 4.5), "eye_white"))
    if closed:
        ops.append(CL([(eye_r[0] - 3.4, y + 0.6), (eye_r[0], y + 2.0), (eye_r[0] + 3.2, y + 0.2)],
                      "eye_dark", 1.9))
        ops.append(CL([(eye_l[0] - 3.6, y + 0.6), (eye_l[0], y + 2.0), (eye_l[0] + 3.4, y + 0.2)],
                      "eye_dark", 1.9))
    elif dead:
        for cx in (eye_r[0], eye_l[0]):
            ops.append(CL([(cx - 2.8, y - 2.6), (cx + 2.8, y + 2.6)], "eye_dark", 1.7))
            ops.append(CL([(cx - 2.8, y + 2.6), (cx + 2.8, y - 2.6)], "eye_dark", 1.7))
    else:
        hh = 1.9 if squint else 2.4
        ops.append(F(oval(eye_r[0] - 0.2, y + 0.4, 1.9, hh), "eye_dark"))
        ops.append(F(oval(eye_l[0] - 0.1, y + 0.4, 2.0, hh + 0.2), "eye_dark"))
        ops.append(F(oval(eye_r[0] - 0.9, y - 0.7, 0.75, 0.9), "eye_white"))
        ops.append(F(oval(eye_l[0] - 0.8, y - 0.7, 0.8, 0.95), "eye_white"))
        # cilio superior espesso
        ops.append(CL([(eye_r[0] - 3.4, y - 3.2), (eye_r[0] + 0.2, y - 4.4),
                       (eye_r[0] + 3.2, y - 3.0)], "eye_dark", 1.3))
        ops.append(CL([(eye_l[0] - 3.6, y - 3.4), (eye_l[0] + 0.2, y - 4.8),
                       (eye_l[0] + 3.4, y - 3.2)], "eye_dark", 1.3))
        if kind in ("hurt", "crit"):
            ops.append(SHP(capsule((eye_r[0] - 3.2, y - 5.4), (eye_r[0] + 2.0, y - 3.8),
                                   3.4, 2.8), "skin_sh"))

    by = y - 7.4

    def brow(cx, inner, outer, thick=2.4):
        return [(cx - 4.6, by + outer), (cx - 0.6, by + inner - 1.0),
                (cx + 3.4, by + outer - 0.2),
                (cx + 3.4, by + outer - 0.2 + thick),
                (cx - 0.6, by + inner - 1.0 + thick),
                (cx - 4.6, by + outer + thick)]

    if kind == "shock":
        ops += [P([(-13.6, by + 0.8), (-8.8, by - 3.4), (-4.4, by - 0.2),
                   (-4.4, by + 1.6), (-8.8, by - 1.4), (-13.6, by + 2.2)], "hair"),
                P([(-0.6, by - 0.2), (3.8, by - 3.8), (8.2, by + 0.4),
                   (8.2, by + 2.2), (3.8, by - 1.6), (-0.6, by + 1.6)], "hair")]
    elif kind == "crit":
        ops += [P([(-14.0, by + 2.8), (-8.8, by - 2.6), (-4.2, by + 2.0),
                   (-8.8, by - 0.4)], "hair"),
                P([(-0.8, by + 2.0), (3.8, by - 2.8), (8.6, by + 2.6),
                   (3.8, by - 0.6)], "hair")]
    elif kind in ("angry", "combat", "strain"):
        ops += [P(brow(-8.6, 2.0, 4.2), "hair"), P(brow(3.6, 2.0, 4.2), "hair")]
    elif kind == "hurt":
        ops += [P(brow(-8.6, -1.4, -0.8), "hair"), P(brow(3.6, -1.4, -0.8), "hair")]
    elif kind == "smirk":
        ops += [P(brow(-8.6, 1.0, 1.6), "hair"), P(brow(3.6, -0.2, 2.2), "hair")]
    else:
        ops += [P(brow(-8.6, 0.9, 1.8), "hair"), P(brow(3.6, 0.9, 1.8), "hair")]

    ops.append(CL([(13.4, -179.0), (14.8, -176.8), (13.0, -176.0)], "skin_sh", 1.4))
    ops.append(CL([(-3.4, -173.4), (1.4, -173.0)], "skin_sh", 1.0))
    my = -171.6
    if kind in ("angry", "crit", "hurt", "strain"):
        ops.append(F([(2.6, my), (8.0, my - 1.2), (10.6, my + 0.2), (8.4, my + 2.4),
                      (4.2, my + 2.2), (2.6, my + 0.7)], "mouth"))
        ops.append(F([(4.2, my + 0.5), (7.2, my + 0.2), (8.0, my + 1.5), (4.9, my + 1.7)],
                     "eye_white"))
    elif kind == "shock":
        ops.append(F(oval(6.6, my + 0.9, 2.4, 2.9), "mouth"))
    elif kind == "smirk":
        ops.append(CL([(3.0, my + 1.0), (7.2, my + 0.2), (10.4, my - 2.0)], "mouth", 1.8))
    elif kind == "dead":
        ops.append(CL([(3.4, my), (8.2, my + 1.4)], "mouth", 1.6))
    else:
        ops.append(CL([(3.0, my + 0.4), (7.2, my + 0.4)], "mouth", 1.8))
    return part(f"face_{kind}", J["head"], ops, bone="head", z=111)


def _hair_front():
    mass = [(-18.0, -199.0), (-18.2, -205.4), (-14.2, -210.6), (-6.8, -213.2),
            (2.0, -213.4), (10.4, -211.0), (16.4, -205.6), (18.2, -198.6),
            (17.0, -195.6), (12.4, -198.4), (6.0, -196.8), (-0.6, -199.0),
            (-7.4, -196.8), (-13.4, -198.8)]
    ops = [F(mass, "hair")]
    spikes = [
        [(-17.4, -200.4), (-28.8, -210.0), (-21.4, -212.4), (-12.8, -207.4)],
        [(-13.2, -205.4), (-18.4, -221.0), (-10.6, -219.0), (-4.8, -210.4)],
        [(-5.2, -210.4), (-6.6, -226.0), (-0.4, -219.0), (2.8, -212.4)],
        [(2.4, -212.2), (5.2, -225.4), (9.4, -217.0), (11.0, -210.6)],
        [(10.6, -210.0), (18.6, -220.0), (18.0, -211.0), (17.8, -204.0)],
        [(17.4, -204.4), (28.6, -210.0), (22.8, -202.0), (19.8, -196.6)],
    ]
    for sp in spikes:
        ops.append(P(sp, "hair"))
    ops += [
        CL([(-21.8, -215.4), (-13.6, -208.0)], "hair_sh", 1.2),
        CL([(-10.6, -219.0), (-5.4, -209.4)], "hair_sh", 1.2),
        CL([(-0.4, -219.0), (1.2, -212.0)], "hair_sh", 1.2),
        CL([(9.4, -217.0), (8.8, -210.0)], "hair_sh", 1.2),
        CL([(18.2, -213.0), (16.8, -204.0)], "hair_sh", 1.2),
    ]
    # franja curta acima das sobrancelhas
    ops += [
        P([(-17.6, -199.2), (-10.8, -200.4), (-13.6, -195.8), (-18.0, -196.4)], "hair"),
        P([(-6.6, -198.4), (0.6, -199.0), (-2.6, -193.8), (-8.6, -195.4)], "hair"),
        P([(2.2, -198.8), (9.0, -198.0), (6.2, -192.6), (0.6, -194.8)], "hair"),
        P([(10.2, -197.6), (16.6, -199.6), (16.2, -194.4), (11.0, -195.0)], "hair"),
    ]
    ops += [AS("hair_sh", 3.0, 3.6), AH("hair_hi", -2.8, -3.2)]
    return part("hair_front", J["head"], ops, bone="head", z=115)


def _hair_back():
    mass = [(-17.8, -194.0), (-20.6, -183.0), (-19.0, -172.0), (-13.0, -165.0),
            (-3.6, -163.6), (3.2, -167.0), (7.2, -175.0), (4.8, -184.0),
            (0.4, -191.0), (-6.6, -197.0)]
    ops = [F(mass, "hair")]
    for s in ([(-19.0, -186.0), (-28.0, -190.0), (-21.2, -182.0)],
              [(-17.8, -176.0), (-26.2, -174.0), (-19.0, -171.6)],
              [(-9.2, -166.0), (-11.2, -158.6), (-4.0, -164.4)]):
        ops.append(P(s, "hair"))
    ops += [AS("hair_sh", 2.4, 3.0), AH("hair_hi", -2.2, -2.6)]
    return part("hair_back", J["hair_back"], ops, bone="hair_back_01", z=40)


def _torso():
    gi = [(-27.0, -150.0), (-17.0, -156.6), (-6.0, -158.4), (8.0, -158.4),
          (18.0, -156.4), (28.0, -149.4), (26.4, -140.0), (23.0, -130.0),
          (19.4, -118.0), (17.4, -102.0), (19.0, -92.4), (-19.0, -92.4),
          (-17.4, -102.0), (-19.4, -118.0), (-23.0, -130.0), (-26.4, -140.0)]
    ops = [
        F(capsule((0, -166.0), (0, -152.0), 14.4, 16.4), "skin"),
        F(gi, "gi"),
        # V do decote com camisa azul
        CFP([(-11.4, -158.6), (0.0, -137.0), (11.4, -158.6), (6.6, -159.2),
             (0.0, -147.6), (-6.6, -159.2)], "blue"),
        CFP([(-12.6, -158.0), (-1.4, -135.0), (1.4, -135.8), (-9.6, -158.6)], "blue_sh"),
        CFP([(12.6, -158.0), (1.4, -135.0), (-1.4, -135.8), (9.6, -158.6)], "blue_sh"),
        # faixa
        F([(-20.4, -104.0), (20.4, -104.0), (21.2, -92.0), (-21.2, -92.0)], "blue"),
        L([(-19.8, -98.0), (19.8, -98.0)], "blue_sh", 1.3),
        L([(17.6, -102.4), (5.0, -100.0), (-4.0, -101.6)], "blue_hi", 1.5),
        AS("gi_sh", 3.4, 4.6),
        AH("gi_hi", -3.0, -3.4),
        CL([(-21.6, -144.0), (-18.0, -128.0), (-15.6, -110.0)], "gi_sh", 1.5),
        CL([(8.6, -152.0), (5.6, -136.0), (3.6, -120.0)], "gi_sh", 1.3),
        CL([(-7.0, -108.0), (-2.0, -120.0)], "gi_sh", 1.1),
    ]
    return part("torso", J["spine"], ops, bone="spine", z=90)


def _pelvis():
    pants = [(-18.4, -97.0), (18.4, -97.0), (18.8, -89.6), (15.4, -84.0),
             (4.6, -83.0), (0.0, -86.0), (-4.6, -83.0), (-15.4, -84.0), (-18.8, -89.6)]
    ops = [F(pants, "blue"), AS("blue_sh", 3.0, 3.8), AH("blue_hi", -2.4, -3.0),
           CL([(-10.0, -80.2), (-3.0, -82.2)], "blue_sh", 1.3),
           CL([(2.0, -81.8), (9.0, -79.8)], "blue_sh", 1.3)]
    return part("pelvis", J["pelvis"], ops, bone="pelvis", z=80)


def _arm(side: str):
    s = side
    sh, el, wr = J[f"shoulder_{s}"], J[f"elbow_{s}"], J[f"wrist_{s}"]
    out = {}
    # manga CURTA azul (camisa) cobrindo o deltoide
    dx, dy = el[0] - sh[0], el[1] - sh[1]
    Lm = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / Lm, dy / Lm
    cuff = (sh[0] + ux * 16.0, sh[1] + uy * 16.0)
    sleeve = capsule(sh, cuff, 23.0, 19.0)
    ops_s = [F(sleeve, "blue"), AS("blue_sh", 2.8, 3.4), AH("blue_hi", -2.0, -2.4),
             CF(capsule(cuff, (cuff[0] + ux * 1.8, cuff[1] + uy * 1.8), 19.4, 19.0), "blue_sh"),
             CL([(sh[0] - 5.4, sh[1] + 3), (cuff[0] - 6.6, cuff[1] + 3)], "blue_sh", 1.1)]
    out[f"upper_arm_{s}"] = part(f"upper_arm_{s}", sh, ops_s,
                                bone=f"upper_arm_{s}", z=130 if s == "f" else 60)
    # braço nu
    fore = capsule(((el[0] + sh[0]) / 2 + 1, (el[1] + sh[1]) / 2), wr, 17.5, 14.5)
    bx, by = wr[0] - el[0], wr[1] - el[1]
    bL = (bx * bx + by * by) ** 0.5
    bux, buy = bx / bL, by / bL
    nx, ny = -buy, bux
    b0 = (wr[0] - bux * 8.4 - nx * 7.8, wr[1] - buy * 8.4 - ny * 7.8)
    b1 = (wr[0] - bux * 8.4 + nx * 7.8, wr[1] - buy * 8.4 + ny * 7.8)
    b2 = (wr[0] - bux * 1.0 + nx * 8.0, wr[1] - buy * 1.0 + ny * 8.0)
    b3 = (wr[0] - bux * 1.0 - nx * 8.0, wr[1] - buy * 1.0 - ny * 8.0)
    ops = [F(fore, "skin"), AS("skin_sh", 2.8, 3.4), AH("skin_hi", -2.0, -2.4),
           F([b0, b1, b2, b3], "blue"), HI([b0, b2], "blue_hi"),
           CL([(el[0] + 1, el[1] + 9), (wr[0] - 1, wr[1] - 7)], "skin_sh", 1.1)]
    out[f"forearm_{s}"] = part(f"forearm_{s}", el, ops, bone=f"forearm_{s}",
                               z=131 if s == "f" else 61)
    # punho fechado
    hand = [(-8.2, -7.6), (0.2, -11.0), (8.0, -7.6), (11.0, 0.4), (7.6, 9.4),
            (-1.2, 10.6), (-8.6, 5.4), (-9.8, -1.4)]
    hand = [(wr[0] + x, wr[1] + y) for x, y in hand]
    ops = [F(hand, "skin"), AS("skin_sh", 2.6, 3.0), AH("skin_hi", -2.0, -2.4),
           CL([(wr[0] - 4.0, wr[1] + 2.0), (wr[0] + 1.2, wr[1] + 2.8),
               (wr[0] + 5.4, wr[1] + 1.0)], "skin_sh", 1.1)]
    out[f"hand_{s}"] = part(f"hand_{s}", wr, ops, bone=f"hand_{s}",
                            z=132 if s == "f" else 62)
    return out


def _leg(side: str):
    s = side
    hip, knee, ankle = J[f"hip_{s}"], J[f"knee_{s}"], J[f"ankle_{s}"]
    out = {}
    thigh = capsule((hip[0] + (2.4 if s == "f" else -2.4), hip[1]), knee, 25, 20, bulge=0.04)
    out[f"thigh_{s}"] = part(
        f"thigh_{s}", hip,
        [F(thigh, "blue"), AS("blue_sh", 3.2, 4.0), AH("blue_hi", -2.6, -3.0),
         CL([(hip[0] - 6, hip[1] + 6), (knee[0] - 4, knee[1] - 8)], "blue_sh", 1.4)],
        bone=f"thigh_{s}", z=100 if s == "f" else 70)
    shin = capsule(knee, (ankle[0], ankle[1] - 2), 21, 16)
    ops = [F(shin, "blue"), AS("blue_sh", 2.8, 3.6), AH("blue_hi", -2.2, -2.8),
           F([(ankle[0] - 8.6, ankle[1] - 10.0), (ankle[0] + 8.8, ankle[1] - 10.0),
              (ankle[0] + 8.4, ankle[1] - 3.0), (ankle[0] - 8.2, ankle[1] - 3.0)], "blue_sh")]
    out[f"shin_{s}"] = part(f"shin_{s}", knee, ops, bone=f"shin_{s}",
                            z=101 if s == "f" else 71)
    # bota compacta: sola em ankle+12 (y=0 do mundo)
    # bota com bico para frente: calcanhar atras, ponta em x+17, sola em ankle.y+12
    boot = [(ankle[0] - 9.4, ankle[1] - 10.4), (ankle[0] + 4.4, ankle[1] - 11.4),
            (ankle[0] + 12.0, ankle[1] - 6.0), (ankle[0] + 17.4, ankle[1] + 1.6),
            (ankle[0] + 17.8, ankle[1] + 9.2), (ankle[0] + 15.0, ankle[1] + 12.0),
            (ankle[0] - 9.0, ankle[1] + 12.0), (ankle[0] - 10.4, ankle[1] + 2.0)]
    ops = [F(boot, "blue"), AS("blue_sh", 2.8, 3.4), AH("blue_hi", -2.4, -2.8),
           F([(ankle[0] - 9.8, ankle[1] + 8.6), (ankle[0] + 17.6, ankle[1] + 8.6),
              (ankle[0] + 17.8, ankle[1] + 9.6), (ankle[0] + 15.0, ankle[1] + 12.0),
              (ankle[0] - 9.0, ankle[1] + 12.0)], "boot_sole"),
           CF(capsule((ankle[0] + 12.6, ankle[1] + 2.4), (ankle[0] + 16.6, ankle[1] + 5.0),
                      7.0, 5.0), "blue_hi"),
           L([(ankle[0] - 3.4, ankle[1] - 5.2), (ankle[0] + 7.4, ankle[1] - 6.2)],
             "lace", 1.8)]
    out[f"foot_{s}"] = part(f"foot_{s}", ankle, ops, bone=f"foot_{s}",
                            z=102 if s == "f" else 72)
    return out


def build_goku_parts() -> dict:
    parts = {"head": _head()}
    for kind in ("neutral", "combat", "angry", "strain", "hurt", "crit", "shock",
                 "smirk", "dead", "blink"):
        parts[f"face_{kind}"] = _face(kind)
    parts["hair_front"] = _hair_front()
    parts["hair_back"] = _hair_back()
    parts["torso"] = _torso()
    parts["pelvis"] = _pelvis()
    parts.update(_arm("f"))
    parts.update(_arm("b"))
    parts.update(_leg("f"))
    parts.update(_leg("b"))
    return parts
