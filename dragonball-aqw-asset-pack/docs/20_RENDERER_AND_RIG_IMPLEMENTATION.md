# 20 — IMPLEMENTAÇÃO DO RENDERIZADOR E DO RIG
**Projeto AURA · v1.0.0 · Fase 2 (S02)**

Este documento descreve **como** o pipeline vetorial-first da ADR-0001 foi
realmente implementado em `tools/aura/`. Ele é a ponte entre a especificação
(docs 02–05) e o código que gera os GIFs de validação.

---

## 1. Por que um renderizador próprio

O pack precisa ser **reproduzível**: qualquer pessoa (ou IA) deve poder regerar
cada frame a partir de JSON + código, sem depender de um arquivo PSD perdido.
Por isso nenhum sprite é desenhado à mão em bitmap: as peças são **descritas**
por formas e o frame é **composto** pelo renderizador.

| Requisito | Consequência de projeto |
|---|---|
| Determinismo total | zero aleatoriedade; qualquer ruído é semente fixa |
| Fluidez | interpolação + IK + molas em vez de poses fixas |
| Variação barata | troca de textura/cor/peça sem redesenhar animação |
| Verificável por máquina | cada frame sai com sockets e world-space do esqueleto |

---

## 2. Arquitetura dos módulos

```
tools/aura/
  core.py      paleta, Catmull-Rom, operadores de peça, build em 4x, warp
  shapes.py    formas (capsule, oval, poly) e atalhos F/CF/AS/AH/CL
  pose.py      esqueleto, cinemática direta, IK de 2 ossos, molas
  rig.py       montagem: camadas + warp por osso + sockets + clamp de chão
  anim.py      controles de alto nível -> Pose (lean, crouch, foot targets)
  clips.py     biblioteca de clipes do 1º modelo
  easing.py    avaliador de standards/easing_library.json
  scene.py     fundos, VFX, HUD, rastro de movimento
  dummy.py     boneco de treino + números de dano (cenas de combate)
  render.py    clipe -> frames 512² com câmera, FX e feedback
  export.py    GIF, APNG, spritesheet, folha de contato
```

### 2.1 `core.py` — rasterização

Cada peça é uma `Part` com lista de operadores:

| Operador | Efeito |
|---|---|
| `fill` / `fill_poly` | silhueta base (Catmull-Rom suaviza; `_poly` mantém arestas) |
| `shadow` / `highlight` | manchas recortadas pela silhueta (cel shading manual) |
| `auto_shadow` / `auto_highlight` | silhueta deslocada 2–3 px, recortada — sombra automática |
| `line` / `clip_line` | detalhes internos; `clip` garante que não vazem da peça |
| `clip_fill` | preenchimento recortado (decote, bandagens) |

As peças são construídas em **4×** (supersample estático) e reduzidas para 2×
por LANCZOS. O contorno vem de **dilatação morfológica** (OpenCV) sobre o alfa:
3,0 px externo, sem costura em junta rotacionada — o método da ADR-0001.

### 2.2 `pose.py` — esqueleto

29 ossos, 8 sockets, 13 rigs derivados. Convenções:

- ângulos em graus, **positivo = horário na tela**;
- cada osso tem `pos` (mundo, y para cima) e `dir_deg` (direção absoluta);
- a cinemática direta acumula `(rest_world + delta)` e herda escala do pai;
- **IK de 2 ossos** posiciona joelho/tornozelo a partir do alvo do pé;
- **molas** (stiffness/damping) animam cabelo e capa com atraso.

Duas decisões que evitaram bugs clássicos:

1. **Singularidade do IK.** Quando a perna fica reta, `acos` produz duas
   soluções e o joelho "estala" ~300° em um frame. A distância é limitada a
   97,5 % de `l1 + l2`, mantendo o joelho ligeiramente dobrado.
2. **Pivô = cabeça do osso.** A peça é desenhada na pose de repouso e rotacionada
   em torno do pivô; o ângulo aplicado é `world_angle − rest_angle`. Sem essa
   subtração todas as peças giram em torno do eixo errado.

### 2.3 `rig.py` — composição

Ordem de desenho = `layer_order.json` elevado ao espaço 2× do canvas. Detalhes
que afetam a fluidez percebida:

- **membros de trás a 82 % de luminosidade** (profundidade AQW);
- **trava de chão**: nenhum pé/tornozelo desenha abaixo de `y = 0`; se o IK
  pedir, o pé é preso e os descendentes recalculados (evita "atravessar o piso"
  em morte/queda);
- **sockets** recalculados por frame (mão, boca, peito, ponta de arma) — usados
  por VFX, números de dano e rastro;
- **sombra de contato** em gradiente gaussiano (não um disco chapado).

### 2.4 `anim.py` — controles, não ossos

Os clipes não animam ossos diretamente. Escrevem **controles legíveis**:

```
lean, twist, crouch, head_turn, head_tilt,
shoulder_f/b, elbow_f/b, wrist_f/b, spread_f/b,
hip_f/b, knee_f/b, foot_fx/fy/bx/by (alvos de IK), foot_fp/bp (pitch),
root_x, root_y, hair, impulse
```

`pose_from_params` traduz controles em rotações e alvos de pé. Vantagens:
reaproveitar clipes entre rigs, reescrever a matriz sem tocar nas peças e
inspecionar um keyframe lendo um dicionário.

---

## 3. Fluxo de um frame

```
clip.sample(frame)          # interpolação com a curva de easing do trecho
      ↓
pose_from_params()          # controles -> rotações + alvos de pé
      ↓
Skeleton.solve()            # cinemática direta
      ↓
solve_leg() + recompute()   # IK de perna
      ↓
Secondary.apply()           # cabelo/capa com molas
      ↓
ActorRig.render()           # 20+ peças: warp afim + alpha_composite em 2×
      ↓
resize LANCZOS -> 512²      # downsample com pré-filtro
      ↓
scene (fundo, dummy, FX, HUD, popup)
```

Custo medido: **57 ms/frame** (24 peças, 512², 2×) — o mesmo número do
benchmark da Fase 1. Um clipe de 96 frames leva ~5,5 s; os 18 GIFs de validação
levam **46 s** no total.

---

## 4. Referência de peças do primeiro modelo

18 peças obrigatórias + 10 faces + cabelo = **28 arquivos de peça** gerados por
código (`parts_goku.py`).

| Grupo | Peças |
|---|---|
| Cabeça | `head`, `hair_front`, `hair_back` |
| Face | 10 expressões: neutral, combat, angry, strain, hurt, crit, shock, smirk, dead, blink |
| Tronco | `torso` (gi + V azul + faixa), `pelvis` |
| Braços | `upper_arm_f/b` (manga azul), `forearm_f/b`, `hand_f/b` |
| Pernas | `thigh_f/b`, `shin_f/b`, `foot_f/b` (bota com bico e solado) |

Proporções finais: altura 220 px, cabeça 46 px (~4,8 cabeças), tronco 76 px,
pernas 80 px, mãos 19 px, pés 30 px de comprimento. A silhueta foi calibrada
contra a referência AQW: cabeça grande, mãos e pés exagerados, tronco curto.

---

## 5. Limitações conhecidas (v0.1.0)

| Limite | Consequência | Mitigação planejada |
|---|---|---|
| Vista 3/4 fixa para a direita | `turn_180` só espelha o sprite | rig de 8 direções na fase de expansão |
| Sem física de tecido real | capa/cabelo são molas 1-D | colisão simples na S09 |
| Antialiasing de warp | bordas levemente suaves em 512² | render 4× para export final de sprite |
| Sem som | — | fora do escopo do pack |

---

## 6. Como reproduzir

```bash
python3 tools/cli.py validate     # standards + schemas
python3 tools/cli.py anim         # 11 métricas em 23 clipes
python3 tools/cli.py previews     # 18 GIFs V01–V18
python3 tools/cli.py pack         # exports/ + manifests com SHA-256
python3 tools/cli.py check        # tudo acima
```
