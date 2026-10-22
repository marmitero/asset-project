"""Renderiza a pose de repouso do rig como referencia para a IA repintar."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from PIL import Image, ImageDraw  # noqa: E402

from aura.parts_goku import build_goku_parts  # noqa: E402
from aura.pose import Pose, Skeleton  # noqa: E402
from aura.rig import ActorRig, load_layers  # noqa: E402

OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)


def build_rig():
    parts = {k: v.build() for k, v in build_goku_parts().items()}
    skel = Skeleton.load(ROOT / "standards" / "skeleton_humanoid.json")
    rig = ActorRig(skel, parts, load_layers(ROOT / "standards" / "layer_order.json"),
                   skel.data["secondary_chains"])
    return skel, rig


if __name__ == "__main__":
    skel, rig = build_rig()
    # rosto e franja sao "attachments": sem isso o rig renderiza cabeca vazia
    # e a IA le a silhueta como se fosse de costas (aconteceu no 1o teste)
    rig.attachments.update({"face": "face_neutral", "hair_front": "hair_front"})
    # repouso absoluto: sem pose, sem sombra, sem fundo
    body, _ = rig.render(Pose(), facing=1, zoom=1.0, out_size=(512, 512), shadow=False)
    bbox = body.getbbox()
    print("bbox do personagem:", bbox, "altura:", bbox[3] - bbox[1])
    body = body.crop(bbox)
    # amplia para 3x com nearest nao: LANCZOS para a IA ver forma limpa
    scale = 1000 / body.height
    big = body.resize((int(body.width * scale), 1000), Image.LANCZOS)
    # monta sobre fundo cinza claro uniforme, com margem
    pad = 60
    ref = Image.new("RGB", (big.width + pad * 2, big.height + pad * 2), (200, 200, 200))
    ref.paste(big, (pad, pad), big)
    ref.save(OUT / "rig_rest_reference.png")
    print("wrote", OUT / "rig_rest_reference.png", ref.size)
