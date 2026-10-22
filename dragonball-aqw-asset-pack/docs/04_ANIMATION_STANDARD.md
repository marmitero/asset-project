# 04 — ANIMATION STANDARD
**Projeto AURA · v1.0.0**
Norma de timing, poses, curvas, secundárias e feedback. É o documento que garante que "fluidez" seja uma propriedade reproduzível, não um acidente.

---

## 1. Os 12 princípios aplicados ao paper-doll

| Princípio | Como vira regra técnica |
|---|---|
| **Squash & stretch** | Escala não-uniforme em tronco/cabeça, preservando volume (`sx·sy ≈ 1`), máximo 12%. |
| **Antecipação** | Todo ataque tem 3–6 frames de recuo antes do golpe; skills têm 8–14. |
| **Staging** | Pose de ataque desenha uma linha de ação legível; arma fora da silhueta do corpo. |
| **Straight ahead / pose to pose** | Autoramos pose a pose (key poses), com inbetweens gerados por curva — não frame a frame. |
| **Follow through / overlapping** | Cabelo, capa, aura e arma têm atraso de 1–3 frames e continuam 4–10 frames após o corpo parar. |
| **Slow in / slow out** | Toda rotação de membro usa easing; `linear` é proibido. |
| **Arcs** | Mãos e pés percorrem Bézier; nunca linha reta. |
| **Secondary action** | Respiração, piscar, sway de quadril, poeira no pé. |
| **Timing** | Tabela normativa por clipe (§5). Holds de 2 frames em poses-chave. |
| **Exaggeration** | Ângulos 15–25% além do realista; nunca quebrar a junta. |
| **Solid drawing** | Volume constante; sem membro "de borracha". |
| **Appeal** | Silhueta e expressão antes de detalhe. |

---

## 2. Arquitetura de tempo

| Camada | Taxa | Por quê |
|---|---|---|
| **Autoria (keys)** | **24 fps** | Preserva o "timing de desenho" do Flash: holds, snappy attacks, peso. |
| **Amostragem (render)** | **60 fps** | Movimento contínuo em tela moderna. |
| **Preview GIF** | **25 fps** | GIF quantiza atraso em 10 ms; 25 fps (40 ms) é exato. |
| **Preview alpha** | **APNG 60 fps** | Inspeção de borda e fluidez real. |
| **Spritesheet baked** | 30 ou 60 fps | Fallback para engines sem skeletal. |

- Durações sempre declaradas em **frames de base (24)**; `ms = frames/24×1000`.
- Um clipe de 18 frames dura 750 ms.
- Nunca converter um clipe para 60 fps "esticando" keys sem reautoria de spacing.
- Holds: uma pose pode ser mantida 2–4 frames (jitter sutil de 0,3° para não "congelar").

---

## 3. ADR-0003 — Por que não animar tudo a 60 fps

Animar keys a 60 fps tende a produzir movimento "escorregadio": aceleração uniforme, sem contraste de tempo, sem peso. O olho lê isso como flutuação. AQW original roda a 24 fps e a sensação anime vem justamente do contraste entre poses rápidas (2 frames) e holds (4 frames).

**Decisão:** keys em 24, interpolação em 60. O contraste de timing é preservado; a suavidade vem da curva, não do número de desenhos.

---

## 4. Biblioteca de curvas

`standards/easing_library.json`. Nomes usados nas timelines:

| Nome | Curva | Uso |
|---|---|---|
| `linear` | reta | só eixos mecânicos |
| `ease_in_quad` | t² | iniciar movimento (antecipação saindo) |
| `ease_out_quad` | 1−(1−t)² | assentamento leve |
| `ease_in_out_quad` | smoothstep | respiração, sway |
| `ease_in_cubic` | t³ | golpe (aceleração violenta) |
| `ease_out_cubic` | 1−(1−t)³ | recuperação |
| `ease_in_out_cubic` | — | transições amplas |
| `ease_out_back` | overshoot 1,7 | overshoot de membro/arma |
| `ease_out_elastic` | oscilação amortecida | capa/cabelo em impacto |
| `ease_out_bounce` | quique | queda de corpo morto |
| `smoothstep` | 3t²−2t³ | default de membros |
| `catmull` | spline | trajetórias (mão, arma, pé) |
| `hold` | constante | holds de pose |

**Regra:** a soma de `ease_in_*` + `ease_out_*` em um movimento dá a sensação de peso; sem `ease_in` no golpe, o ataque parece empurrado.

---

## 5. Matriz de clipes — personagem jogável

Normativa para `humanoid_male_a`. Colunas: frames @24, duração, loop, fases, eventos.

### 5.1 Locomoção e estados

| Clip | Frames | ms | Loop | Fases | Eventos |
|---|---|---|---|---|---|
| `idle` | 96 | 4000 | ✅ | respiração ×2 + peso + blink | `blink@58` |
| `idle_combat` | 72 | 3000 | ✅ | base baixa, guarda, respiração curta | `blink@40` |
| `blink` | 4 | 167 | overlay | fechar/fechar/abrir | — |
| `walk` | 24 | 1000 | ✅ | 2 passos (contato/baixo/passagem/alto ×2) | `footstep@0,12` |
| `run` | 16 | 667 | ✅ | 2 passos com fase aérea | `footstep@0,8` |
| `walk_back` | 24 | 1000 | ✅ | 2 passos invertidos | `footstep@0,12` |
| `turn` | 12 | 500 | ❌ | pivô de 180° | `turn@6` |
| `jump_start` | 8 | 333 | ❌ | agachar 4 / esticar 4 | `jump@6` |
| `fall` | 8 | 333 | ✅ | loop de queda | — |
| `land` | 10 | 417 | ❌ | impacto 2 / recuperar 8 | `land@1`, `dust@1` |
| `dodge` | 16 | 667 | ❌ | antecipar 2 / deslocar 8 / recuperar 6 | `invuln_on@2`, `invuln_off@12` |
| `block_enter` | 6 | 250 | ❌ | erguer guarda | — |
| `block_loop` | 24 | 1000 | ✅ | guarda com tensão | — |
| `block_impact` | 10 | 417 | ❌ | recuo + recuperação | `impact@1` |
| `sit` | 40 | 1667 | ✅ | sentar + loop de respiração | — |

### 5.2 Combate

| Clip | Frames | ms | Loop | Fases (frames) | Eventos |
|---|---|---|---|---|---|
| `attack_light_1` | 18 | 750 | ❌ | antecipar 0–3 · golpe 4–5 · impacto 6 · hold 7–8 · recuperar 9–17 | `whoosh@3`, `vfx@5`, `hit@6`, `cancel@12` |
| `attack_light_2` | 20 | 833 | ❌ | antecipar 0–4 · golpe 5–6 · impacto 7 · hold 8–9 · recuperar 10–19 | `whoosh@4`, `vfx@6`, `hit@7`, `cancel@14` |
| `attack_light_3` | 22 | 917 | ❌ | antecipar 0–5 · golpe 6–7 · impacto 8 · hold 9–11 · recuperar 12–21 | `whoosh@5`, `vfx@7`, `hit@8`, `cancel@16` |
| `attack_heavy` | 30 | 1250 | ❌ | antecipar 0–8 · golpe 9–11 · impacto 12 · hold 13–16 · recuperar 17–29 | `whoosh@8`, `vfx@11`, `hit@12`, `shake@12`, `cancel@24` |
| `attack_crit` | 24 | 1000 | ❌ | antecipar 0–5 · golpe 6–7 · impacto 8 · hold 9–12 · recuperar 13–23 | `whoosh@5`, `vfx_crit@7`, `hit@8`, `flash@8`, `shake@8` |
| `attack_whiff` | 20 | 833 | ❌ | antecipar 0–3 · golpe 4–6 · desequilíbrio 7–11 · recuperar 12–19 | `whoosh@3`, `off_balance@8` |
| `cast` | 36 | 1500 | ❌ | preparar 0–6 · concentrar 7–18 · liberar 19–22 · recuperar 23–35 | `charge@7`, `release@19`, `vfx@20` |
| `channel` | 24 | 1000 | ✅ | loop de concentração | `tick@0,8,16` |
| `ki_charge` | 40 | 1667 | ✅ | loop de carga | `charge@0` |
| `hurt_light` | 12 | 500 | ❌ | impacto 0–1 · recuo 2–4 · recuperar 5–11 | `hit@0`, `flash@0` |
| `hurt_heavy` | 18 | 750 | ❌ | impacto 0–2 · recuo 3–7 · recuperar 8–17 | `hit@0`, `flash@0`, `shake@0` |
| `hurt_crit` | 24 | 1000 | ❌ | impacto 0–3 · giro/recuo 4–10 · recuperar 11–23 | `hit@0`, `flash@0`, `shake@0`, `crit_fx@0` |
| `knockback` | 20 | 833 | ❌ | impulso 0–3 · aéreo 4–9 · queda 10–13 · levantar 14–19 | `land@12` |
| `death` | 40 | 1667 | ❌ | impacto 0–3 · queda 4–16 · corpo 17–26 · desvanecer 27–39 | `death@20`, `fade@27` |
| `revive` | 30 | 1250 | ❌ | surgir 0–14 · levantar 15–29 | `revive@14` |
| `victory` | 60 | 2500 | ❌ | pose 0–14 · hold 15–30 · loop leve 31–59 | `sfx@14` |
| `taunt` | 48 | 2000 | ❌ | gesto 0–18 · hold 19–34 · retorno 35–47 | — |
| `transform_in` | 48 | 2000 | ❌ | carga 0–18 · explosão 19–26 · pose 27–47 | `aura_on@19`, `shake@19` |
| `transform_out` | 36 | 1500 | ❌ | dissipar 0–20 · retorno 21–35 | `aura_off@20` |
| `spawn` | 24 | 1000 | ❌ | materializar 0–14 · aterrissar 15–23 | `spawn@14` |

### 5.3 Regras da matriz
- Todo clipe tem **frame de fechamento** igual ao frame 0 quando `loop=true` (não renderizado; usado para emenda).
- `hit` ocorre **1 frame antes** do VFX de impacto para compensar o frame de render.
- `cancel` é o primeiro frame em que a ação pode ser interrompida por outra.
- Combo: `combo_window` = `[hit+2, hit+10]` para leves; `[hit+3, hit+12]` para pesado.
- Clipes de reação **não** têm loop.

---

## 6. Locomoção em detalhe

### 6.1 Caminhada (24 frames, 2 passos)

| Frame | Fase | Perna frontal | Perna traseira | Root Y | Braços |
|---|---|---|---|---|---|
| 0 | contato | estendida à frente (−18°) | estendida atrás (+18°) | 0 | opostos, ±22° |
| 3 | baixo | absorve peso (−6°) | empurra (+26°) | **−3** | ±18° |
| 6 | passagem | passa sob o corpo (+2°) | levanta, joelho 60° | +1 | ±8° |
| 9 | alto | push-off (+14°) | avança, joelho 30° | **+3** | 0° |
| 12 | contato | espelhado | espelhado | 0 | espelhado |
| 15 | baixo | — | — | −3 | — |
| 18 | passagem | — | — | +1 | — |
| 21 | alto | — | — | +3 | — |
| 24 | =0 | | | | |

- **Inclinação do tronco:** 4° à frente.
- **Rotação de quadril:** ±7°; **ombros:** ±6° em oposição.
- **Cabeça:** compensa 60% da rotação do tronco (estabilização).
- **Stride:** 2 passos = 140 px/s × 1 s = **140 px** → **70 px por passo**.
- **IK:** o pé de apoio fica travado no chão entre o contato e o push-off; o tornozelo resolve o ângulo. Slip máximo aceito: **1 px**.
- **Arcos:** o pé de balanço sobe 10 px e descreve arco; nunca desliza em linha reta.
- **Overlap:** capa/cabelo 2 frames atrás; arma 1 frame atrás com sway de 3°.

### 6.2 Corrida (16 frames, 2 passos)

| Frame | Fase | Root Y | Inclinação | Perna | Braço |
|---|---|---|---|---|---|
| 0 | contato | 0 | 14° | frontal −32° | oposto, 45° |
| 2 | baixo | **−6** | 15° | absorve, joelho 40° | 38° |
| 4 | push | +2 | 14° | estende +30° | 20° |
| 6 | aéreo | **+8** | 13° | ambas no ar, joelhos 55°/25° | 0° |
| 8 | contato | 0 | 14° | espelhado | espelhado |
| 14 | aéreo | +8 | 13° | — | — |
| 16 | =0 | | | | |

- **Speed:** 340 px/s; 2 passos em 0,667 s → **113 px por passo**.
- Braço frontal sobe até 45° e traseiro recua 35°; cotovelo nunca estica 100%.
- Cabelo e capa com **lag de 2–3 frames** e amplitude maior que no walk.
- A arma acompanha a mão com 1 frame de atraso e rotação de −6° no push-off.
- Fase aérea **obrigatória**: sem ela, não é corrida.

### 6.3 Idle (96 frames)

- **Respiração:** 2 ciclos de 48 frames. Tronco escala `sy 1,00→1,018→1,00` e `sx 1,00→0,994→1,00` (volume preservado).
- **Peso:** deslocamento lateral do root de ±2 px em ciclo de 96 frames, com quadril compensando 3°.
- **Cabeça:** sway de 2° com defasagem de 12 frames.
- **Braços:** ±2,5° com defasagem de 8 frames entre frontal e traseiro.
- **Capa/cabelo:** seno de 48 frames, amplitude 3–5°, defasagem por segmento.
- **Blink:** 1 evento no frame 58 (4 frames de overlay), mais blink aleatório em runtime a cada 2,4–5,0 s.
- **Movimento sempre presente:** nenhum frame idêntico ao anterior exceto o fechamento do loop.

---

## 7. Combate e feedback

### 7.1 Anatomia de um ataque

```
ANTECIPAÇÃO ──► GOLPE ──► IMPACTO ──► HOLD ──► RECUPERAÇÃO
   3–8f          2–3f       1f        2–4f       6–14f
   ease_out      ease_in    —         hold       ease_out
```

- **Antecipação:** ombro e quadril recuam em direções opostas; peso vai para o pé de trás. Arma sai da silhueta.
- **Golpe:** 2–3 frames no máximo. É o frame mais rápido do clipe.
- **Impacto:** 1 frame de contato + 2–4 de hold (hitstop). Sem hold, não há peso.
- **Recuperação:** overshoot de 4–6° e retorno com `ease_out_back`.
- **Cancelamento:** a partir do frame `cancel`; antes disso, o ataque é comprometido.

### 7.2 Hitstop (por tipo de golpe)

| Golpe | Hitstop (frames @60) | Duração | Screen shake | Flash branco |
|---|---|---|---|---|
| Leve | 3 | 50 ms | 3 px / 120 ms | 1 frame α 0,55 |
| Pesado | 5 | 83 ms | 6 px / 180 ms | 2 frames α 0,7 |
| Crítico | 8 | 133 ms | 10 px / 260 ms | 2 frames α 0,85 |
| Skill/ultimate | 10 | 167 ms | 14 px / 350 ms | 3 frames α 0,9 |

### 7.3 Números de dano

| Tipo | Cor | Tamanho | Animação |
|---|---|---|---|
| Normal | `#F2E9D8` | 22 px | sobe 28 px, fade 700 ms |
| Dano elemental | cor do elemento | 22 px | idem |
| Crítico | `#FFB020` | 34 px + contorno | pop 1,4×, shake, sobe 42 px, 900 ms |
| Cura | `#3FBF6A` | 22 px | sobe + ícone “+” |
| Miss | `#A9A28C` | 26 px | “MISS” sobe 18 px, fade 600 ms |
| Bloqueio | `#6FB6FF` | 22 px | “BLOCK” + faísca |

### 7.4 Miss, crítico e dano recebido (definições)

- **Miss/whiff (atacante):** `attack_whiff` — o golpe passa do alvo, o corpo continua 2 frames além, off-balance por 4 frames. VFX de “whoosh” sem impacto. Texto “MISS”.
- **Miss/evade (defensor):** `dodge` ou `evade_backstep` (12 frames: 3 recuo + 6 hold + 3 retorno). Invulnerabilidade de 2 a 12.
- **Crítico (atacante):** `attack_crit` — antecipação 2 frames maior, follow-through 6° além, flash + shake + VFX de crit. O dano é resolvido no `hit@8`.
- **Crítico (defensor):** `hurt_crit` — giro de tronco 15°, cabeça 22°, recuo de 28 px, face `crit`, 1 frame de silhueta branca.
- **Dano leve:** `hurt_light`, recuo 6 px, face `hurt`.
- **Dano pesado:** `hurt_heavy`, recuo 18 px, `shake` 4 px.
- **Bloqueio:** `block_impact`, recuo 4 px, faísca azul, sem mudança de face.

---

## 8. Movimento secundário

| Cadeia | Ossos | Rigidez | Amortecimento | Atraso | Amplitude máx. |
|---|---|---|---|---|---|
| Cabelo traseiro | 2 | 0,55 | 0,22 | 2 f | 18° |
| Cabelo SSJ | 3 | 0,65 | 0,18 | 2 f | 24° |
| Capa | 3 | 0,40 | 0,18 | 3 f | 32° |
| Cauda saiyajin | 3 | 0,50 | 0,20 | 2 f | 26° |
| Faixa/obi | 2 | 0,60 | 0,25 | 1 f | 14° |
| Antena namek | 1 | 0,70 | 0,30 | 1 f | 10° |
| Aura | procedural | — | — | — | ruído + pulsação 6% |

Modelo: mola-amortecida de segunda ordem, integrada a 60 Hz:
`a = -k·(θ - θ_target) - c·ω`; `θ += ω·dt`; `ω += a·dt`.
Clamps de ângulo por osso para não inverter.

Regras:
- A secundária **nunca** é a mesma curva da primária; sempre defasada.
- Em impacto, a secundária recebe impulso e oscila 8–14 frames.
- Em idle, a secundária é a única coisa que se move em alguns frames — é o que dá vida.

---

## 9. Transições, cancelamento e blend

| Transição | Blend | Observação |
|---|---|---|
| idle ↔ walk | 4 f (167 ms) | sincronizar fase do pé |
| walk ↔ run | 3 f | manter contato do pé |
| qualquer → hurt | 0 f (corte) | dano interrompe tudo |
| hurt → idle | 6 f | —
| ataque → idle | 6 f, após `cancel` | —
| ataque → ataque (combo) | 2 f | a partir de `combo_window` |
| cast → idle | 8 f | —
| block → idle | 4 f | —
| morte | 0 f | corta |

- Blend é **interpolação de pose por osso**, não cross-fade de bitmap.
- Durante blend, eventos do clipe de origem são suprimidos.
- Em rede/multiplayer, o estado é autoritativo no servidor; animação é previsão local.

---

## 10. Facing, espelhamento e root motion

- Personagem é autorado virado para **+X** (direita).
- Virar para −X = `scaleX = −1` no actor; sockets e VFX são espelhados junto.
- A arma permanece no slot `weapon_f` após o espelhamento (o `_f` continua sendo o lado da câmera).
- **Root motion:** desligado por padrão (o gameplay move o actor). Clipes `knockback`, `dodge` e `death` declaram `root_motion: true` com deslocamento embutido.
- Poeira/impacto no chão usam o socket `feet`, sempre em world space.

---

## 11. Eventos

| Evento | Payload | Consumo |
|---|---|---|
| `hit_frame` | tipo de dano, multiplicador | combate |
| `vfx_emit` | id, socket, offset, flip | VFX |
| `sfx` | id, volume | áudio |
| `footstep` | pé, superfície | áudio + poeira |
| `projectile_spawn` | id, socket, velocidade | combate |
| `hit_stop` | frames | câmera/animação |
| `shake` | amplitude, duração | câmera |
| `flash` | cor, alpha, frames | render |
| `invuln_on/off` | — | gameplay |
| `cancel` | — | input |
| `combo_window` | [início, fim] | input |
| `aura_on/off` | id | VFX |
| `transform` | forma | sistema |
| `turn` | direção | gameplay |
| `death` | — | gameplay |
| `fade` | alpha alvo | render |

---

## 12. Checklist de aprovação de clipe

- [ ] Duração e fases conforme §5, ±1 frame.
- [ ] Todos os membros usam curva (nenhum `linear`).
- [ ] Arco visível em mão, arma e pé.
- [ ] Root com subida/descida de peso (locomoção).
- [ ] Pé de apoio sem slip > 1 px.
- [ ] Secundárias defasadas e com overshoot.
- [ ] Pivôs sem fenda em todos os frames.
- [ ] Loop fecha sem salto (quando loop).
- [ ] Hit frame e eventos corretos.
- [ ] Expressão facial coerente com o esforço.
- [ ] Silhueta legível em 3 frames-chave.
- [ ] Reprodução a 25 fps e 60 fps aprovada visualmente.
