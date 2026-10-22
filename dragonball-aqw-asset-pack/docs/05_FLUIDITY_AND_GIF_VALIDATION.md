# 05 — FLUIDEZ E PROTOCOLO DE VALIDAÇÃO POR GIF
**Projeto AURA · v1.0.0**
Este documento define o **Gate G3**, o mais importante do projeto: nenhum asset avança para produção em escala sem passar por aqui.

---

## 1. Definição operacional de fluidez

Um sprite é fluido quando, reproduzido em movimento, satisfaz **seis critérios**:

| # | Critério | Definição | Limite técnico |
|---|---|---|---|
| F1 | **Integridade de junta** | Nenhum pixel de fundo aparece entre peças, em nenhum frame. | 0 px de gap em todas as juntas, todos os frames |
| F2 | **Peso e timing** | Existe contraste entre rápido e lento; não há aceleração uniforme. | ≥ 1 seguimento `ease_in_*` + ≥ 1 `ease_out_*` por movimento; hitstop presente |
| F3 | **Arcos e spacing** | Mãos, pés e arma percorrem curvas; o espaçamento entre frames acelera e desacelera. | Desvio de reta > 2 px em arcos; variação de spacing > 20% |
| F4 | **Sobreposição de ação** | Secundárias chegam depois e terminam depois do corpo. | Atraso 1–3 frames; overshoot ≥ 2° |
| F5 | **Contato com o chão** | O pé de apoio não escorrega nem flutua. | Slip ≤ 1 px; contato com y=0 ±1 px |
| F6 | **Continuidade** | O loop fecha; não há salto de pose, jitter ou frame duplicado acidental. | Δângulo ≤ 0,5°; Δpos ≤ 0,5 px; sem duplicata não intencional |

**Definição de aprovado:** F1–F6 atendidos + rubrica §7 ≥ 24/30 + nenhum critério da rubrica < 3.

---

## 2. Por que GIF (e não vídeo)

- O GIF é **scrubável frame a frame** por qualquer pessoa, sem ferramenta.
- Roda em loop contínuo, expondo emendas.
- É o formato que o usuário pediu e o que artistas usam para revisão de ciclo.
- **Limitação:** GIF tem alpha binário e atraso quantizado em 10 ms. Por isso:
  - preview em **GIF 25 fps (40 ms)** com **fundo sólido** de revisão;
  - preview alpha em **APNG 60 fps** para inspeção de borda;
  - o master nunca é GIF — é PNG + JSON.

---

## 3. Especificação técnica dos GIFs

| Propriedade | Valor |
|---|---|
| Canvas | 512 × 512 (personagem), 256 × 256 (pet), 1024 × 1024 (boss) |
| FPS | **25** (delay 40 ms) |
| Fundo | `#14161C` com grade de 32 px a 6% e linha de chão `#2A2F3C` |
| Sombra | elipse de contato sempre visível |
| Rótulo | canto inferior esquerdo: `ASSET_ID · CLIP · vX.Y.Z · 25fps` |
| Régua | marca de 220 px à direita (toggle `--ruler`) |
| Loop | infinito para loops; one-shot **não** loopa, mas segura o último frame 1,0 s |
| Paleta | quantização adaptativa 256 cores + dithering desligado |
| Tamanho alvo | ≤ 2,5 MB por GIF |
| Nome | `DB_CHAR_HERO_GOKU_BASE__<clip>__v0.1.0.gif` |

**Regra de revisão:** assistir 3 loops completos a 100%, depois 1 loop a 50%, depois scrub frame a frame.

---

## 4. Pacote de validação do primeiro modelo (18 GIFs)

Obrigatórios antes do Gate G3. Todos com o mesmo boneco, mesma luz e mesma câmera.

| # | Clip | Frames | Duração | O que valida | Ajuda visual |
|---|---|---|---|---|---|
| V01 | `idle` | 96 | 4,0 s | Respiração, blink, secundárias, loop | — |
| V02 | `idle_combat` | 72 | 3,0 s | Guarda, leitura de combate | — |
| V03 | `walk` | 24 | 1,0 s | Ciclo de 2 passos, foot plant, bob | grade de chão |
| V04 | `run` | 16 | 0,667 s | Fase aérea, inclinação, overlap | grade de chão |
| V05 | `turn_180` | 12 | 0,5 s | Espelhamento sem popping | seta de facing |
| V06 | `jump_land` | 26 | 1,08 s | Antecipação, ar, impacto | linha de chão |
| V07 | `attack_light_1` | 18 | 0,75 s | Antecipação, golpe de 2 f, hitstop | contador de frames |
| V08 | `attack_heavy` | 30 | 1,25 s | Peso, overshoot, recuperação | contador |
| V09 | `combo_light_3` | 60 | 2,5 s | Emenda entre ataques, cancel window | janela de combo realçada |
| V10 | `cast` | 36 | 1,5 s | Concentração, liberação, VFX | socket de mão |
| V11 | `attack_whiff` (**miss**) | 20 | 0,833 s | Golpe no vazio, desequilíbrio | “MISS” |
| V12 | `evade_backstep` (**miss do alvo**) | 12 | 0,5 s | Esquiva do defensor | “MISS” |
| V13 | `attack_crit` (**crítico**) | 24 | 1,0 s | Golpe ampliado, flash, shake | “CRIT” + shake |
| V14 | `hurt_light` (**dano recebido**) | 12 | 0,5 s | Reação rápida, face `hurt` | flash |
| V15 | `hurt_crit` (**dano crítico recebido**) | 24 | 1,0 s | Giro, knockback, face `crit` | flash + número |
| V16 | `death` | 40 | 1,667 s | Queda com peso, fade | — |
| V17 | `block_impact` + `dodge` | 26 | 1,08 s | Guarda, faísca, esquiva | ícone de guarda |
| V18 | `montage_combat` | 120 | 4,8 s | Tudo junto com dummy e HUD mínimo | composição completa |

### 4.1 Cena de combate (V11–V15, V18)
- Um **dummy** (`DB_CHAR_DUMMY_STRAW_A`) ocupa o lado direito, com hurtbox visível.
- Overlays: número de dano, texto MISS/CRIT, flash, shake.
- O GIF mostra **atacante + defensor + feedback simultâneos** — é assim que se valida legibilidade de combate.
- Ângulo de câmera fixo; personagens nunca saem do canvas.

### 4.2 Variações adicionais (a partir do G4, para cada personagem)
Turnaround de silhueta, troca de 3 equipamentos em loop, transformação SSJ, aura loop, sentar/levantar, vitória, taunt, piscar isolado, vento (capa/cabelo), carga de ki.

---

## 5. Como o GIF é gerado

```
rig.json + clip.json
      │
      ├─► amostragem 60 fps (interpolação + IK + spring)
      │
      ├─► render 2048² (4×) ─► downsample 512²
      │
      ├─► composição de cena (fundo, dummy, overlays, labels)
      │
      └─► GIF 25 fps (Pillow) + APNG 60 fps + spritesheet
```

- O **mesmo** pipeline gera GIF, APNG, spritesheet e frames PNG. Não existe "GIF de mentira" feito à mão.
- Se o GIF mostra, o asset tem.
- Contexto de render registrado em `exports/previews/<asset>/manifest.json`: commit, hash do rig, hash do clipe, versão do renderizador.

---

## 6. Métricas automáticas (portão técnico)

`tools/validate_animation.py` roda em cada frame e falha o build se:

| Métrica | Como mede | Limite |
|---|---|---|
| **Gap de junta** | janela de 6×6 px no centro de cada junta; conta pixels com alpha < 8 circundados por alpha > 0 | 0 px |
| **Pivô deslocado** | distância entre pivô da peça e cabeça do osso no espaço world | ≤ 0,25 px |
| **Foot slip** | posição world do pé de apoio durante frames de contato | ≤ 1 px |
| **Foot float** | distância do pé ao chão nos frames de contato | ≤ 1 px |
| **Loop seam (pose)** | Δângulo e Δposição entre frame `N` e `0` | ≤ 0,5° / ≤ 0,5 px |
| **Loop seam (pixel)** | diferença de silhueta entre frame `N−1→0` e `N−2→N−1` | ≤ 2% dos pixels |
| **Jitter** | segunda derivada de ângulo por osso | ≤ 3°/frame² |
| **Frame duplicado** | hash perceptual entre frames consecutivos | ≤ 1 duplicata (só holds intencionais) |
| **Ordem de camada** | z-order do render vs `layer_order.json` | exato |
| **Estouro de canvas** | bounding box do alpha | dentro de 8 px de margem |
| **Alpha sujo** | pixels com 0 < alpha < 16 na borda | 0 |

O relatório é salvo em `production/qa_reports/DB_CHAR_HERO_GOKU_BASE__anim.json`.

---

## 7. Rubrica humana (30 pontos)

Cada critério de 0 a 5. Aprovação: **≥ 24/30** e **nenhum < 3**.

| Critério | 1 (reprovar) | 3 (aceitável) | 5 (excelente) |
|---|---|---|---|
| **R1 — Integridade visual** | fendas, peças flutuando | sem fendas, overlap visível em 1–2 frames | juntas invisíveis em todos os frames e ângulos |
| **R2 — Peso e timing** | movimento uniforme, flutuante | tem antecipação e assentamento | contraste forte, hitstop, impacto convincente |
| **R3 — Arcos e spacing** | trajetórias retas, espaçamento igual | curvas presentes | spacing expressivo, aceleração clara |
| **R4 — Secundárias** | cabelo/capa rígidos | acompanham com atraso | overshoot, impulso no impacto, vida própria |
| **R5 — Continuidade/loop** | salto visível, jitter | emenda discreta | loop perfeito e sem frames mortos |
| **R6 — Leitura e expressão** | pose ambígua, face errada | pose clara | silhueta icônica, expressão forte em 1 frame |

### 7.1 Ficha de avaliação

```
ASSET: DB_CHAR_HERO_GOKU_BASE     CLIP: attack_light_1     VERSION: 0.1.0
R1 [ ]  R2 [ ]  R3 [ ]  R4 [ ]  R5 [ ]  R6 [ ]
TOTAL: __/30        AUTOMÁTICO: PASS / FAIL
OBSERVAÇÕES:
CORREÇÕES SOLICITADAS:
```

---

## 8. Ciclo de correção

```
renderizar → assistir → marcar frame + defeito → corrigir key/curva/peça → re-renderizar
```

Regras:
- **Um defeito por iteração**, com frame anotado. "Está estranho" não é bug.
- Se o defeito é de **peça** (fenda, pivô), corrige-se a peça, não a animação.
- Se o defeito é de **timing**, corrige-se a curva/duração, não o desenho.
- Se o defeito aparece em 3 clipes diferentes, o problema é do **rig** — volta para o G2.
- Máximo de 3 ciclos por clipe antes de reavaliar a abordagem.
- Cada iteração gera um novo `v0.x.y` e mantém o anterior em `production/rejected/` (histórico).

Defeitos comuns e correção:

| Sintoma | Causa provável | Correção |
|---|---|---|
| Pé escorrega | IK não travado / stride inconsistente | travar alvo do pé e recalcular stride |
| Joelho "estala" | interpolação linear / ângulo passando de 0° | adicionar key intermediária e clamp |
| Braço "de borracha" | escala no slot | remover escala, usar rotação |
| Movimento flutuante | tudo em ease_in_out | inserir holds e ease_in no golpe |
| Loop "pula" | frame de fechamento diferente | igualar pose N à pose 0 |
| Costura no ombro | pivô fora da junta | mover pivô para a cabeça do osso |
| Capa atravessa a perna | ordem de camada / sem colisão | ajustar z e amplitude |
| Ataque sem impacto | sem hitstop / impacto sem hold | adicionar 4–8 frames de hitstop |

---

## 9. ADR-0005 — Congelamento da Matriz

### 9.1 O que congela
| Item | Arquivo | Hash |
|---|---|---|
| Esqueleto | `standards/skeleton_humanoid.json` | SHA-256 |
| Escala/canvas | `standards/canvas_and_scale.json` | SHA-256 |
| Camadas | `standards/layer_order.json` | SHA-256 |
| Paleta | `standards/palette_master.json` | SHA-256 |
| Matriz de clipes | `standards/clip_matrix.json` | SHA-256 |
| Easing | `standards/easing_library.json` | SHA-256 |
| Schemas | `standards/*.schema.json` | SHA-256 |
| Naming | `standards/naming.json` | SHA-256 |
| Visual Bible | `docs/01_VISUAL_BIBLE.md` | SHA-256 |

### 9.2 Certificado
`docs/matrix/FROZEN_MATRIX_v1.0.0.json` contém: versão, data, hashes, resultados dos 18 GIFs, rubrica, aprovador, e a declaração:

> "A Matriz v1.0.0 está congelada. Todo asset a partir desta data deve conformar-se a ela ou apresentar ADR de exceção com plano de migração."

### 9.3 Controle de mudança
- Mudança em item congelado exige **ADR**, justificativa, impacto estimado, plano de migração e nova versão (`v1.1.0` ou `v2.0.0`).
- Assets antigos não são regerados automaticamente; declaram `matrix_version`.
- Pivô, altura e ordem de camada são **breaking** (`v2.0.0`).

### 9.4 Por que congelar antes de escalar
Um erro de 2 px no pivô do ombro, descoberto no personagem 30, custa 30× mais. O congelamento transforma o primeiro modelo em **molde**, não em exceção.

---

## 10. Evidências e armazenamento

```
exports/previews/DB_CHAR_HERO_GOKU_BASE/
  DB_CHAR_HERO_GOKU_BASE__idle__v0.1.0.gif
  ...
  manifest.json            (hashes, render version, data)
production/qa_reports/
  DB_CHAR_HERO_GOKU_BASE__anim.json
  DB_CHAR_HERO_GOKU_BASE__rubric.md
production/session_reports/
  S07_validation.md
```

- GIFs aprovados são imutáveis; correções geram nova versão.
- O `manifest.json` liga cada GIF ao commit e ao hash do rig/clipe.
- Nenhum GIF é editado manualmente depois de gerado.

---

## 11. Critério de saída do G3

- [ ] 18 GIFs existem, com nome e versão corretos.
- [ ] Todos abrem, loopam e têm a duração declarada.
- [ ] Relatório automático: PASS em todas as métricas.
- [ ] Rubrica ≥ 24/30 em cada clipe, nenhum critério < 3.
- [ ] Revisão visual do usuário registrada.
- [ ] Nenhum `TODO` em peça visível.
- [ ] Aprovação assinada em `production/session_reports/S07_validation.md`.

Só então o G4 (congelamento) é iniciado.
