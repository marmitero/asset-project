# TOOLS

Pipeline do projeto AURA. Ainda em construção: a Fase 1 entrega apenas validação de padrões e benchmark.

## Disponível

| Ferramenta | O que faz |
|---|---|
| `validate_standards.py` | Valida JSONs de `standards/` e `production/`: IDs, ossos, slots, camadas, clipes, cores, manifesto. |
| `benchmark_render.py` | Mede o custo do pipeline de warp/composição (OpenCV + Pillow). Não grava arquivos. |

```bash
python3 tools/validate_standards.py
python3 tools/benchmark_render.py --parts 24 --frames 120
```

## Planejado (Fase 2)

```
tools/
├── rig/          skeleton.py, transform.py, ik.py, spring.py
├── render/       shapes.py, shading.py, stroke.py, parts.py, composer.py, scene.py
├── anim/         easing.py, timeline.py
├── export/       sheet.py, atlas.py, gif.py, apng.py
├── validate/     validate.py, metrics.py
├── pack/         manifest.py
└── cli.py        build / preview / validate / pack
```

## Dependências

```
Pillow==13.0.0
numpy==2.4.6
opencv-python-headless==5.0.0
```

Sem ffmpeg, cairo, Inkscape ou Blender. Previews em GIF (25 fps) e APNG (60 fps).
