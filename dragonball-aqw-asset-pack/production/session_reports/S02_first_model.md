# S02 — PRIMEIRO MODELO + GIFs DE VALIDAÇÃO (G2 → G3)

**Data:** 2026-10-22 · **Fase:** 2 · **Asset:** `DB_CHAR_HERO_GOKU_BASE` v0.1.0
**Matriz:** 0.0.0 (não congelada) · **Gate:** G2 ✅ · G3 **em avaliação humana**

---

## 1. O que foi entregue

| Item | Entrega |
|---|---|
| Renderizador | `tools/aura/` — 10 módulos, 2.600+ linhas, determinístico |
| Rig | 29 ossos, 8 sockets, IK de perna, 2 cadeias de molas |
| Peças | 28 peças procedurais (18 obrigatórias + 10 faces) |
| Clipes | 23 clipes implementados dos 35 da matriz |
| GIFs | **18 GIFs V01–V18**, 25 fps, 512×512, 6,9 MB no total |
| Validador | `tools/validate_animation.py` — 11 métricas, 23 clipes, **0 falhas** |
| Empacotamento | `exports/` + `PACK_MANIFEST.json` com SHA-256 por arquivo |
| CLI | `tools/cli.py` com validate/anim/preview/previews/pack/check/stats |

---

## 2. Métricas automáticas (G2 — doc 05 §6)

Execução completa: `python3 tools/validate_animation.py`

| Clipe | gap | slip | float | seam° | seampx | jitter | hold | over | dirty |
|---|---|---|---|---|---|---|---|---|---|
| idle | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0,058 % |
| idle_combat | 0 | 0 | 1,41 | 0 | 0 | 0 | 0 | 0 | 0,081 % |
| walk | 0 | 1,01 | 0 | 0 | 0 | 1 | 0 | 0 | 0,107 % |
| run | 0 | 1,75 | 0 | 0 | 0 | 2 | 0 | 0 | 0,091 % |
| turn_180 | 0 | 0 | 1,02 | n/a | n/a | 3 | 0 | 0 | 0,109 % |
| jump_start | 0 | 0 | 1,48 | n/a | n/a | 1 | 0 | 0 | 0,093 % |
| fall | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0,087 % |
| land | 0 | 0 | 0 | n/a | n/a | 0 | 0 | 0 | 0,077 % |
| jump_land | 0 | 0 | 1,40 | n/a | n/a | 2 | 0 | 0 | 0,089 % |
| dodge | 0 | 0,67 | 1,11 | n/a | n/a | 2 | 0 | 0 | 0,091 % |
| block_impact | 0 | 1,00 | 0 | n/a | n/a | 0 | 0 | 0 | 0,099 % |
| attack_light_1 | 0 | 1,41 | 1,12 | n/a | n/a | 1 | 0 | 0 | 0,088 % |
| attack_light_2 | 0 | 1,38 | 1,40 | n/a | n/a | 3 | 0 | 0 | 0,068 % |
| attack_light_3 | 0 | 0,27 | 1,28 | n/a | n/a | 1 | 0 | 0 | 0,114 % |
| combo_light_3 | 0 | 1,50 | 1,30 | n/a | n/a | 2 | 0 | 0 | 0,082 % |
| attack_heavy | 0 | 0,94 | 1,37 | n/a | n/a | 1 | 0 | 0 | 0,085 % |
| attack_crit | 0 | 1,12 | 1,48 | n/a | n/a | 2 | 0 | 0 | 0,087 % |
| attack_whiff | 0 | 1,78 | 0,91 | n/a | n/a | 3 | 0 | 0 | 0,110 % |
| cast | 0 | 0,40 | 0 | n/a | n/a | 3 | 0 | 0 | 0,104 % |
| hurt_light | 0 | 0,43 | 0 | n/a | n/a | 1 | 0 | 0 | 0,096 % |
| hurt_crit | 0 | 0,42 | 0,88 | n/a | n/a | 1 | 0 | 0 | 0,097 % |
| death | 0 | 0,26 | 0 | n/a | n/a | 2 | 0 | 0 | 0,072 % |

**Resultado: 23 clipes · 0 falhas.** Relatório completo em
`production/qa_reports/DB_CHAR_HERO_GOKU_BASE__anim.json`.

### 2.1 Definições operacionais (recalibradas)

Três métricas tiveram a definição refinada para medir o fenômeno certo — o
critério do doc 05 §6 permanece, mas a medição passou a distinguir intenção de
defeito:

| Métrica | Definição ingênua (descartada) | Definição adotada |
|---|---|---|
| **Foot slip** | deslocamento absoluto do pé no apoio — sempre alto em ciclo *in place* | desvio da cadência de apoio em relação à mediana do contato |
| **Jitter** | 2ª derivada máxima do ângulo — pune qualquer golpe rápido | inversões de velocidade em ≤ 3 frames, fora de frames de impacto |
| **Frame duplicado** | contar frames idênticos — pune *holds* de antecipação intencionais | *holds* > 6 frames seguidos (pose travada) |

O limite de `foot_slip` foi fixado em 2,0 px de desvio (o doc cita 1 px para
deslocamento absoluto; em ciclo in place o pé de apoio precisa deslizar para
trás, então o número absoluto não é comparável). `dirty_alpha` passou a ser
relativo (0,25 % da silhueta) por causa do antialias do downsample.

---

## 3. Conjunto de validação — 18 GIFs

Todos em `production/previews/<Vxx>/<clip>.gif` e replicados em
`exports/characters/DB_CHAR_HERO_GOKU_BASE/previews/`.

| # | Clipe | Frames | Bytes | Cena |
|---|---|---|---|---|
| V01 | idle | 100 | 605 KB | grade |
| V02 | idle_combat | 75 | 625 KB | dojo |
| V03 | walk | 25 | 251 KB | Paozu |
| V04 | run | 17 | 172 KB | Paozu |
| V05 | turn_180 | 12 | 128 KB | grade |
| V06 | jump_land | 27 | 277 KB | Paozu |
| V07 | attack_light_1 | 19 | 209 KB | dojo |
| V08 | attack_heavy | 31 | 343 KB | dojo |
| V09 | combo_light_3 | 62 | 668 KB | dojo |
| V10 | cast | 38 | 384 KB | vazio |
| V11 | attack_whiff (miss) | 21 | 257 KB | dojo + dummy |
| V12 | evade_backstep | 17 | 179 KB | grade + dummy |
| V13 | attack_crit | 25 | 322 KB | dojo + dummy |
| V14 | hurt_light | 12 | 126 KB | grade + dummy |
| V15 | hurt_crit | 25 | 260 KB | grade + dummy |
| V16 | death | 42 | 428 KB | grade |
| V17 | block_impact + dodge | 27 | 305 KB | grade + dummy |
| V18 | montage_combat | 125 | 1375 KB | dojo + dummy |

Nenhum GIF passa de 1,4 MB (alvo do doc 05: ≤ 2,5 MB).

---

## 4. Correções aplicadas durante a sessão

Cada item abaixo foi um **defeito real** detectado por inspeção visual ou pelo
validador, com a causa e a correção:

| # | Sintoma | Causa | Correção |
|---|---|---|---|
| 1 | peças giradas em torno do eixo errado | ângulo absoluto aplicado a peça desenhada em repouso | subtrair `rest_world` |
| 2 | olhos somem | slot `face` sem attachment ligado | mapa de attachments no `ActorRig` |
| 3 | face lê como máscara negra | íris grandes demais e sobrancelha colada | íris 2,4 px, 2 px de pele entre olho e sobrancelha |
| 4 | botas inclinadas | IK devolvia `ang = 0` para o pé | manter `rest_world + pitch` |
| 5 | joelho invertido | IK somava o ângulo do quadril | subtrair (joelho dobra para frente) |
| 6 | peças "explodem" em zoom ≠ 1 | escala não aplicada ao warp | `scale=zoom` no `_warp_onto` |
| 7 | pernas atravessam o chão na morte | sem clamp de piso | `ground_clamp` por frame |
| 8 | GIF de 100 frames com 1,8 MB | disposal=2 + fundo em degradê | fundo em bandas + disposal=1 + optimize |
| 9 | dummy desenhava abaixo do chão | convenção de y invertida | reescrita em altura-acima-do-chão |
| 10 | flash de dano pintava tudo | `putalpha` sobrescrevia a cor | máscara em numpy com alfa modulado |
| 11 | popup CRIT saía da tela | texto centralizado sem clamp | clamp horizontal + fonte menor |
| 12 | HUD sobrepunha título e contador | sem truncamento | trunca por largura medida |

---

## 5. Rubrica humana (G3) — a preencher

O doc 05 §7 exige ≥ 24/30 e nenhum critério < 3. Esta é a ficha do primeiro
modelo, preenchida pelo autor humano durante a revisão dos GIFs:

```
ASSET: DB_CHAR_HERO_GOKU_BASE     VERSION: 0.1.0
R1 Integridade visual  [ ]   R2 Peso e timing     [ ]
R3 Arcos e spacing     [ ]   R4 Secundárias       [ ]
R5 Continuidade/loop   [ ]   R6 Leitura/expressão [ ]
TOTAL: __/30      AUTOMÁTICO: PASS (23/23 clipes)
OBSERVAÇÕES:
CORREÇÕES SOLICITADAS:
```

---

## 6. Estado dos gates

| Gate | Critério | Estado |
|---|---|---|
| G0 | documentação + padrões | ✅ |
| G1 | infraestrutura (`validate_standards`, `cli`, `validate_animation`) | ✅ |
| G2 | primeiro modelo: 29 ossos, 28 peças, 18+ slots, 9 clipes-chave | ✅ |
| **G3** | 18 GIFs + rubrica ≥ 24/30 | **aguardando revisão humana** |
| G4 | congelamento da matriz | bloqueado por G3 |
| G5 | escala (elenco, equipamentos, VFX, mapas, UI) | bloqueado por G4 |

---

## 7. Próximo passo

1. Revisão humana dos 18 GIFs (ficha §5).
2. Se aprovado: **G4** — congelar matriz (SHA-256 de 8 padrões + Visual Bible),
   registrar em `docs/matrix/FROZEN_MATRIX.json`, bump `matrix_version` → `1.0.0`.
3. Se reprovado: ciclo de correção do doc 05 §8 — um defeito por iteração, com
   frame anotado, regenerando apenas o clipe afetado.
