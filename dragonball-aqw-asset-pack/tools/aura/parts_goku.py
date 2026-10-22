"""Peças do Goku base (gi laranja + camisa azul). y para baixo, chão = 0.

Silhueta v1.2: cabeça 46 px, tronco alongado (76 px), pernas 80 px,
mãos e pés grandes. Toda peça é desenhada na pose de repouso do esqueleto.
"""
from __future__ import annotations

import math

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
EYE_Y = -190.0


def _head():
    # v2: cranio 3px mais largo em cada lado (o rosto v1 ficava espremido,
    # sem area util para olho + sobrancelha dentro dos 46 px de altura)
    skull = [(0.0, -213.4), (10.6, -212.0), (17.4, -206.0), (20.0, -196.6),
             (19.0, -185.6), (15.4, -177.2), (8.6, -171.2), (0.0, -169.6),
             (-7.8, -171.2), (-14.2, -176.6), (-17.8, -185.6), (-19.0, -195.6),
             (-15.4, -206.0), (-8.4, -211.6)]
    ops = [
        F(skull, "skin"),
        F(oval(16.0, -184.0, 3.6, 5.6), "skin"),
        CL([(15.4, -188.0), (16.0, -184.6), (15.4, -180.6)], "skin_sh", 1.5),
        CF(capsule((-10.2, -172.0), (-3.4, -169.6), 8.6, 6.8), "skin_sh"),
        AS("skin_sh", 2.0, 2.8),
        AH("skin_hi", -2.8, -3.2),
        CL([(7.0, -170.2), (11.6, -173.2)], "skin_sh", 1.3),
        CL([(-12.0, -195.0), (-9.0, -204.0)], "skin_sh", 1.1),
    ]
    return part("head", J["head"], ops, bone="head", z=110)


def _face(kind: str = "neutral"):
    """Rosto v2: esclera grande, iris que preenche o olho, cilio espesso.

    O v1 desenhava esclera enorme com pupila minima — lia como "olho de
    boneco". Aqui o iris ocupa ~60% da altura do olho e o cilio cobre a
    borda superior, que e o que da o olhar de anime.
    """
    y = EYE_Y
    closed = kind == "blink"
    dead = kind == "dead"
    squint = kind in ("angry", "crit", "strain", "hurt")
    eye_f = (4.6, y)      # olho da frente (lado +x = frente do personagem)
    eye_b = (-8.8, y)     # olho de tras
    ops = []

    def sclera(cx, w=4.5, h=5.2, tilt=0.55):
        """Amendoa: canto interno baixo, canto externo alto, base arredondada."""
        return [(cx - w, y + 0.6 + tilt),
                (cx - w * 0.55, y - h * 0.72),
                (cx + w * 0.10, y - h),
                (cx + w * 0.72, y - h * 0.72),
                (cx + w, y + 0.2 - tilt * 0.3),
                (cx + w * 0.62, y + h * 0.72),
                (cx - w * 0.20, y + h * 0.86),
                (cx - w * 0.72, y + h * 0.50)]

    def iris(cx, r, ry=None):
        ry = ry or r
        return [(cx + r * math.cos(2 * math.pi * i / 12),
                 y + 0.9 + ry * math.sin(2 * math.pi * i / 12)) for i in range(12)]

    if not dead:
        ops.append(F(sclera(eye_b[0], 4.3, 4.9), "eye_white"))
        ops.append(F(sclera(eye_f[0], 4.6, 5.2), "eye_white"))

    if closed:
        for cx in (eye_b[0], eye_f[0]):
            ops.append(CL([(cx - 4.0, y + 0.9), (cx - 0.4, y + 2.4), (cx + 3.6, y + 0.5)],
                          "eye_dark", 2.2))
    elif dead:
        for cx in (eye_b[0], eye_f[0]):
            ops.append(CL([(cx - 2.9, y - 2.7), (cx + 2.9, y + 2.7)], "eye_dark", 1.8))
            ops.append(CL([(cx - 2.9, y + 2.7), (cx + 2.9, y - 2.7)], "eye_dark", 1.8))
    else:
        hh = 0.62 if squint else 1.0
        for cx, r in ((eye_b[0], 3.0), (eye_f[0], 3.2)):
            ops.append(F(iris(cx, r, r * hh), "eye_dark"))
            ops.append(F(iris(cx, r * 0.46, r * 0.44 * hh), "eye_iris"))   # anel interno
            ops.append(F(oval(cx - r * 0.34, y + 0.9 - r * 0.40, r * 0.30, r * 0.30),
                         "eye_white"))                                     # brilho
        # cilio superior espesso, cobre o topo da esclera
        ops.append(CL([(eye_b[0] - 4.2, y - 1.6), (eye_b[0] - 1.4, y - 4.7),
                       (eye_b[0] + 3.4, y - 3.3)], "eye_dark", 1.7))
        ops.append(CL([(eye_f[0] - 4.5, y - 1.6), (eye_f[0] - 1.4, y - 5.0),
                       (eye_f[0] + 3.5, y - 3.5)], "eye_dark", 1.8))
        if kind in ("hurt", "crit"):
            ops.append(SHP(capsule((eye_b[0] - 3.4, y - 6.0), (eye_b[0] + 2.2, y - 4.2),
                                   3.6, 3.0), "skin_sh"))

    # by = base da sobrancelha. Precisa ficar ACIMA do cilio (y-5.0), com folga:
    # no v2 estava em y-7.2 e a sobrancelha (by+1.9+1.9) caia em y-3.4,
    # sobrepondo o cilio e fundindo sobrancelha+olho numa mascara preta.
    by = y - 10.6

    def brow(cx, inner, outer, thick=2.3):
        """Sobrancelha fina e separada do olho — no v2 ela encostava no cilio
        e os dois juntos viravam uma mascara preta na cara inteira."""
        return [(cx - 4.6, by + outer), (cx - 0.6, by + inner - 0.9),
                (cx + 3.3, by + outer - 0.2),
                (cx + 3.3, by + outer - 0.2 + thick),
                (cx - 0.6, by + inner - 0.9 + thick),
                (cx - 4.6, by + outer + thick)]

    BROW_OUT = 1.2

    if kind == "shock":
        ops += [P([(-14.4, by + 1.0), (-9.2, by - 3.6), (-4.6, by - 0.2),
                   (-4.6, by + 1.8), (-9.2, by - 1.4), (-14.4, by + 2.4)], "hair"),
                P([(-0.6, by - 0.2), (4.0, by - 4.0), (8.6, by + 0.4),
                   (8.6, by + 2.4), (4.0, by - 1.6), (-0.6, by + 1.8)], "hair")]
    elif kind == "crit":
        ops += [P([(-14.6, by + 3.0), (-9.2, by - 2.8), (-4.4, by + 2.2),
                   (-9.2, by - 0.4)], "hair"),
                P([(-0.8, by + 2.2), (4.0, by - 3.0), (9.0, by + 2.8),
                   (4.0, by - 0.6)], "hair")]
    elif kind in ("angry", "combat", "strain"):
        ops += [P(brow(-9.2, 1.8, 3.0), "hair"), P(brow(4.2, 1.8, 3.0), "hair")]
    elif kind == "hurt":
        ops += [P(brow(-9.2, -1.5, -0.8), "hair"), P(brow(4.2, -1.5, -0.8), "hair")]
    elif kind == "smirk":
        ops += [P(brow(-9.2, 1.1, 1.7), "hair"), P(brow(4.2, -0.2, 2.4), "hair")]
    else:
        ops += [P(brow(-9.2, 1.0, 1.2), "hair"), P(brow(4.2, 1.0, 1.2), "hair")]

    # nariz discreto e orelha
    ops.append(CL([(14.2, -181.4), (15.6, -179.0), (13.8, -178.2)], "skin_sh", 1.5))
    ops.append(CL([(-3.6, -175.8), (1.6, -175.4)], "skin_sh", 1.0))
    ops.append(CF(capsule((10.0, -183.0), (12.6, -180.2), 5.0, 4.0), "skin_hi"))

    my = -177.0
    if kind in ("angry", "crit", "hurt", "strain"):
        ops.append(F([(3.0, my), (8.4, my - 1.3), (11.0, my + 0.2), (8.8, my + 2.6),
                      (4.6, my + 2.4), (3.0, my + 0.8)], "mouth"))
        ops.append(F([(4.6, my + 0.6), (7.6, my + 0.3), (8.4, my + 1.6), (5.3, my + 1.8)],
                     "eye_white"))
    elif kind == "shock":
        ops.append(F(oval(7.0, my + 1.0, 2.6, 3.1), "mouth"))
    elif kind == "smirk":
        ops.append(CL([(3.4, my + 1.0), (7.6, my + 0.2), (10.8, my - 2.2)], "mouth", 2.0))
    elif kind == "dead":
        ops.append(CL([(3.8, my), (8.6, my + 1.5)], "mouth", 1.7))
    else:
        ops.append(CL([(3.4, my + 0.4), (7.6, my + 0.4)], "mouth", 2.0))
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
    # franja curta ACIMA da sobrancelha (v2: subiu 4px; antes cobria a testa
    # inteira e a sobrancelha encostava na franja, virando mascara preta)
    ops += [
        P([(-18.6, -202.2), (-11.2, -203.4), (-13.8, -200.8), (-19.0, -200.4)], "hair"),
        P([(-7.2, -201.8), (0.9, -202.4), (-2.7, -199.6), (-9.0, -200.2)], "hair"),
        P([(2.5, -202.2), (9.6, -201.4), (6.7, -197.8), (1.1, -199.4)], "hair"),
        P([(10.8, -201.0), (17.6, -203.0), (17.4, -199.4), (11.8, -199.6)], "hair"),
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
    # v2: cintura mais estreita e ombro mais largo (silhueta em V, nao "saco")
    gi = [(-27.5, -150.0), (-17.6, -157.2), (-6.2, -159.0), (8.2, -159.0),
          (18.6, -157.0), (28.5, -149.4), (26.6, -140.0), (22.4, -130.0),
          (17.8, -118.0), (15.2, -102.0), (16.4, -92.4), (-16.4, -92.4),
          (-15.2, -102.0), (-17.8, -118.0), (-22.6, -130.0), (-27.0, -140.0)]
    ops = [
        F(gi, "gi"),
        # V do decote com camisa azul
        CFP([(-12.4, -160.6), (0.0, -136.2), (12.4, -160.6), (7.2, -161.4),
             (0.0, -147.4), (-6.9, -159.8)], "blue"),
        CFP([(-13.0, -158.6), (-1.5, -134.2), (1.4, -135.0), (-9.9, -159.2)], "blue_sh"),
        CFP([(13.0, -158.6), (1.4, -134.2), (-1.5, -135.0), (9.9, -159.2)], "blue_sh"),
        # sombra INTERNA do decote (profundidade, nao so contorno)
        CFP([(-8.6, -157.4), (0.0, -145.0), (8.6, -157.4), (0.0, -151.6)], "blue_deep"),
        # faixa
        F([(-19.8, -104.0), (19.8, -104.0), (20.6, -92.0), (-20.6, -92.0)], "blue"),
        F([(-20.6, -95.0), (20.6, -95.0), (20.6, -92.0), (-20.6, -92.0)], "blue_deep"),
        L([(-19.2, -98.6), (19.2, -98.6)], "blue_sh", 1.4),
        L([(-17.0, -102.6), (5.0, -100.2), (-4.2, -101.8)], "blue_hi", 1.6),
        # nó da faixa com sobra caindo (o v1 nao tinha)
        F([(-4.4, -94.0), (4.6, -94.4), (5.2, -88.4), (-5.0, -88.0)], "blue"),
        F([(-3.6, -94.2), (-0.4, -94.4), (-0.8, -88.2), (-4.0, -88.2)], "blue_sh"),
        P([(1.8, -90.0), (6.4, -86.6), (5.0, -82.4), (2.4, -85.8)], "blue"),
        P([(1.8, -90.0), (2.6, -85.6), (1.2, -82.2), (0.4, -85.8)], "blue_sh"),
        AS("gi_sh", 3.6, 5.0),
        AH("gi_hi", -3.2, -3.6),
        # dobras de tecido: ombro->cintura e algumas curtas
        CL([(-22.4, -145.0), (-18.4, -130.0), (-15.6, -112.0), (-14.2, -99.0)], "gi_sh", 1.7),
        CL([(9.2, -152.0), (6.2, -137.0), (4.0, -120.0), (3.0, -106.0)], "gi_sh", 1.4),
        CL([(-8.0, -140.0), (-3.0, -132.0), (1.0, -128.0)], "gi_sh", 1.2),
        CL([(-9.4, -110.0), (-5.0, -121.0)], "gi_sh", 1.2),
        CL([(14.0, -136.0), (10.2, -124.0), (8.4, -116.0)], "gi_sh", 1.1),
        CL([(-16.6, -120.0), (-11.0, -116.0), (-7.0, -117.0)], "gi_hi", 1.0),
        # peitoral: sombra sob a linha do peito
        CL([(-15.8, -143.6), (-6.0, -145.2), (7.0, -144.6), (15.2, -142.0)], "gi_sh", 1.6),
        CL([(-14.2, -146.6), (-5.0, -148.0), (6.0, -147.6), (13.6, -145.2)], "gi_hi", 1.2),
        # PESCOCO por ULTIMO (senao o gi cobre): do queixo ao decote
        F(capsule((0, -171.0), (0, -156.0), 14.4, 17.4), "skin"),
        CF(capsule((0, -168.6), (0, -163.4), 15.0, 16.2), "skin_sh"),
        CL([(-6.4, -160.0), (6.4, -160.0)], "skin_sh", 1.2),
    ]
    return part("torso", J["spine"], ops, bone="spine", z=90)


def _pelvis():
    pants = [(-17.0, -97.0), (17.0, -97.0), (17.4, -89.6), (14.6, -84.0),
             (4.6, -83.0), (0.0, -86.0), (-4.6, -83.0), (-14.6, -84.0), (-17.4, -89.6)]
    ops = [F(pants, "blue"), AS("blue_sh", 3.0, 3.8), AH("blue_hi", -2.4, -3.0),
           CL([(-10.0, -80.2), (-3.0, -82.2)], "blue_sh", 1.3),
           CL([(2.0, -81.8), (9.0, -79.8)], "blue_sh", 1.3)]
    return part("pelvis", J["pelvis"], ops, bone="pelvis", z=80)


def _arm(side: str):
    s = side
    sh, el, wr = J[f"shoulder_{s}"], J[f"elbow_{s}"], J[f"wrist_{s}"]
    out = {}
    # manga CURTA azul: deltoide arredondado, nao um cano cortado
    dx, dy = el[0] - sh[0], el[1] - sh[1]
    Lm = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / Lm, dy / Lm
    cuff = (sh[0] + ux * 17.0, sh[1] + uy * 17.0)
    # v2: capsula com bulge -> ombro mais cheio, cuf mais justo
    sleeve = capsule(sh, cuff, 25.5, 18.5, bulge=0.10)
    ops_s = [F(sleeve, "blue"), AS("blue_sh", 3.0, 3.6), AH("blue_hi", -2.2, -2.6),
             # brilho e sombra ja vem do AS/AH (faixa de borda); aqui so o cuff
             CF(capsule(cuff, (cuff[0] + ux * 2.2, cuff[1] + uy * 2.2), 19.4, 19.0), "blue_deep"),
             CL([(sh[0] - 4.0, sh[1] + 5.0), (cuff[0] - 5.0, cuff[1] + 4.6)], "blue_deep", 1.1)]
    out[f"upper_arm_{s}"] = part(f"upper_arm_{s}", sh, ops_s,
                                bone=f"upper_arm_{s}", z=130 if s == "f" else 60)
    # braço nu: bíceps com bulge, antebraço afinando para o punho
    mid = ((el[0] + sh[0]) / 2, (el[1] + sh[1]) / 2)
    fore = capsule(mid, wr, 18.5, 13.5, bulge=0.09)
    bx, by = wr[0] - el[0], wr[1] - el[1]
    bL = (bx * bx + by * by) ** 0.5
    bux, buy = bx / bL, by / bL
    nx, ny = -buy, bux
    # munhequeira azul mais alta e visivel (v1 era um risco)
    b0 = (wr[0] - bux * 10.2 - nx * 7.4, wr[1] - buy * 10.2 - ny * 7.4)
    b1 = (wr[0] - bux * 10.2 + nx * 7.4, wr[1] - buy * 10.2 + ny * 7.4)
    b2 = (wr[0] - bux * 2.4 + nx * 7.6, wr[1] - buy * 2.4 + ny * 7.6)
    b3 = (wr[0] - bux * 2.4 - nx * 7.6, wr[1] - buy * 2.4 - ny * 7.6)
    ops = [F(fore, "skin"), AS("skin_sh", 1.8, 2.2), AH("skin_hi", -2.4, -2.8),
           # sombra do bíceps: FAIXA fina no lado interno (capsula inteira
           # escurecia o antebraco todo e lia como braco de outra cor)
           SHP(capsule((mid[0] - nx * 4.2, mid[1] - ny * 4.2),
                       (el[0] - nx * 3.0 + bux * 3.0, el[1] - ny * 3.0 + buy * 3.0),
                       9.0, 7.0), "skin_sh"),
           F([b0, b1, b2, b3], "blue"), AS("skin_sh", 2.0, 2.4),
           CF(capsule(((b0[0] + b2[0]) / 2 - 1.0, (b0[1] + b2[1]) / 2 - 1.0),
                      ((b1[0] + b3[0]) / 2 - 1.0, (b1[1] + b3[1]) / 2 - 1.0), 3.0, 3.0), "blue_deep"),
           HI([b0, b2], "blue_hi"),
           # rim light: aro claro na borda iluminada (faz o membro "saltar" a 1x)
           CL([(wr[0] - bux * 9.0 - nx * 6.6, wr[1] - buy * 9.0 - ny * 6.6),
               (el[0] + bux * 2.0 - nx * 5.0, el[1] + buy * 2.0 - ny * 5.0)],
              "skin_hi", 1.6),
           CL([(el[0] + 1.0, el[1] + 9.0), (wr[0] - 1.0, wr[1] - 8.0)], "skin_sh", 1.2)]
    out[f"forearm_{s}"] = part(f"forearm_{s}", el, ops, bone=f"forearm_{s}",
                               z=131 if s == "f" else 61)
    # punho fechado: MAIOR (v1 tinha mao pequena, lia como manopla)
    hand = [(-9.6, -8.8), (0.4, -12.8), (9.4, -8.8), (12.8, 0.6), (8.8, 11.0),
            (-1.4, 12.4), (-10.0, 6.2), (-11.4, -1.6)]
    hand = [(wr[0] + x, wr[1] + y) for x, y in hand]
    ops = [F(hand, "skin"), AS("skin_sh", 2.0, 2.4), AH("skin_hi", -2.4, -2.8),
           # nós dos dedos
           CL([(wr[0] - 5.0, wr[1] + 1.4), (wr[0] - 1.0, wr[1] + 2.6),
               (wr[0] + 3.0, wr[1] + 1.8), (wr[0] + 6.6, wr[1] - 0.8)],
              "skin_sh", 1.3),
           CL([(wr[0] - 4.6, wr[1] + 5.8), (wr[0] + 5.8, wr[1] + 4.0)], "skin_sh", 1.1)]
    out[f"hand_{s}"] = part(f"hand_{s}", wr, ops, bone=f"hand_{s}",
                            z=132 if s == "f" else 62)
    return out


def _leg(side: str):
    s = side
    hip, knee, ankle = J[f"hip_{s}"], J[f"knee_{s}"], J[f"ankle_{s}"]
    out = {}
    # coxa: volume na parte alta, afina no joelho (v1 era cano reto)
    thigh = capsule((hip[0] + (2.6 if s == "f" else -2.6), hip[1]), knee, 27, 19, bulge=0.12)
    out[f"thigh_{s}"] = part(
        f"thigh_{s}", hip,
        [F(thigh, "blue"), AS("blue_sh", 3.4, 4.2), AH("blue_hi", -2.8, -3.2),
         # dobra atras do joelho
         # dobra CURTA atras do joelho (linha longa atravessava a perna toda)
         CL([(hip[0] - 6, hip[1] + 10), (knee[0] - 4, knee[1] - 14)], "blue_sh", 1.5)],
        bone=f"thigh_{s}", z=100 if s == "f" else 70)
    shin = capsule(knee, (ankle[0], ankle[1] - 2), 22, 15, bulge=0.05)
    ops = [F(shin, "blue"), AS("blue_sh", 3.0, 3.8), AH("blue_hi", -2.4, -3.0),
           # topo da bota com elástico
           F([(ankle[0] - 9.2, ankle[1] - 13.0), (ankle[0] + 9.4, ankle[1] - 13.0),
              (ankle[0] + 9.0, ankle[1] - 5.0), (ankle[0] - 8.8, ankle[1] - 5.0)], "blue_sh"),
           L([(ankle[0] - 8.6, ankle[1] - 9.4), (ankle[0] + 9.0, ankle[1] - 9.4)],
             "blue_deep", 1.3),
           CL([(knee[0] + 1, knee[1] + 8), (ankle[0] + 1, ankle[1] - 16)], "blue_hi", 1.2)]
    out[f"shin_{s}"] = part(f"shin_{s}", knee, ops, bone=f"shin_{s}",
                            z=101 if s == "f" else 71)
    # bota: bico mais agudo, solado mais grosso, cano com cadarço
    # sola em ankle+12.0 = y=0 do mundo (chao). O solado claro ocupa o
    # ultimo 1.6px; passar disso fazia o pe penetrar o piso em 2px.
    boot = [(ankle[0] - 10.2, ankle[1] - 12.4), (ankle[0] + 4.6, ankle[1] - 13.6),
            (ankle[0] + 13.2, ankle[1] - 7.0), (ankle[0] + 19.4, ankle[1] + 1.2),
            (ankle[0] + 19.8, ankle[1] + 6.8), (ankle[0] + 16.2, ankle[1] + 10.4),
            (ankle[0] - 9.6, ankle[1] + 10.4), (ankle[0] - 11.2, ankle[1] + 1.6)]
    ops = [F(boot, "blue"), AS("blue_sh", 3.0, 3.6), AH("blue_hi", -2.6, -3.0),
           # solado grosso e claro
           F([(ankle[0] - 10.4, ankle[1] + 6.6), (ankle[0] + 19.4, ankle[1] + 6.6),
              (ankle[0] + 19.8, ankle[1] + 7.8), (ankle[0] + 16.2, ankle[1] + 10.4),
              (ankle[0] - 9.6, ankle[1] + 10.4)], "boot_sole"),
           L([(ankle[0] - 9.8, ankle[1] + 7.4), (ankle[0] + 19.2, ankle[1] + 7.4)],
             "boot_sole_sh", 1.0),
           # cadarço (leitura de bota)
           # (v2) cadarco fino no CANO, nao no bico
           L([(ankle[0] - 7.8, ankle[1] - 11.0), (ankle[0] + 0.6, ankle[1] - 9.6)],
             "lace", 1.4),
           L([(ankle[0] - 8.0, ankle[1] - 8.0), (ankle[0] + 1.0, ankle[1] - 6.6)],
             "lace", 1.3),
           L([(ankle[0] - 7.8, ankle[1] - 5.0), (ankle[0] + 1.4, ankle[1] - 3.8)],
             "lace", 1.2)]
    out[f"foot_{s}"] = part(f"foot_{s}", ankle, ops, bone=f"foot_{s}",
                            z=102 if s == "f" else 72, stroke=3.6)
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
