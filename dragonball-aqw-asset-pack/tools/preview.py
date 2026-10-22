import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image
from aura.pose import Skeleton
from aura.rig import ActorRig, load_layers
from aura.parts_goku import build_goku_parts
from aura import clips
from aura.render import ClipRenderer, ShowConfig
from aura.scene import W, H

parts = {k: v.build() for k, v in build_goku_parts().items()}
skel = Skeleton.load('standards/skeleton_humanoid.json')
rig = ActorRig(skel, parts, load_layers('standards/layer_order.json'), skel.data['secondary_chains'])
r = ClipRenderer(rig, skel)
name = sys.argv[1] if len(sys.argv) > 1 else 'idle'
frames_n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
clip = clips.get(name)
cfg = ShowConfig(background='grid', caption=f'{name}', show_timeline=True)
t0 = time.time()
tiles = []
for i in range(frames_n):
    f = clip.frames * i / frames_n
    tiles.append(r.frame(clip, f, cfg))
dt = time.time() - t0
sheet = Image.new('RGB', (W * min(3, frames_n), H * ((frames_n + 2) // 3)), (0, 0, 0))
for i, im in enumerate(tiles):
    sheet.paste(im.convert('RGB'), ((i % 3) * W, (i // 3) * H))
sheet.save(f'/tmp/prev_{name}.png')
print(f'{name}: {len(tiles)} frames em {dt*1000:.0f} ms ({dt/len(tiles)*1000:.1f} ms/frame)')
