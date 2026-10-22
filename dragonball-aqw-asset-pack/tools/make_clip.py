import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aura.pose import Skeleton
from aura.rig import ActorRig, load_layers
from aura.parts_goku import build_goku_parts
from aura import clips
from aura.render import ClipRenderer, ShowConfig, clip_to_gif_frames
from aura.export import save_gif

parts = {k: v.build() for k, v in build_goku_parts().items()}
skel = Skeleton.load('standards/skeleton_humanoid.json')
rig = ActorRig(skel, parts, load_layers('standards/layer_order.json'), skel.data['secondary_chains'])
r = ClipRenderer(rig, skel)
name = sys.argv[1] if len(sys.argv) > 1 else 'idle'
out = sys.argv[2] if len(sys.argv) > 2 else f'/tmp/{name}.gif'
clip = clips.get(name)
cfg = ShowConfig(background='grid', caption=name, show_hud=bool(int(sys.argv[3]) if len(sys.argv)>3 else 1))
t0=time.time()
rc = clip_to_gif_frames(clip, r, cfg)
save_gif(rc.frames, out, duration_ms=int(1000/25), loop=clip.loop)
print(f'{name}: {len(rc.frames)} frames, {time.time()-t0:.1f}s, {Path(out).stat().st_size//1024} KB')
