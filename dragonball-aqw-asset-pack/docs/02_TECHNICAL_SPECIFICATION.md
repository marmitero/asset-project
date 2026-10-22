# 02 — TECHNICAL SPECIFICATION
**Projeto AURA · v1.0.0**
Especificação normativa de canvas, coordenadas, resolução, exportação, metadados e orçamento de performance.

---

## 1. Princípios

1. **Engine-agnóstico.** PNG + JSON são a fonte de verdade. `.tscn`, `.prefab`, `.anim` são exemplos, nunca a entrega principal.
2. **Determinismo.** O mesmo rig + timeline produz pixels idênticos em qualquer máquina com a mesma versão do renderizador.
3. **Escala potência de 2.** Tudo que vira atlas mede 512, 1024, 2048.
4. **Alpha verdadeiro.** Nada de fundo fingido, chroma key ou máscara retangular.
5. **Metadados exatos.** Se o JSON diz 64×92, o PNG tem 64×92.

---

## 2. ADR-0002 — Sistemas de coordenadas e escala

### 2.1 Espaços

| Espaço | Origem | Eixo X | Eixo Y | Unidade | Onde aparece |
|---|---|---|---|---|---|
| **World** | ground center do personagem | + direita (frente) | **+ para cima** | px @1× | documentos, física, gameplay |
| **Rig local** | junta do osso | + ao longo do osso (repouso) | + perpendicular | px @1× | arquivos de rig |
| **Image** | canto superior esquerdo | + direita | **+ para baixo** | px | PNG, spritesheet, atlas, pivôs de imagem |
| **UV** | canto superior esquerdo | + direita | + baixo | 0–1 | atlas JSON |

**Conversão:** `image_y = ground_y − world_y`; `world_y = ground_y − image_y`.
O renderizador faz a conversão; nenhum asset de arte “pensa” em y-down.

### 2.2 Escala canônica
- `1 unidade = 1 px` a **1×**.
- Adulto heroico = **220 px** = 2,20 m no mundo do jogo → **100 px/m**.
- `pixels_per_unit = 100` no metadata (compatível com engines que usam metros).
- Gravidade de referência: `9,8 m/s² = 980 px/s²`.
- Velocidade de caminhada: **140 px/s** (1,4 m/s). Corrida: **340 px/s** (3,4 m/s).
- Nenhum asset é autorado abaixo de 2× e reduzido; a fonte é sempre 4× supersample do alvo de render.

### 2.3 Canvas de personagem

| Propriedade | Valor |
|---|---|
| Canvas de render | **512 × 512 px** |
| Centro X (root) | **256** |
| Linha de chão (world y=0) | **image y = 448** |
| Altura de personagem | 220 px (cabeça em y=228) |
| Headroom para armas/capas/asas | 228 px acima da cabeça |
| Margem inferior | 64 px |
| Supersampling | **4× na peça estática** (render único) · **2× no frame animado** (warp + downsample) |
| Padding de segurança interno | 8 px em todas as bordas |

Personagens maiores que 220 px (bosses, Oozaru) usam canvas **1024×1024** com a mesma linha de chão em `y = 896` e a mesma origem de chão (512, 896).

### 2.4 Conversão de escalas

| Escala | Canvas | Altura do personagem | Uso |
|---|---|---|---|
| 1× | 512² | 220 px | preview de jogo, GIF |
| 2× | 1024² | 440 px | atlas de alta densidade, retina |
| 4× (fonte) | 2048² | 880 px | master de peça (render único) |

---

## 3. Resoluções por categoria

| Categoria | Canvas / frame | Escala de export | Observação |
|---|---|---|---|
| Personagem jogável | 512² | 1× e 2× | 29 slots |
| Boss gigante | 1024² (ou 1536²) | 1× e 2× | escala própria |
| Pet | 256² | 1× e 2× | 1/3–1/2 do player |
| Inimigo comum | 512² | 1× | pode ser 384² se pequeno |
| Retrato de HUD | 256×256 | 1× | cabeça + ombros |
| Ícone de skill/item | 128×128 | export 64/128/256 | margem segura 12 px |
| Frame de VFX pequeno | 256² | 1× | projétil, impacto |
| Frame de VFX grande | 512² | 1× | explosão, beam |
| Camada de cenário | 1920×1080 | 1× | 3 camadas por mapa |
| Tile de chão | 256×256 | 1× | tileável, costura zero |
| Prop | variável, múltiplo de 8 | 1× | âncora no chão |
| Elemento de UI | 9-slice base 64 px | 1× e 2× | insets em JSON |
| Fonte de UI | vetor/ttf externa | — | não embutir texto |

**Regra de ouro:** ícones são exportados em 3 tamanhos a partir do master 512²; nunca desenhar em 64 px.

---

## 4. Alpha, cor e bordas

- Formato: **PNG RGBA 8 bits/canal**, alpha **straight** (não premultiplicado).
- Perfil: sRGB, sem ICC embutido.
- Borda: anti-alias por supersampling; **proibido** halo de cor de fundo. A cor dos pixels semitransparentes deve ser a cor local da arte (não branco/preto).
- **Alpha bleed:** antes de empacotar em atlas, extrudar 2 px de cor sob alpha 0 para evitar linha escura ao filtrar.
- Não usar: JPEG, WebP com perdas, paleta indexada (exceto GIF de preview), fundo branco/preto.
- Pixel “quase transparente” (alpha 1–8) é removido para evitar franja em ferramentas antigas.

---

## 5. Recorte, pivô e alinhamento

### 5.1 Regras
- Peças são exportadas **no canvas completo do personagem** (512²) ou **recortadas com offset** — nunca “centralizadas por bounding box”.
- Se recortada, o metadata guarda:
  - `trim`: `{x, y, w, h}` no canvas original;
  - `pivot_px`: coordenada **na imagem recortada**;
  - `pivot_canvas_px`: coordenada no canvas original (fonte de verdade).
- Um pivô pode cair **fora** da imagem recortada (ex.: cabo de arma). O schema permite valores negativos.
- Arredondamento: pivôs em **inteiros** de px @1×, com resolução mínima de 0,25 px no rig. Export final arredonda para inteiro.
- Nenhuma peça é redimensionada após autorada; escala só no rig (`scale` de slot), com `nearest`/`lanczos` declarado.

### 5.2 Pivôs obrigatórios (nomes fixos)
`neck`, `shoulder_f`, `shoulder_b`, `elbow_f`, `elbow_b`, `wrist_f`, `wrist_b`, `hip_f`, `hip_b`, `knee_f`, `knee_b`, `ankle_f`, `ankle_b`, `toe_f`, `toe_b`, `grip`, `root`, `cape_base`, `hair_base`.

### 5.3 Ordem de camadas
Fonte única: `standards/layer_order.json`. Valores:

| z | slot |
|---|---|
| 0 | `shadow` |
| 10 | `pet` |
| 20 | `aura_back` |
| 30 | `cape` |
| 31 | `wings` |
| 40 | `hair_back` |
| 50 | `weapon_back` |
| 70 | `thigh_b` |
| 71 | `shin_b` |
| 72 | `foot_b` |
| 80 | `pelvis` |
| 90 | `torso` |
| 92 | `upper_arm_b` |
| 93 | `forearm_b` |
| 94 | `hand_b` |
| 100 | `thigh_f` |
| 101 | `shin_f` |
| 102 | `foot_f` |
| 110 | `head` |
| 111 | `face` |
| 115 | `hair_front` |
| 116 | `helm` |
| 120 | `shoulders` |
| 130 | `upper_arm_f` |
| 131 | `forearm_f` |
| 132 | `hand_f` |
| 140 | `weapon_f` |
| 150 | `attack_fx` |
| 160 | `aura_front` |

> **21 camadas canônicas** do master-prompt §7.1 + **8 extensões** (`shadow`, `pet`, `aura_back`, `wings`, `face`, `attack_fx`, `aura_front`) + separação de `hair_front`/`helm` = **29 slots de render**. As 21 canônicas permanecem a espinha dorsal; as extensões são opcionais e declaradas.

---

## 6. Spritesheets e atlas

### 6.1 Spritesheet
- Células **uniformes**; célula = canvas da categoria (512², 256² etc.).
- Grade máxima **8 colunas**; linhas ilimitadas até 2048 px de altura.
- Ordem de leitura: esquerda→direita, topo→baixo.
- Padding entre células: **0 px** (a célula já inclui margem de 8 px) — atlas usa padding próprio.
- Arquivo: `PNG` + `.json` irmão com `frame_count`, `cell_w`, `cell_h`, `columns`, `fps`, `loop`.
- Animações longas (> 64 frames) são exportadas em múltiplas sheets numeradas `_part01`, `_part02`.

### 6.2 Atlas
- Tamanho: **2048×2048** padrão; 1024² para UI e ícones.
- Padding entre sprites: **4 px @1× (8 px @2×)**; extrude 2 px.
- Algoritmo: MaxRects/skyline estável (ordem determinística por ID) para diffs reproduzíveis.
- Metadados: JSON hash com `frames {name: {frame{x,y,w,h}, rotated, trimmed, spriteSourceSize, sourceSize, pivot}}`.
- Atlas nunca contém peças de rigs diferentes no mesmo arquivo (facilita update parcial).

### 6.3 Convenção de nomes de frame
`<asset_id>__<clip>__<frame:04d>.png` — ex.: `DB_CHAR_HERO_GOKU_BASE__run__0012.png`.

---

## 7. Animação — formato de dados

### 7.1 Autoria e amostragem
- Keys em **24 fps** (`fps_base = 24`), tempo em frames inteiros.
- Render de preview e bake em **60 fps** (`fps_sample = 60`).
- Duração de clipe em frames de base; conversão `ms = frames / 24 × 1000`.
- Eventos no frame de base, com offset opcional em frames de amostragem.

### 7.2 Schema
Ver `standards/animation.schema.json`. Estrutura resumida:

```json
{
  "clip": "attack_light_1",
  "fps_base": 24,
  "fps_sample": 60,
  "duration_frames": 18,
  "loop": false,
  "root_motion": false,
  "tracks": {
    "shoulder_f": { "rotation": [[0, 0, "ease_in_out"], [4, -62, "ease_out"], [6, 74, "ease_out_quad"], [18, 0, "ease_in_out"]] },
    "root": { "position": [[0, [0,0], "linear"], [6, [8,0], "ease_out"]] }
  },
  "events": [
    {"frame": 6, "type": "hit_frame", "payload": {"damage_type": "physical"}},
    {"frame": 6, "type": "vfx_emit", "payload": {"id": "DB_VFX_SLASH_01", "socket": "weapon_f"}}
  ]
}
```

### 7.3 Tipos de track
`rotation` (graus), `position` (px), `scale` ([sx, sy]), `alpha` (0–1), `attachment` (string), `visible` (bool).

### 7.4 Convenções
- Rotação em **graus**, sentido **horário positivo** na tela, `0` = orientação de repouso do osso.
- Interpolação padrão: **cúbica com tangentes Catmull-Rom**; `ease` por segmento sobrescreve.
- `linear` é proibido em membros (permitido só em eixos mecânicos, ex.: plataforma).
- Loop: o frame `duration` é idêntico ao frame `0` em pose (não é renderizado; serve de fechamento).

### 7.5 Saídas por clipe

| Saída | Formato | Uso |
|---|---|---|
| Timeline | JSON | runtime skeletal |
| Preview | GIF 25 fps | validação visual |
| Preview alpha | APNG 60 fps | inspeção de borda |
| Spritesheet | PNG + JSON | fallback baked |
| Frames | PNG individuais | debug, VFX, atlas |
| Thumbnail | PNG 256² | catálogo/documentação |

---

## 8. Metadados

### 8.1 Campos obrigatórios por asset
`asset_id`, `name`, `category`, `subcategory`, `version`, `status`, `session`, `created_at`, `files[]`, `dimensions`, `pivot`, `layer`, `rig_compat`, `palette_ref`, `tags`, `license_note`.

### 8.2 Campos obrigatórios por personagem
`rig`, `body_type`, `height_px`, `continuity`, `form`, `parts[]`, `animations[]`, `sockets[]`, `hurtbox`, `portrait`, `masks[]`.

### 8.3 Sockets (pontos de emissão)
`hand_f` (arma/projétil), `hand_b`, `chest` (aura/beam), `mouth` (ki blast), `forehead` (beam), `back` (capa/asas), `feet` (poeira), `weapon_tip`.

Cada socket declara `bone` e `offset_px` / `offset_bone_local`.

### 8.4 Hitbox / hurtbox
- Hurtbox padrão do adulto: elipse **44 × 190 px**, base no root.
- Hitbox por clipe, em retângulo ou cápsula, com `active_frames`.
- Boss: hurtbox própria, nunca reduzida ao tamanho do player.

### 8.5 JSON
- UTF-8 sem BOM, indentação 2 espaços, newline final, inteiros para px, floats para ângulos.
- Sem `NaN`/`Infinity`. Sem chaves duplicadas. Ordenação de chaves alfabética em arquivos gerados (diffs limpos).

---

## 9. Orçamento de performance

| Item | Orçamento |
|---|---|
| Peças por personagem | 18–26 |
| Ossos por personagem | 28–40 |
| Desenhos por frame de personagem (pior caso) | ≤ 24 |
| Texturas de personagem em memória | ≤ 2 MB @1× |
| Atlas por personagem | 1 × 2048² (folgado) |
| Frames por clipe | 6–48 (exceções documentadas) |
| FPS de gameplay alvo | 60 |
| Personagens simultâneos (referência) | 30 |
| Partículas por efeito | ≤ 24 |
| Camadas de cenário | 3–5 ativas |
| Draw calls por personagem | ≤ 26 |
| Tamanho do pack por personagem (PNG+JSON) | ≤ 3 MB |

**Estratégia:** animação skeletal em runtime reduz memória drasticamente; o bake existe para engines sem skeletal 2D. Nunca pré-assar 60 fps de todos os clipes para todos os personagens sem necessidade.

---

## 10. Validação técnica automatizada

`tools/validate.py` verifica:

1. JSON parseia e valida contra schema.
2. Todo arquivo referenciado existe; todo arquivo órfão é reportado.
3. PNG é RGBA, dimensões corretas, não vazio, alpha presente.
4. Pivô dentro dos limites declarados (ou justificado fora).
5. `asset_id` único e formatado.
6. Camada existe em `layer_order.json`.
7. Nome de arquivo segue `standards/naming.json`.
8. `rig_compat` aponta para rig existente.
9. Nenhum frame de clipe fora da duração.
10. Loop declara frame de fechamento.
11. Socket aponta para osso existente.
12. Dimensões de atlas batem com o JSON.
13. Hash do asset registrado no manifesto.
14. Nenhum texto embutido em imagem de UI (quando `text_free: true`).

Falha em qualquer item = `QA_PENDING` ou `REWORK_REQUIRED`, nunca `APPROVED`.

---

## 11. Convenções de entrega

```
exports/
  individual_png/DB_CHAR_HERO_GOKU_BASE/parts/*.png
  spritesheets/DB_CHAR_HERO_GOKU_BASE/run.png + run.json
  atlases/DB_CHAR_HERO_GOKU_BASE.atlas.png + .json
  metadata/DB_CHAR_HERO_GOKU_BASE.json
  previews/DB_CHAR_HERO_GOKU_BASE__run__v1.0.0.gif
```

- Toda entrega é acompanhada de `checksums.sha256`.
- Nenhum arquivo temporário, `.psd`, cache ou imagem de teste entra em `exports/`.
- Assets reprovados vão para `production/rejected/<asset_id>/` com `reason.md`.

---

## 12. Compatibilidade e versionamento

- **SemVer** por asset: `MAJOR` quebra pivô/rig; `MINOR` adiciona clipe/peça; `PATCH` corrige arte.
- `rig_version` e `matrix_version` declarados em todo personagem.
- Mudança de pivô é **MAJOR** e exige migração.
- Consumidores devem tolerar campos extras (forward compatibility).
