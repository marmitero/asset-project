"""Exportação: GIF, APNG, spritesheet e atlas JSON."""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image

from aura.render import BASE_FPS, GIF_FPS, RenderedClip


def _quantize(frames: list[Image.Image], colors: int = 200) -> list[Image.Image]:
    """Quantiza com paleta GLOBAL para evitar cintilação entre frames."""
    if not frames:
        return []
    # paleta a partir dos frames amostrados (evita custo de 96x quantize)
    sample_idx = list(range(0, len(frames), max(1, len(frames) // 8)))[:8]
    strip = Image.new("RGB", (frames[0].width, frames[0].height * len(sample_idx)))
    for i, idx in enumerate(sample_idx):
        strip.paste(frames[idx].convert("RGB"), (0, i * frames[0].height))
    pal = strip.quantize(colors=colors, method=Image.MEDIANCUT, dither=Image.NONE)
    out = []
    for f in frames:
        out.append(f.convert("RGB").quantize(palette=pal, dither=Image.NONE))
    return out


def save_gif(frames: list[Image.Image], path: str | Path, duration_ms: int | None = None,
             fps: int = GIF_FPS, loop: bool = True, colors: int = 200) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if duration_ms is None:
        duration_ms = int(round(1000 / fps))
    q = _quantize(frames, colors)
    # disposal=1 + optimize: apenas as diferenças entre frames vão para o arquivo
    q[0].save(path, save_all=True, append_images=q[1:], duration=duration_ms,
              loop=0 if loop else 1, optimize=True, disposal=1)
    return path


def save_apng(frames: list[Image.Image], path: str | Path,
              duration_ms: int | None = None, fps: int = 60, loop: bool = True) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if duration_ms is None:
        duration_ms = int(round(1000 / fps))
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=duration_ms,
                   loop=0 if loop else 1, disposal=1, blend=0)
    return path


def save_spritesheet(frames: list[Image.Image], path: str | Path, columns: int = 8,
                     meta: dict | None = None) -> Path:
    """Spritesheet power-of-two quando possível, com JSON de atlas ao lado."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not frames:
        return path
    fw, fh = frames[0].size
    cols = min(columns, len(frames))
    rows = math.ceil(len(frames) / cols)
    sheet = Image.new("RGBA", (fw * cols, fh * rows), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.alpha_composite(f, ((i % cols) * fw, (i // cols) * fh))
    sheet.save(path)
    data = {
        "image": path.name,
        "frame_width": fw, "frame_height": fh,
        "columns": cols, "rows": rows, "count": len(frames),
        "frames": [{"index": i, "x": (i % cols) * fw, "y": (i // cols) * fh,
                    "w": fw, "h": fh} for i in range(len(frames))],
    }
    if meta:
        data.update(meta)
    Path(str(path).rsplit(".", 1)[0] + ".json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def save_contact_sheet(frames: list[Image.Image], path: str | Path, columns: int = 6,
                       thumb: float = 0.5, label: str = "") -> Path:
    from PIL import ImageDraw
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not frames:
        return path
    tw, th = int(frames[0].width * thumb), int(frames[0].height * thumb)
    rows = math.ceil(len(frames) / columns)
    sheet = Image.new("RGB", (tw * columns, th * rows + 20), (18, 20, 26))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(frames):
        sheet.paste(f.convert("RGB").resize((tw, th), Image.LANCZOS),
                    ((i % columns) * tw, (i // columns) * th + 20))
        d.text(((i % columns) * tw + 4, (i // columns) * th + 24), str(i),
               fill=(255, 210, 120))
    d.text((4, 5), label, fill=(220, 226, 236))
    sheet.save(path)
    return path


def export_clip(rc: RenderedClip, out_dir: str | Path, gif: bool = True,
                apng: bool = False, sheet: bool = True, contact: bool = False,
                loop: bool = True, prefix: str = "", suffix: str = "") -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{prefix}{rc.name}{suffix}"
    info = {"name": rc.name, "frames": len(rc.frames),
            "duration_ms": rc.duration_ms, "files": []}
    if gif:
        p = save_gif(rc.frames, out_dir / f"{stem}.gif",
                     duration_ms=int(round(1000 / GIF_FPS)), loop=loop)
        info["files"].append({"type": "gif", "path": str(p),
                              "bytes": p.stat().st_size})
    if apng:
        p = save_apng(rc.frames, out_dir / f"{stem}.png", loop=loop)
        info["files"].append({"type": "apng", "path": str(p),
                              "bytes": p.stat().st_size})
    if sheet:
        p = save_spritesheet(rc.frames, out_dir / f"{stem}_sheet.png",
                             meta={"clip": rc.name, "fps": BASE_FPS})
        info["files"].append({"type": "sheet", "path": str(p),
                              "bytes": p.stat().st_size})
    if contact:
        p = save_contact_sheet(rc.frames, out_dir / f"{stem}_contact.png",
                              columns=6, thumb=0.42, label=rc.name)
        info["files"].append({"type": "contact", "path": str(p),
                              "bytes": p.stat().st_size})
    return info
