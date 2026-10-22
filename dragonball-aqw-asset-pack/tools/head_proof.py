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
    pass
faces = sys.argv[1:] or ['neutral']
rig = ActorRig(skel, parts, load_layers('standards/layer_order.json'), skel.data['secondary_chains'])
hidden = {'torso','pelvis','thigh_f','thigh_b','shin_f','shin_b','foot_f','foot_b',
          'upper_arm_f','upper_arm_b','forearm_f','forearm_b','hand_f','hand_b'}
tiles = []
for face in faces:
    p = dict(parts); p['face'] = p[f'face_{face}']
    for k in hidden: p.pop(k, None)
    r = ActorRig(skel, p, load_layers('standards/layer_order.json'), {}, attachments={'face': f'face_{face}'})
    img,_ = r.render(Pose(), out_size=(512,512), shadow=False)
    tiles.append(img.crop((200, 200, 312, 320)).resize((336, 360), Image.NEAREST))
sheet = Image.new('RGB', (336*len(tiles), 400), (24,26,32))
for i,t in enumerate(tiles): sheet.paste(t, (336*i, 20))
d=ImageDraw.Draw(sheet); d.text((6,4), ' / '.join(faces), fill=(230,230,230))
sheet.save('/tmp/heads.png'); print('ok')
