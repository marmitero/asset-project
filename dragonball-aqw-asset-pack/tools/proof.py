"""Render de inspeção: personagem em 3 tamanhos + silhueta."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image, ImageDraw
from aura.pose import Skeleton, Pose
from aura.rig import ActorRig, load_layers
from aura.parts_goku import build_goku_parts

parts = {k: v.build() for k, v in build_goku_parts().items()}
skel = Skeleton.load('standards/skeleton_humanoid.json')
for s in skel.data['slots']:
    if s['slot'] == 'torso':
        s['bone'] = 'spine'
rig = ActorRig(skel, parts, load_layers('standards/layer_order.json'), skel.data['secondary_chains'], attachments={'face': 'face_neutral'})

sheet = Image.new("RGBA", (1100, 620), (20, 22, 28, 255))
img, _ = rig.render(Pose(), out_size=(512, 512))
sheet.alpha_composite(img, (0, 40))
big = img.resize((512, 512))
# silhueta
sil = Image.new("RGBA", img.size, (0, 0, 0, 0))
a = img.getchannel("A").point(lambda v: 255 if v > 40 else 0)
black = Image.new("RGBA", img.size, (0, 0, 0, 255)); black.putalpha(a)
sheet.alpha_composite(black, (560, 40))
d = ImageDraw.Draw(sheet)
for i, px in enumerate([48, 96, 220]):
    thumb = img.resize((int(512 * px / 512), int(512 * px / 512)), Image.LANCZOS)
    crop = img.copy()
    bb = crop.getbbox()
    thumb2 = img.crop(bb).resize((px // 2, int((bb[3]-bb[1]) * (px/2) / (bb[2]-bb[0]))), Image.LANCZOS)
    sheet.alpha_composite(thumb2, (20 + i * 120, 40 + 460))
d.text((10, 10), "GOKU BASE  |  proof sheet  |  rest pose  |  silhueta", fill=(220, 220, 220))
sheet.convert("RGB").save('/tmp/proof.png')
print("saved")
