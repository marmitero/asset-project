"""Gera folhas de contato rápidas para QA visual do primeiro modelo."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image, ImageDraw
from aura.pose import Skeleton
from aura.rig import ActorRig, load_layers
from aura.parts_goku import build_goku_parts
from aura import clips
from aura.render import ClipRenderer, ShowConfig

parts = {k: v.build() for k, v in build_goku_parts().items()}
skel = Skeleton.load('standards/skeleton_humanoid.json')
rig = ActorRig(skel, parts, load_layers('standards/layer_order.json'), skel.data['secondary_chains'])
r = ClipRenderer(rig, skel)

name = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
zoom = float(sys.argv[3]) if len(sys.argv) > 3 else 1.4
cfg = ShowConfig(background='grid', show_hud=False, zoom=zoom)
c = clips.get(name)
r.trail = []
tiles = [r.frame(c, c.frames * i / n, cfg) for i in range(n)]
cols = min(4, n); rows = (n + cols - 1) // cols
sheet = Image.new('RGB', (512 * cols, 512 * rows), (10, 11, 14))
for i, t in enumerate(tiles):
    sheet.paste(t.convert('RGB'), ((i % cols) * 512, (i // cols) * 512))
d = ImageDraw.Draw(sheet); d.text((8, 6), f'{name} — {c.frames}f — {n} amostras', fill=(255, 230, 160))
sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS).save(f'/tmp/sheet_{name}.png')
print(f'/tmp/sheet_{name}.png')
