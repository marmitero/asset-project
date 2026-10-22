# 13 — PIPELINE E FERRAMENTAS
**Projeto AURA · v1.0.0**
Auditoria real de capacidades, arquitetura do pipeline, orçamento de gerações e protocolo de sessão.

---

## 1. Auditoria de capacidades (verificada em 2026-10-22)

| Capacidade | Ferramenta | Status | Observação |
|---|---|---|---|
| Geração de imagem | `generate_image` (plataforma) | ✅ | usada só para concept/backdrop |
| Rasterização e composição | Python 3.11.2 + **Pillow 13.0.0** | ✅ | supersampling, alpha, GIF/APNG |
| Álgebra/máscaras | **NumPy 2.4.6** | ✅ | recorte, dilatação, blending |
| Warp/transformação | **OpenCV 5.0.0 (headless)** | ✅ | `warpAffine` ~0,75 ms/peça |
| Conversão de formato | **ImageMagick 6.9.11-60** | ✅ | GIF, PNG, montagem |
| Automação | Node 22.22.3 | ✅ | opcional |
| Git / GitHub | git + gh | ✅ | versionamento e PR |
| **ffmpeg** | — | ❌ | sem MP4; usar APNG/GIF |
| **cairo / skia** | — | ❌ | `skia-python` falha por `libEGL.so.1`; pipeline usa Pillow + OpenCV |
| **cairo / cairosvg** | — | ❌ | sem SVG rasterizado nativo |
| **Inkscape** | — | ❌ | idem |
| **Blender / Spine** | — | ❌ | não há rig de terceiros |
| **Fontes de fantasia** | — | ❌ | DejaVu como placeholder |

**Conclusão:** o pipeline é **Python + Pillow + NumPy + OpenCV headless**, sem dependências externas de arte. É compatível com a decisão D1 (vector-first) e não bloqueia nada essencial.

### 1.1 Benchmark medido (2026-10-22, 1 núcleo)
Cena sintética: 24 peças de 200×300 px, canvas 512².

| Abordagem | Tempo/frame | Viável? |
|---|---|---|
| Pillow puro, 4× supersample | ~2.050 ms | ❌ |
| Pillow, 2× com peças recortadas | ~500 ms | ⚠️ |
| OpenCV `warpAffine` + Pillow `alpha_composite`, 2× | **~57 ms (17 fps)** | ✅ |
| Encode GIF 48 frames @25 fps | ~0,15 s | ✅ |
| Encode APNG 60 frames @60 fps | ~0,57 s | ✅ |

Consequência: peças estáticas são rasterizadas em 4× uma única vez; a animação transforma em **2×** e reduz para 1× com `INTER_AREA`. Um clipe de 96 frames renderiza em ~5 s; os 18 GIFs em menos de 1 minuto de CPU.

### 1.1 Limitações que o pipeline assume
- Sem GPU: renders são CPU-bound; medido em ~57 ms/frame 512² com 24 peças (2×, OpenCV).
- Sem vetorização nativa: formas são definidas em código (Bézier/polígonos) e rasterizadas com supersampling 4×.
- GIF com alpha binário: previews de alpha usam APNG.
- Sem MP4: documentação de vídeo fica como opcional.

---

## 2. Arquitetura do pipeline

```
 definitions/            (código: formas, paletas, partes)
        │
        ▼
 tools/rig/  ──► skeleton.json, rig.json
        │
        ▼
 tools/anim/ ──► clipes (keys 24 fps) + easing + IK + spring
        │
        ▼
 tools/render/ ──► rasteriza peças (4×) ──► compõe frame (512²)
        │
        ├──► tools/export/ ──► PNG, spritesheet, atlas, GIF, APNG
        └──► tools/validate/ ──► métricas e QA
        │
        ▼
 exports/ + production/ + asset_manifest.json
```

### 2.1 Módulos previstos

| Módulo | Responsabilidade |
|---|---|
| `tools/rig/skeleton.py` | ossos, hierarquia, rest pose, limites |
| `tools/rig/transform.py` | matrizes 2D, world/local, espelhamento |
| `tools/rig/ik.py` | IK de 2 ossos, foot planting |
| `tools/rig/spring.py` | secundárias (cabelo, capa, cauda) |
| `tools/anim/easing.py` | curvas da biblioteca |
| `tools/anim/timeline.py` | tracks, sampling, blend, eventos |
| `tools/render/shapes.py` | Bézier, polígonos, máscaras |
| `tools/render/shading.py` | cel-shading, recorte de sombra, rim light |
| `tools/render/stroke.py` | contorno por dilatação de alpha |
| `tools/render/parts.py` | peças: camadas, paleta, máscaras |
| `tools/render/composer.py` | montagem do actor, ordem de camadas |
| `tools/render/scene.py` | cena de validação (fundo, dummy, overlays) |
| `tools/export/sheet.py` | spritesheets |
| `tools/export/atlas.py` | atlas + JSON |
| `tools/export/gif.py` | GIF 25 fps, paleta, labels |
| `tools/export/apng.py` | APNG 60 fps |
| `tools/validate/validate.py` | integridade estrutural |
| `tools/validate/metrics.py` | gap, slip, seam, jitter |
| `tools/pack/manifest.py` | manifesto, checksums |
| `tools/cli.py` | `aura build / preview / validate / pack` |

### 2.2 CLI

```bash
python -m tools.cli build   characters/canonical_heroes/goku/base
python -m tools.cli preview --asset goku_base --clips idle,walk,run --fps 25
python -m tools.cli validate --all
python -m tools.cli pack --atlas 2048
```

---

## 3. Modelo de peça (vector-first)

Uma peça é descrita em código:

```python
Part(
    id="torso",
    layers=[
        Fill(path=bezier(...), color="gi_orange_base"),
        ShadowMask(path=bezier(...), color="gi_orange_shadow"),
        Highlight(path=bezier(...), color="gi_orange_highlight"),
        Detail(strokes=[...], color="outline_inner"),
    ],
    stroke=3.0,
    masks=["cloth_primary"],
)
```

- `path` em coordenadas locais da peça; pivô no centro da junta.
- `ShadowMask` é recortado pelo alpha da peça (nunca vaza).
- Contorno = dilatação do alpha em `stroke/2`, composto atrás; garante espessura uniforme.
- Render em 4× → downsample LANCZOS 512².
- Paleta vem de `palette_master.json`; trocar paleta regenera a peça inteira (variantes de cor).

### 3.1 Regras de determinismo
- Nenhum uso de `random` sem seed fixa (`seed = hash(asset_id)`).
- Ordem de desenho por `layer_order.json`, nunca por ordem de dict.
- Arredondamento de ângulos a 4 casas antes do render.
- Versão do renderizador incluída nos metadados; mudança de versão invalida previews.

---

## 4. Estrutura real do repositório

```
dragonball-aqw-asset-pack/
  README.md · VERSION.md · LICENSE_NOTES.md · asset_manifest.json
  docs/            19 documentos + matrix/
  standards/       JSON + schemas
  references/      paletas, pranchas, folhas
  characters/      parts, rigs, animations, previews
  equipment/ enemies/ pets/ skills/ environments/ ui/
  exports/         png, spritesheets, atlases, metadata, previews
  production/      ledger, backlog, registry, continuity, reports
  examples/        cenas de integração
  tools/           pipeline
```

---

## 5. Pipeline de produção por asset

```
1. PLANNED       → entra no backlog com ID
2. DEFINE        → forma/paleta/código da peça
3. GENERATE      → render das peças + montagem
4. PROCESS       → normalização de alpha, pivô, máscaras
5. ANIMATE       → clipes e eventos
6. VALIDATE      → métricas + GIF
7. REVIEW        → rubrica
8. EXPORT        → png/sheet/atlas/metadata
9. REGISTER      → manifesto + ledger + relatório
10. APPROVED
```

---

## 6. ADR-0006 — Orçamento de gerações e definição de sessão

O master-prompt limita a **10 gerações de imagem por sessão**. O pipeline atual quase não usa geração de imagem (D1/D2). Para não transformar a regra em teatro nem ignorá-la:

- **Sessão de produção** = unidade de trabalho com objetivo e relatório (não necessariamente um dia).
- **Orçamento de imagem**: 10 chamadas por sessão, 6–8 para novos conceitos/backdrops, 2–4 reservadas. Se a sessão não usa imagem, registra `0/10`.
- **Trabalho de rig/código/documentação** não consome orçamento de imagem.
- O ledger registra os dois números separadamente: `image_generations` e `engineering_sessions`.
- Nenhuma sessão pode declarar conclusão sem relatório e sem atualizar o estado.

---

## 7. Ledger e continuidade

### 7.1 `production/generation_ledger.json`
```json
{
  "sessions": [
    {
      "id": "S01",
      "date": "2026-10-22",
      "phase": "1 - Documentation",
      "objective": "Visual Bible + standards",
      "image_generations": {"planned": 0, "executed": 0, "reserved": 0},
      "assets_created": [],
      "assets_approved": [],
      "assets_rejected": [],
      "notes": "documentação completa, sem geração de imagem"
    }
  ]
}
```

### 7.2 `production/continuity_state.json`
```json
{
  "project": "dragonball-aqw-asset-pack",
  "current_phase": "PHASE_2_FIRST_MODEL",
  "last_completed_session": "S01",
  "next_session": "S02",
  "matrix_version": "0.0.0",
  "matrix_frozen": false,
  "approved_assets": [],
  "pending_assets": ["DB_CHAR_HERO_GOKU_BASE"],
  "blocked_assets": [],
  "known_issues": [],
  "next_priorities": ["tools/rig", "humanoid_male_a", "goku base parts"]
}
```

Ao retomar: ler README → Visual Bible → spec técnica → continuidade → último relatório → backlog. Nunca recomeçar do zero.

---

## 8. Build e empacotamento

| Comando | Saída |
|---|---|
| `aura build` | partes + rig + clipes validados |
| `aura preview` | GIF/APNG por clipe |
| `aura validate` | relatórios JSON + exit code |
| `aura pack` | atlas, manifesto, checksums, zip |

- Build é incremental (hash de input).
- `aura pack` falha se qualquer asset em `exports/` não estiver `APPROVED`.
- Checksums em `exports/checksums.sha256`.

---

## 9. Versionamento e branches

- `main` = estado estável do pack.
- Branch de produção por fase.
- Commits pequenos e descritivos: `feat(rig): humanoid_male_a rest pose`.
- Assets binários grandes só em `exports/` e com Git LFS quando necessário (documentar).
- Nada de `.psd`, cache ou render intermediário no repositório.

---

## 10. Riscos operacionais

| Risco | Mitigação |
|---|---|
| Render CPU lento | cache por hash; previews sob demanda; render em lote |
| Perda de contexto | continuidade + relatórios + este doc |
| Dependência de Pillow 13 | `requirements.txt` com versões pinadas |
| Divergência de preview | previews geradas pelo mesmo commit, com hash |
| Regressão visual | diff de silhueta + re-render do pacote G3 |
| Sem ffmpeg | APNG/GIF; MP4 documentado como opcional |

---

## 11. `requirements.txt` (pinado)

```
Pillow==13.0.0
numpy==2.4.6
```

Instalação no ambiente: `pip install --break-system-packages -r requirements.txt`
(Ambiente gerenciado externamente; usar `--break-system-packages` ou venv.)
