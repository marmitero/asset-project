# 22 — Plano dos problemas 2 e 3

**Status:** plano aprovado para execução. **Nada foi implementado neste documento.**
O problema 1 já está resolvido (ver `docs/21` §9).

Medições feitas em 2026-10-22 com o rig v1.2.0 + paint pass v2, no commit
`aac9e5f`. Todas as réguas abaixo foram medidas, não estimadas.

---

## Problema 2 — contato do pé no chão

### O que foi medido

Para cada clipe, o pixel mais baixo do sprite renderizado (pés sozinhos, sem sombra),
comparado com a linha do chão em `y = 448`:

| clipe | pixel mais baixo | desvio do chão |
|---|---|---|
| `idle` | 448–448 | **0 px** |
| `walk` | 448–449 | +1 px (afunda) |
| `run` | 448–450 | +2 px (afunda) |
| `attack_heavy` | 448–448 | **0 px** |
| `turn_180` | 444–448 | **−4 px (flutua)** |
| `land` | 440–442 | **−6 a −8 px (flutua)** |

E as métricas do `validate_animation.py` hoje:

| clipe | `foot_slip` | `foot_float` |
|---|---|---|
| `walk` | 1,01 | 0 |
| `run` | **1,75** | 0 |
| `attack_whiff` | **1,78** | 0 |
| `idle_combat` | 0 | 1,41 |
| `jump_start` | 0 | 1,48 |
| `turn_180` | 0 | 1,02 |

Limites atuais: `foot_slip` ≤ 2,0 por 12 frames, `foot_float` ≤ 1,5 px.

### A documentação anterior estava errada

O `docs/21` §8 dizia que "o rig pisa 4–5 px **abaixo** da linha do chão por causa
do contorno". **Não é isso.** O sprite afunda no máximo 2 px (`run`). O defeito
real é o oposto: em `land` e `turn_180` o personagem **flutua 4–8 px acima** do
chão. Então não é um problema de contorno — é um problema de *planejamento de
contato*.

### Causa raiz

1. **`ground_clamp` não sabe qual pé está plantado.** Ele acha o pixel mais baixo
   do sprite inteiro e desloca o root até esse pixel encostar em 448. Em `land`
   o joelho/cintura desce mais que o pé, então o clamp "planta" o joelho e o pé
   fica no ar.
2. **Os pés são FK, não IK.** A posição do tornozelo vem da cadeia
   quadril → joelho → tornozelo. Nada no pipeline resolve o tornozelo *para um
   alvo no chão*.
3. **Não existe o conceito de "pé plantado" nos dados do clipe.** O validador
   mede deslizamento e flutuação como heurística, mas o clipe não declara
   "neste trecho este pé está no chão", então nenhuma correção pode ser aplicada
   com segurança.
4. **O offset da sola é um número mágico.** `ankle + 10.4` está escrito à mão em
   `parts_goku.py`, e o traço da bota (3,6 px) não entra na conta.

### Etapas propostas

Cada etapa termina num commit que passa em `validate_animation.py` (23/0) e
`validate_standards.py` (0/0). Nenhuma etapa mexe em clipe que já está correto.

#### E1 — Offset da sola calculado, não digitado
- Calcular `SOLE_OFFSET` a partir do bbox alfa real da peça `foot_*` (pivot →
  pixel mais baixo), em vez de `ankle + 10.4`.
- Expor em `standards/skeleton_humanoid.json` como `sole_offset`.
- **Aceite:** `idle` continua em 0 px de desvio e o número deixa de ser mágico.

#### E2 — Declarar o pé plantado no clipe
- Novo campo por keyframe: `"plant": "f" | "b" | "both" | None` (default `None`).
- Aplicar só onde é obviamente verdadeiro: `idle`, `idle_combat`, `walk`,
  `run`, `land`, `turn_180`, `block_impact`, `cast`, `attack_*` (frames de
  apoio).
- **Aceite:** `validate_animation.py` passa a reportar `foot_ground` por clipe.

#### E3 — IK de dois ossos no pé plantado
- Usar `solve_leg()` (já existe em `aura.pose`) para resolver
  quadril → tornozelo com alvo em `(foot_x, ground_y − sole_offset)`.
- Só quando `plant` marca aquele pé naquele frame; nos demais, FK como hoje.
- Direção do joelho: manter a atual (para frente) e travar por parâmetro, senão
  o joelho inverte em `land`.
- **Aceite:** `|ground_delta| ≤ 1 px` em todo frame declarado como plantado.

#### E4 — `ground_clamp` restrito
- Com E3, o clamp global deixa de ser necessário nos clipes terrestres.
  Passar a aplicá-lo **só** em `fall`/`jump_start`/`jump_land`, onde o corpo
  realmente está no ar.
- **Aceite:** `land` passa de −6/−8 px para 0 ± 1 px; `turn_180` de −4 para 0 ± 1.

#### E5 — Novos limites no validador
- `foot_ground` (novo): ≤ 1,0 px nos frames com `plant`.
- `foot_slip`: baixar o limite de 2,0 para 1,2 depois que `run` e `attack_whiff`
  estiverem em IK — os 1,75/1,78 de hoje passam raspando.

#### E6 — Regenerar e julgar a 1×
- `tools/render_set.py` + `tools/pack.py`; julgar **em escala 1×** (regra do
  projeto: julgar a 1× primeiro).
- **Aceite:** `walk` e `run` sem "patinação" visível; `land` sem flutuar.

### Riscos

| risco | mitigação |
|---|---|
| IK muda a silhueta da perna (o joelho pode estufar) | travar o ângulo do joelho e validar por clipe, não em lote |
| `ground_clamp` e IK brigando pelo mesmo pixel | E4 remove o clamp onde há IK |
| `run` tem as duas pernas no ar em parte do ciclo | `plant: None` nos frames de voo; o validador ignora esses frames |
| perna esticando além do alcance → joelho travado | `solve_leg` precisa devolver falha explícita; nesse frame, cai para FK e o validador avisa |

### Ordem de execução

E1 → E2 → E3 → E4 → E5 → E6. E1 e E2 são de baixo risco e já entregam
instrumentação; o risco real está concentrado em E3.

---

## Problema 3 — proporção da cabeça

### O que foi medido

| grandeza | valor |
|---|---|
| altura do sprite (ponta do cabelo → sola) | **229 px** |
| altura nominal do personagem | 220 px |
| cabeça (crânio + contorno) | **46 px** |
| razão corpo / cabeça | **4,78 – 4,98** |
| alvo AQWorlds | **≈ 1/6** |
| cabeça para chegar a 1/6 (corpo 220) | **36,7 px** |

A cabeça atual é ~25 % maior do que o alvo. É o que dá a leitura "chibi" em vez
de "adulto estilizado".

Stack vertical atual, em coordenadas absolutas (y negativo = para cima):

| op | y |
|---|---|
| topo do crânio | −213,4 |
| `EYE_Y` | −190,0 |
| boca | −177,0 |
| queixo (base do crânio) | −169,6 |
| pescoço (cápsula) | −170,0 → −158,0 |

O crânio ocupa 43,8 px de polígono, mais o contorno. Os olhos ficam a 23 px do
topo e a boca a 13,4 px do queixo.

### Causa raiz

Não é um número errado — é que **todas as ops faciais são px absolutos** num
crânio de 46 px. Não existe uma constante `HEAD_H`; o tamanho está espalhado
pelo polígono do crânio, por `EYE_Y`, pela boca, pelas sobrancelhas e pelo
pescoço. Por isso encolher a cabeça "na mão" quebra o espaçamento
olho/sobrancelha/boca — que é exatamente a armadilha já registrada no projeto
(*"layered fixes in a 46 px skull: compute the vertical stack first"*).

### Opções

| opção | resultado | veredito |
|---|---|---|
| **A** — encolher a cabeça para 38 px, corpo em 220 | razão 5,79 | **recomendada** |
| B — manter a cabeça e crescer o corpo para 276 px | razão 6,0 | rejeitada: estoura o canvas 512² e a linha do chão |
| C — passo intermediário em 42 px | razão 5,24 | usar só como etapa de A, não como destino |

### Etapas propostas

#### E1 — Parametrizar antes de encolher
- Introduzir `HEAD_H = 46.0` e `HEAD_CY` e reescrever o crânio, `EYE_Y`, boca,
  sobrancelha, orelha e pescoço em função de `HEAD_H` (frações).
- **`HEAD_H = 46` neste commit: nenhuma mudança visual.** É só refactor.
- **Aceite:** os 18 GIFs saem idênticos (comparar por hash de pixels).

#### E2 — Fechar o stack vertical
- Escrever o stack de cima para baixo em frações de `HEAD_H`:
  topo do crânio → linha do cabelo → sobrancelha → centro do olho → nariz →
  boca → queixo.
- Conferir aritmeticamente que cada elemento cabe, antes de renderizar.
- **Aceite:** tabela de frações registrada no doc, somando 1,0.

#### E3 — Encolher para 42 px
- `HEAD_H = 42`. Ajustar só o pescoço (fica 4 px mais longo) e o pivot.
- Regenerar e **julgar a 1×**.
- **Aceite:** olho ≥ 3,2 px de altura a 1×; sobrancelha não encosta no cílio.

#### E4 — Encolher para 38 px
- Mesmo procedimento. Aqui o limite físico aparece: com olho de 3,2 px e
  cílio de 1,2 px, o crânio de 38 px ainda comporta, mas a pupila fica com
  ~1,5 px.
- **Ponto de decisão do usuário:** se em 38 px o rosto perder legibilidade a
  1×, parar em 40–42 px (razão ~5,4) e aceitar que o pacote é um pouco mais
  "jovem" que o AQW.

#### E5 — Cabelo
- Os espinhos somam ~9 px acima do crânio e passam a dominar a silhueta quando
  a cabeça encolhe. Reduzir a altura dos espinhos proporcionalmente, senão a
  razão medida no sprite (229 px) não melhora na prática.

### Medição de aceite

- Nova métrica em `validate_standards.py`: `head_ratio = altura_sprite / HEAD_H`,
  com faixa aceitável **5,5 – 6,0**.
- Conferir em `idle`, `attack_light_1` e `hurt_crit` a 1× — são os três onde o
  rosto mais aparece.
- Nenhum clipe pode piorar as métricas de fluidez (o crânio muda de massa, a
  cadeia secundária do cabelo pode reagir).

### Riscos

| risco | mitigação |
|---|---|
| rosto ilegível a 1× | decisão explícita de parar em 40–42 px (E4) |
| cabelo passa a dominar a silhueta | E5 |
| sockets de `head`/`forehead`/`mouth` desalinham | recalcular a partir de `HEAD_H`, não de px absolutos |
| offsets do `standards/player_offsets` (equipamento) apontam para o crânio antigo | revisar `docs/06` e os offsets de `helm`/`hair` |

### Ordem de execução

E1 → E2 → E3 → (decisão) → E4 → E5. E1 é obrigatório: encolher antes de
parametrizar é o que já deu errado no v1.

---

## Resumo de esforço

| problema | etapas | risco | bloqueia freeze? |
|---|---|---|---|
| 2 — contato do pé | 6 | médio (IK) | sim: `land` flutuando é visível |
| 3 — cabeça | 5 | alto (rosto a 1×) | sim: é a maior diferença de estilo vs AQW |

Nenhum dos dois bloqueia a publicação do pacote atual: o G3 segue válido com o
problema 1 resolvido, e os dois planos acima são o escopo do **G4 (freeze)**.
