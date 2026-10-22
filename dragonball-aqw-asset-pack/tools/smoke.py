import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aura.pose import Skeleton
from aura.rig import ActorRig, load_layers
from aura.parts_goku import build_goku_parts
from aura import clips
from aura.render import ClipRenderer, ShowConfig

parts = {k: v.build() for k, v in build_goku_parts().items()}
skel = Skeleton.load('standards/skeleton_humanoid.json')
rig = ActorRig(skel, parts, load_layers('standards/layer_order.json'), skel.data['secondary_chains'])
r = ClipRenderer(rig, skel)
cfg = ShowConfig(background='grid', show_hud=False)
t0=time.time()
for name in clips.CLIPS:
    c = clips.get(name)
    n = 0
    for i in range(0, c.frames, max(1, c.frames // 6)):
        img = r.frame(c, i, cfg); n += 1
    print(f"{name:16s} {c.frames:3d}f -> {n} ok")
print(f"total {time.time()-t0:.1f}s")
