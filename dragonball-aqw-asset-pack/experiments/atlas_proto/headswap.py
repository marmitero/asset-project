"""Demo: substitui APENAS a cabeca por uma peca gerada isoladamente.

Mostra o contraste com o teste de corpo inteiro: quando a IA recebe um alvo
pequeno e isolado, o resultado e muito melhor e o registro e trivial.
"""
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from aura.core import PartImage, rgba  # noqa: E402
from aura.parts_goku import build_goku_parts  # noqa: E402
from aura.pose import Pose, Skeleton  # noqa: E402
from aura.rig import ActorRig, load_layers  # noqa: E402
from cut_atlas import OUT, matte  # noqa: E402
import normalize  # noqa: E402

FRAME = 512
GROUND = 448.0
NORMALIZE = True


def register_to_box(rgb, a, box, out=FRAME):
    """Escala a peca para preencher exatamente `box` (x0,y0,x1,y1) no canvas."""
    ys, xs = np.where(a > 0.4)
    if not len(ys):
        raise ValueError("alpha vazio")
    sx0, sy0, sx1, sy1 = xs.min(), ys.min(), xs.max(), ys.max()
    bx0, by0, bx1, by1 = box
    sx = (bx1 - bx0) / max(sx1 - sx0, 1)
    sy = (by1 - by0) / max(sy1 - sy0, 1)
    M = np.array([[sx, 0, bx0 - sx0 * sx], [0, sy, by0 - sy0 * sy]], np.float32)
    rim = cv2.warpAffine(rgb, M, (out, out), flags=cv2.INTER_AREA,
                         borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    ra = cv2.warpAffine(a, M, (out, out), flags=cv2.INTER_AREA,
                        borderMode=cv2.BORDER_CONSTANT, borderValue=0.0)
    return rim, np.clip(ra, 0, 1)


def build_headswap(head_png: Path):
    parts = {k: v.build() for k, v in build_goku_parts().items()}
    skel = Skeleton.load(ROOT / "standards" / "skeleton_humanoid.json")
    rig = ActorRig(skel, parts, load_layers(ROOT / "standards" / "layer_order.json"),
                   skel.data["secondary_chains"])
    rig.attachments.update({"face": "face_neutral", "hair_front": "hair_front"})

    # onde fica o conjunto cabeca+franja+rosto na pose de repouso
    keep = {"head", "face_neutral", "hair_front"}
    sandbox = {}
    for k, v in parts.items():
        if k in keep:
            sandbox[k] = v
        else:
            sandbox[k] = PartImage(name=k, image=Image.new("RGBA", v.size, (0, 0, 0, 0)),
                                   pivot=v.pivot, z=v.z, bone=v.bone)
    rig.parts = sandbox
    solo, _ = rig.render(Pose(), facing=1, zoom=1.0, out_size=(FRAME, FRAME),
                         shadow=False, ground_clamp=False)
    box = solo.getbbox()
    print("caixa do conjunto cabeca:", box)

    rgb, a = matte(head_png)
    himg, ha = register_to_box(rgb, a, box)
    # adere a peca a paleta mestra ANTES de compor (evita "colagem")
    if NORMALIZE:
        himg = normalize.apply(himg, ha,
                               ["skin", "skin_sh", "skin_hi", "hair", "hair_sh",
                                "hair_hi", "eye_white", "eye_dark"], 0.8, 1)
    # contorno fechado
    m = (ha > 0.35).astype(np.uint8)
    edge = cv2.dilate(m, np.ones((3, 3), np.uint8)) - m
    rgba_img = np.dstack([himg.astype(np.uint8), (ha * 255).astype(np.uint8)]).copy()
    rgba_img[edge > 0, :3] = rgba("outline")[:3]
    rgba_img[edge > 0, 3] = 255
    # o rig espera pecas @2x (ver PartImage.scale=2 em core.build_part).
    # montar em 512 e entregar 512 faz a peca sair na METADE do tamanho.
    img = Image.fromarray(rgba_img).resize((FRAME * 2, FRAME * 2), Image.LANCZOS)

    world = skel.solve(Pose())
    w = world["head"]
    wx, wy = FRAME / 2 + w["pos"][0], GROUND + w["pos"][1]
    # a imagem e o canvas inteiro (512x512): o pivo e a posicao do osso NO canvas.
    # (subtrair box[0],box[1] aqui deslocava a cabeca para fora do lugar)
    pivot = (wx * 2, wy * 2)      # pivo tambem @2x
    head_part = PartImage(name="head", image=img, pivot=pivot, z=110, bone="head")

    # reanexa tudo e troca o conjunto cabeca pela peca unica
    rig.parts = dict(parts)
    rig.parts["head"] = head_part
    for k in ("face_neutral", "hair_front"):
        v = parts[k]
        rig.parts[k] = PartImage(name=k, image=Image.new("RGBA", v.size, (0, 0, 0, 0)),
                                 pivot=v.pivot, z=v.z, bone=v.bone)
    rig.attachments.pop("face", None)
    rig.attachments.pop("hair_front", None)
    return skel, rig


if __name__ == "__main__":
    skel, rig = build_headswap(OUT / "ai_head.jpg")
    img, _ = rig.render(Pose(), facing=1, zoom=1.0, out_size=(FRAME, FRAME), shadow=False)
    img.save(OUT / "headswap_rest.png")
    print("wrote", OUT / "headswap_rest.png")
