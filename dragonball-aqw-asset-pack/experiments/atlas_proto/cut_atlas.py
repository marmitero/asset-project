"""Atlas pintado por IA: recorta a arte gerada nas 29 peças do rig e reanima.

Pipeline:
  1. desenha a pose de repouso do rig (1x, 512) e o alpha de CADA peça
  2. tira o fundo cinza da arte da IA (estimativa de cor por linha)
  3. registra a arte no rig por escala anisotropica do bbox da silhueta
  4. recorta a arte com o alpha de cada peça, fecha o contorno, sobe para 2x
  5. monta PartImage e devolve um rig identico ao vetorial, mas pintado

Nao toca em exports/. Saida em experiments/atlas_proto/out/.
"""
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from aura.core import PartImage, rgba  # noqa: E402
from aura.parts_goku import build_goku_parts  # noqa: E402
from aura.pose import Pose, Skeleton  # noqa: E402
from aura.rig import ActorRig, load_layers  # noqa: E402
from landmark import landmark_register  # noqa: E402

OUT = Path(__file__).resolve().parent / "out"
FRAME = 512
GROUND = 448.0


# ------------------------------------------------------------------ 1. rig
def build_rig():
    parts = {k: v.build() for k, v in build_goku_parts().items()}
    skel = Skeleton.load(ROOT / "standards" / "skeleton_humanoid.json")
    rig = ActorRig(skel, parts, load_layers(ROOT / "standards" / "layer_order.json"),
                   skel.data["secondary_chains"])
    rig.attachments.update({"face": "face_neutral", "hair_front": "hair_front"})
    return skel, rig, parts


def masks_for(rig: ActorRig) -> tuple[dict[str, np.ndarray], tuple]:
    """Alpha de cada slot na pose de repouso, no MESMO pipeline de warp do rig."""
    base_parts = rig.parts
    masks: dict[str, np.ndarray] = {}
    acc = None
    for slot in rig.slots:
        key = rig.attachments.get(slot, slot)   # slot "face" -> chave "face_neutral"
        p = base_parts.get(key)
        if p is None:
            continue
        blank = {k: PartImage(name=k, image=Image.new("RGBA", v.size, (0, 0, 0, 0)),
                              pivot=v.pivot, z=v.z, bone=v.bone)
                 for k, v in base_parts.items()}
        # IMPORTANTE: preservar o alpha original — peca solida != retangulo do bitmap
        sil = Image.new("RGBA", p.size, (255, 255, 255, 0))
        sil.putalpha(p.image.getchannel("A"))
        blank[key] = PartImage(name=key, image=sil, pivot=p.pivot, z=p.z, bone=p.bone)
        rig.parts = blank
        img, _ = rig.render(Pose(), facing=1, zoom=1.0, out_size=(FRAME, FRAME),
                            shadow=False, ground_clamp=False)
        a = np.array(img.getchannel("A"))
        masks[key] = a
        acc = a.copy() if acc is None else np.maximum(acc, a)
    rig.parts = base_parts
    ys, xs = np.where(acc > 20)
    return masks, (xs.min(), ys.min(), xs.max(), ys.max())


# --------------------------------------------------------- 2. matte da IA
def matte(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """RGB + alpha da arte, sem o fundo cinza liso (estimado por linha)."""
    rgb = np.array(Image.open(path).convert("RGB")).astype(np.float32)
    h, w, _ = rgb.shape
    side = max(4, w // 40)
    edge = np.concatenate([rgb[:, :side], rgb[:, -side:]], axis=1)
    bg_row = np.median(edge, axis=1)                       # (h, 3)
    d = np.abs(rgb - bg_row[:, None, :]).max(axis=2)
    alpha = np.clip((d - 8.0) / 26.0, 0.0, 1.0)
    # NOTA: nao "fechar buracos" aqui — os vaos entre as pontas do cabelo sao
    # buracos legitimos e preenche-los borra a silhueta.
    # limpa ruido: maior componente conexa
    m = (alpha > 0.4).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    if n > 1:
        biggest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        keep = (lab == biggest)
        # dilata a area mantida para nao cortar pontas de cabelo soltas
        keep = cv2.dilate(keep.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        alpha = alpha * keep
    return rgb, alpha


# ------------------------------------------------------ 3. registro no rig
def register(rgb: np.ndarray, alpha: np.ndarray, rig_bbox: tuple) -> tuple[np.ndarray, np.ndarray]:
    """Escala anisotropica + translacao para o bbox da silhueta bater com o do rig."""
    h, w, _ = rgb.shape
    ys, xs = np.where(alpha > 0.4)
    src = (xs.min(), ys.min(), xs.max(), ys.max())
    dw, dh = rig_bbox[2] - rig_bbox[0], rig_bbox[3] - rig_bbox[1]
    sw, sh = src[2] - src[0], src[3] - src[1]
    sx, sy = dw / max(sw, 1), dh / max(sh, 1)
    M = np.array([[sx, 0, rig_bbox[0] - src[0] * sx],
                  [0, sy, rig_bbox[1] - src[1] * sy]], np.float32)
    # INTER_AREA: a reducao aqui e ~5x. LANCZOS4 tem ringing e zera o alpha no
    # meio da silhueta, virando buraco/pontinho depois do recorte.
    dst = cv2.warpAffine(rgb, M, (FRAME, FRAME), flags=cv2.INTER_AREA,
                         borderMode=cv2.BORDER_CONSTANT, borderValue=(196, 196, 196))
    dst_a = cv2.warpAffine(alpha, M, (FRAME, FRAME), flags=cv2.INTER_AREA,
                           borderMode=cv2.BORDER_CONSTANT, borderValue=0.0)
    print(f"registro: silhueta IA {sw}x{sh} -> rig {dw}x{dh}  (distorcao x{sx:.3f} y{sy:.3f})")
    return dst, np.clip(dst_a, 0, 1)


# ------------------------------------------------------------ 4. recorte
def make_parts(masks: dict[str, np.ndarray], art: np.ndarray, art_a: np.ndarray,
               skel, rig: ActorRig) -> tuple[dict[str, PartImage], dict]:
    world = skel.solve(Pose())
    outline = rgba("outline")
    pieces: dict[str, PartImage] = {}
    stats = {}
    for slot in rig.slots:
        key = rig.attachments.get(slot, slot)
        p = rig.parts.get(key)
        if p is None or key not in masks:
            continue
        m = (masks[key] > 20).astype(np.uint8)
        if not m.any():
            pieces[slot] = p
            continue
        # ANTES de recortar: erode 1 px. Sem isso a mascara leva uma faixa do
        # contorno escuro da peca VIZINHA, que gira junto com o membro e vira
        # uma linha pontilhada (defeito observado no 1o teste de animacao).
        k = np.ones((3, 3), np.uint8)
        m = cv2.erode(m, k)
        if not m.any():
            pieces[slot] = p
            continue
        # contorno proprio: 1 px de traco na borda da peca erodida
        edge = cv2.dilate(m, k) - m
        a = (m * 255).astype(np.float32) / 255.0 * art_a
        a = np.clip(a * 255, 0, 255)
        ys, xs = np.where(m > 0)
        pad = 3
        x0, y0 = max(0, xs.min() - pad), max(0, ys.min() - pad)
        x1, y1 = min(FRAME, xs.max() + pad), min(FRAME, ys.max() + pad)
        rgb_c = art[y0:y1, x0:x1].astype(np.uint8)
        a_c = a[y0:y1, x0:x1].astype(np.uint8)
        # traco escuro na borda interna (fecha a peca no estilo paper-doll)
        e = edge[y0:y1, x0:x1] > 0
        rgb_c = rgb_c.copy()
        a_c = a_c.copy()
        rgb_c[e] = outline[:3]
        a_c[e] = np.maximum(a_c[e], 200)
        img = Image.fromarray(np.dstack([rgb_c, a_c]))
        # sobe para 2x (a arte da IA tem resolucao sobrando)
        img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
        bone = rig._bone_of(slot)
        w = world.get(bone)
        if not w:
            continue
        wx, wy = FRAME / 2 + w["pos"][0], GROUND + w["pos"][1]
        pivot = ((wx - x0) * 2, (wy - y0) * 2)
        pieces[slot] = PartImage(name=p.name, image=img, pivot=pivot, z=p.z,
                                 bone=p.bone, scale=2)
        stats[slot] = (x1 - x0, y1 - y0)
    return pieces, stats


def build_painted_rig(ai_png: Path):
    skel, rig, _ = build_rig()
    masks, rig_bbox = masks_for(rig)
    rgb, a = matte(ai_png)
    # 1o: caixa da silhueta no enquadramento do rig
    art0, a0 = register(rgb, a, rig_bbox)
    # 2o: alinha as JUNTAS linha a linha (a caixa sozinha nao basta)
    rig_full = np.zeros((FRAME, FRAME), np.uint8)
    for m in masks.values():
        rig_full = np.maximum(rig_full, m)
    art, art_a, cov = landmark_register(art0, a0, rig_full)
    print(f"cobertura do rig apos alinhamento: {cov*100:.1f}%")
    pieces, stats = make_parts(masks, art, art_a, skel, rig)
    rigid = ActorRig(skel, pieces, load_layers(ROOT / "standards" / "layer_order.json"),
                     skel.data["secondary_chains"])
    rigid.attachments.update(rig.attachments)
    print(f"{len(pieces)} pecas recortadas")
    return skel, rigid


if __name__ == "__main__":
    skel, rigid = build_painted_rig(OUT / "ai_painted.jpg")
    img, _ = rigid.render(Pose(), facing=1, zoom=1.0, out_size=(FRAME, FRAME), shadow=False)
    img.save(OUT / "painted_rest.png")
    print("wrote", OUT / "painted_rest.png")
