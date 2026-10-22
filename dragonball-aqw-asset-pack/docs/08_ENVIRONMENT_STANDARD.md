# 08 — ENVIRONMENT STANDARD
**Projeto AURA · v1.0.0**
Norma de cenários 2.5D: camadas, parallax, tiles, props, colisão, oclusão e iluminação.

---

## 1. Modelo espacial

O jogo é **2.5D lateral com plano XY**: o personagem anda para os lados (X) e para frente/trás na tela (Y), com profundidade sugerida por escala, oclusão e parallax — não há rotação de câmera.

```
                 parallax 0.05  céu
                 parallax 0.15  horizonte / montanhas
                 parallax 0.35  fundo médio
                 parallax 0.55  estruturas
                 parallax 0.75  decoração distante
  ──────────────────────────────────────────────  linha de chão (walk band)
                 parallax 1.00  chão caminhável + props
                 parallax 1.25  primeiro plano
                 parallax 1.30  occluders
```

- **Plano jogável:** faixa horizontal; o eixo Y da tela vira profundidade. Personagens “atrás” são desenhados antes e ligeiramente menores (escala 1,0 → 0,86 no fundo da faixa).
- **Câmera:** fixa em Y, rola em X com clamp por mapa.
- **Viewport de referência:** 1280 × 720.
- **Camada de arte:** 1920 × 1080 (permite pan e overscan).
- **Linha de chão base:** y = 640 px no viewport (personagem 220 px → cabeça em 420).

### 1.1 Regra de escala por profundidade
| Posição na faixa | Escala do ator | Velocidade |
|---|---|---|
| Frente (y=700) | 1,00 | 1,00× |
| Meio (y=640) | 0,93 | 0,93× |
| Fundo (y=590) | 0,86 | 0,86× |

O gameplay usa y para ordenar e escalar; a arte do chão já sugere a perspectiva.

---

## 2. Camadas

| # | Camada | Parallax | Conteúdo | Contorno |
|---|---|---|---|---|
| L0 | `sky` | 0,05 | gradiente de céu, sol/lua, nuvens distantes | nenhum |
| L1 | `horizon` | 0,15 | montanhas, silhuetas de cidade | nenhum |
| L2 | `mid` | 0,35 | floresta, castelo, ruínas | 0–0,6 px |
| L3 | `structures` | 0,55 | prédios, templos, portões | 0,8 px |
| L4 | `decor` | 0,75 | árvores menores, estátuas, bandeiras | 0,8 px |
| L5 | `ground` | 1,00 | chão caminhável + tile overlay | nenhum |
| L6 | `props` | 1,00 | barris, pedras, fogueiras, placas | 1,2 px |
| L7 | `foreground` | 1,25 | galhos, colunas, folhas | 1,2 px |
| L8 | `occluders` | 1,30 | objetos que escondem atores | 1,2 px |
| L9 | `overlay` | 1,00 | clima, poeira, luz volumétrica | nenhum |

Regras:
- Camadas L0–L4 são **dessaturadas** progressivamente (15%, 25%, 35%).
- Nenhuma camada de fundo usa preto puro; a mais escura é `#2A2F3C`.
- Personagem sempre tem contraste ≥ 2 tons contra L2–L5.
- Foreground nunca cobre mais de 20% da tela.

---

## 3. Tiles de chão

| Propriedade | Valor |
|---|---|
| Tamanho | 256 × 256 |
| Formato | PNG RGBA opaco (chão não tem alpha) |
| Costura | 0 px de emenda em X e Y |
| Variações | 4 por bioma (base, detalhe, transição, borda) |
| Teste | bloco 3×3 sem emenda visível |
| Overlay | camada separada de detalhes (pedras, grama) para variação |

- Tiles não podem ter gradiente que atravesse a borda.
- Bordas de penhasco/água usam tiles próprios com alpha.
- Chão deve ter textura legível, mas sem detalhe de 1 px (evita ruído).

---

## 4. Props

- Pivô no **centro da base** (ponto de contato com o chão).
- Sombra de contato embutida é proibida; sombra é renderizada em runtime.
- Escala declarada em `scale_ref` (ex.: barril 0,35 do personagem).
- Props interativos têm contorno 1,2 px e variante `_glow` para destaque.
- Props destrutíveis têm 2 estados (intacto, quebrado) + VFX.
- Ancoragem declarada: `ground`, `wall`, `ceiling`, `floating`.

---

## 5. Mapas prioritários

| ID | Nome | Bioma | Elementos-chave |
|---|---|---|---|
| `map_paozu` | Monte Paozu | floresta/montanha | casa de Goku, lago, árvores, estrada de terra |
| `map_kame_house` | Kame House | ilha | casa rosa, palmeiras, mar, areia |
| `map_west_city` | Cidade do Oeste | urbano | prédios arredondados, carros voadores, letreiros |
| `map_tournament` | Torneio de Artes Marciais | arena | ringue, arquibancada, estátuas |
| `map_namek` | Namekusei | alienígena | céu verde, ilhas, casas de cúpula, árvores azuis |
| `map_cell_games` | Arena de Cell | deserto/arena | ringue de pedra, crateras, rochas |
| `map_beerus` | Planeta de Beerus | divino | deserto roxo, árvores cristalinas, templo |
| `map_top` | Torneio do Poder | arena celestial | plataforma flutuante, arquibancada, vazio |

Cada mapa entrega:
```
environments/maps/<map_id>/
  layers/{sky,horizon,mid,structures,decor,ground,foreground,occluders}.png
  tiles/<bioma>_*.png
  props/*.png
  map.json          (colisão, spawns, portais, âncoras de NPC, câmera)
  preview.png       (com ator de referência)
  manifest.json
```

---

## 6. `map.json` — dados do mapa

```json
{
  "map_id": "map_paozu",
  "viewport": [1280, 720],
  "world_width": 3200,
  "ground_band": {"front_y": 700, "back_y": 590},
  "camera": {"min_x": 0, "max_x": 1920, "y": 360},
  "spawns": [{"id": "spawn_start", "pos": [320, 660]}],
  "portals": [{"id": "to_kame", "pos": [3100, 650], "target": "map_kame_house", "spawn": "spawn_east"}],
  "colliders": [{"type": "polygon", "points": [[0, 700], [3200, 700], [3200, 760], [0, 760]]}],
  "blockers": [{"type": "rect", "rect": [1200, 640, 180, 60]}],
  "occluders": [{"id": "tree_01", "rect": [900, 560, 120, 190], "layer": "occluders"}],
  "props": [{"id": "house", "pos": [800, 660], "scale": 2.2, "anchor": "ground"}],
  "npc_anchors": [{"id": "goku_house_door", "pos": [780, 655]}],
  "ambient": {"weather": "none", "light": "day", "palette": "earth_forest"}
}
```

- Colisão em polígono/retângulo no plano XY (não pixel-perfect).
- `blockers` impedem passagem; `colliders` definem área caminhável.
- `occluders` geram máscara de oclusão por Y.
- Portais e spawns são dados, não arte.

---

## 7. Iluminação e paleta por bioma

| Bioma | Céu | Sombra | Destaque | Atmosfera |
|---|---|---|---|---|
| Floresta (dia) | `#8FC5E8` | `#2F4A2A` | `#B7D98A` | quente, verde |
| Ilha | `#7FC8F0` | `#2A5A6A` | `#F2D9A0` | areia clara, mar turquesa |
| Cidade | `#9AB6D8` | `#2E3446` | `#E8D9B8` | cinza-azulado |
| Arena | `#B9D4E8` | `#6B5138` | `#D9B77A` | poeira dourada |
| Namek | `#7FD9B0` | `#1E4A4A` | `#B8F0D8` | verde-azulado alienígena |
| Cell Games | `#E8C99A` | `#5A4430` | `#F2E0B8` | deserto quente |
| Beerus | `#3A2A5A` | `#1A1230` | `#C99AE8` | roxo divino |
| TOP | `#1A2038` | `#0E1220` | `#F2D9A0` | vazio estelar |

Regras:
- Paleta do cenário não compete com a do personagem (Goku laranja nunca sobre fundo laranja).
- Hora do dia declarada (`day`, `dusk`, `night`) e aplicada por *color script* em todas as camadas.
- Luz do cenário deve concordar com a luz do personagem (cima/frente).

---

## 8. Uso de IA generativa em cenários

Permitido **somente** para backdrops pintados (L0–L2) e texturas orgânicas, com pós-processamento obrigatório:

1. Sem contorno preto grosso.
2. Dessaturar 15%.
3. Reduzir contraste em 20%.
4. Escurecer 8% nas bordas (vinheta de profundidade).
5. Verificar coerência de luz com a regra do projeto.
6. Recortar em camadas e gerar parallax manualmente.
7. Nenhum personagem, texto ou logo na imagem.

Prompt padrão:

> "2D game background, painted, soft edges, no outlines, no characters, no text, fantasy/anime environment, **{tema}**, time of day **{hora}**, palette **{paleta}**, side-scrolling backdrop, wide composition, muted contrast, high readability, **{camada}** layer only."

Assets gerados por IA **nunca** entram como personagem, prop interativo ou UI.

---

## 9. Performance e entrega

| Item | Limite |
|---|---|
| Camadas ativas | ≤ 5 |
| Textura por mapa | ≤ 12 MB |
| Props por tela | ≤ 40 |
| Partículas ambientais | ≤ 30 |
| Tiles distintos por bioma | ≤ 16 |

Entrega: PNG por camada, tiles, props, `map.json`, `preview.png` com ator de referência na linha de chão, e validação de costura.

---

## 10. Checklist de cenário

- [ ] Camadas separadas e nomeadas.
- [ ] Parallax declarado.
- [ ] Chão tileável sem costura (teste 3×3).
- [ ] Personagem legível contra todas as camadas.
- [ ] Prop com pivô na base e sombra de runtime.
- [ ] `map.json` válido (colisão, spawn, portal, câmera).
- [ ] Oclusores com máscara.
- [ ] Paleta do bioma respeitada.
- [ ] Sem texto/logo embutido.
- [ ] Preview com ator de referência.
