# D7 — Direção de arte: atlas pintado por IA vs. renderizador vetorial

**Status:** decisão **aberta** — este documento é evidência, não conclusão fechada.
**Data:** 2026-10-22
**Pergunta do usuário:** "a estética ficará melhor quando tratarmos com imagens geradas? ou manterá o padrão atual? achei meio feio"

Este documento existe porque a pergunta é boa e merece resposta medida, não opinião.
Quatro rotas foram testadas de verdade, com código rodando. Os artefatos estão em
`experiments/atlas_proto/out/` e `experiments/style_probe/out/`.

---

## 1. O que foi construído

Um pipeline funcional que **pinta o rig vetorial com arte gerada por IA e continua animando**:

| Módulo | Função |
|---|---|
| `experiments/atlas_proto/rest_ref.py` | renderiza a pose de repouso do rig como referência para a IA |
| `experiments/atlas_proto/cut_atlas.py` | matte do fundo cinza, registro no rig, recorte nas 18 peças, remontagem |
| `experiments/atlas_proto/landmark.py` | registro por perfil de largura (DTW por linha) — alinha juntas, não só a caixa |
| `experiments/atlas_proto/normalize.py` | força paleta mestra + contorno oficial numa peça gerada |
| `experiments/atlas_proto/headswap.py` | troca uma única peça (cabeça) por arte de IA |
| `experiments/atlas_proto/anim_test.py` | compara os dois rigs no mesmo clipe |
| `experiments/atlas_proto/motion_cmp.py` | GIF lado a lado em movimento |
| `experiments/atlas_proto/scale_test.py` | comparativo em escala de jogo e em alta resolução |

Reproduzir: `python3 experiments/atlas_proto/<script>.py` (requer pillow, numpy, opencv).

---

## 2. Resultado medido — o achado que decide tudo

**A cinemática do rig pintado por IA é idêntica à do vetorial.**

```
amostras de osso comparadas: 17980
desvio máximo: 0.0 px   (23 clipes × todos os ossos × todos os frames)
```

Isso não é coincidência: a IA pinta a *pele*, o rig continua sendo a *fonte da
verdade* do movimento. Portanto **os 11 critérios de fluidez do doc 05 §6 passam
por construção** — não existe cenário em que o caminho IA degrade a animação,
porque a animação não passa pela IA.

Consequência: o critério de aceitação nº 1 do projeto (fluidez) **não** é o que
decide esta escolha. O que decide é qualidade de imagem e custo.

---

## 3. As quatro vias, no mesmo frame, mesma câmera

Arquivo: `experiments/atlas_proto/out/veredito_4_vias.png`

| Via | Fluidez | Qualidade de imagem | Custo por personagem |
|---|---|---|---|
| **A. Vetor (atual)** | ✅ aprovada (23/0) | fraca: chapada, silhueta de manequim | ~0 (determinístico) |
| **B. Arte IA solta** | ❌ não anima | excelente | ~1 imagem |
| **C. Atlas corpo inteiro por IA** | ✅ idêntica | **ruim**: emendas erradas, manchas | 1 imagem + 1 h de ajuste |
| **D. IA só na cabeça** | ✅ idêntica | **boa**, mas parece colada | 1 imagem por peça |

---

## 4. Por que "atlas de corpo inteiro" falhou (e não é falta de esforço)

Tentei quatro correções sucessivas e cada uma expôs uma camada do problema:

1. **Escala global** (bbox da silhueta) → alinha a altura total, mas não as juntas.
2. **Alinhamento por perfil de largura (DTW por linha)** → cobertura do rig subiu
   para **96,8%**, o que parecia resolver. Não resolveu.
3. **Erosão de 1 px na máscara** → matou a borda pontilhada, mas não o erro de fundo.
4. **Passe de normalização de paleta e contorno** → unificou a cor, mas não o desenho.

**A causa raiz é irredutível:** a IA desenha o personagem com proporções internas
diferentes das do rig. Ela fez um corpo de ~7 cabeças onde o rig tem 4,5. Nenhum
alinhamento global conserta isso, porque a máscara do braço do rig cai sobre o
tronco da arte gerada — visível na folha de peças
(`experiments/atlas_proto/out/`).

Além disso, duas falhas de matte apareceram e são sistêmicas:
- a IA **não entrega transparência** — o recorte é sempre estimativa;
- o alpha da borda gera **manchas escuras** ao reduzir ~5× (resolvido com
  `INTER_AREA` em vez de `INTER_LANCZOS4`, que tem ringing).

---

## 5. Por que "IA só na peça isolada" funciona melhor

Quando o alvo é pequeno, isolado e a IA não precisa inventar a articulação, o
resultado muda de patamar. A cabeça gerada isoladamente
(`experiments/atlas_proto/out/ai_head.jpg`) tem traço, olho, mecha e sombreado
muito superiores ao vetorial, e o registro é trivial: basta preencher a caixa do
conjunto cabeça+rosto+franja.

Problema remanescente: **coesão**. Uma peça de IA ao lado de um corpo vetorial
parece colagem — traço mais grosso, paleta mais quente. O passe
`normalize.py` aproxima (quantiza para a paleta mestra + contorno oficial), mas
não iguala o desenho.

---

## 6. Recomendação

**Não abandonar o vetor. Usar IA onde ela é estruturalmente superior.**

Divisão proposta por camada do pacote:

| Camada | Técnica | Motivo |
|---|---|---|
| Corpo animado (29 slots) | **vetor**, com o paint pass v2 | precisa de 23 clipes coerentes; IA não garante coerência entre estados |
| Retratos / bustos de diálogo | **IA** | imagem estática, sem restrição temporal — onde a IA ganha de lavada |
| Ícones de item, skills, UI | **IA** | ~60 assets estáticos, custo altíssimo em vetor |
| Fundos de mapa, 2.5D | **IA** | estático, parallax por camadas |
| Skins "premium" de 1 personagem | **IA por peça**, com `normalize.py` | aceitável se o pacote base já estiver congelado |

O que **não** fazer: gerar frame a frame por IA (destrói fluidez — flicker, sem
contato de pé, sem loop fechado; viola o critério de aceitação do G3).

### Próximo passo imediato

O paint pass v2 (7 defeitos do doc `experiments/style_probe/README.md`) continua
sendo o melhor retorno por hora trabalhada: ~1 dia, sem risco, e resolve a maior
parte do "achei meio feio". Depois dele, reavaliar se ainda incomoda.

---

## 7. ADR-0007 (proposta, a confirmar pelo usuário)

> **Aceito:** o renderizador vetorial permanece a fonte de verdade da animação.
> **Aceito:** arte gerada por IA é adotada para assets estáticos (retratos,
> ícones, UI, fundos) sem restrição temporal.
> **Rejeitado:** gerar frames de animação por IA.
> **Condicional:** atlas de peças por IA fica disponível como pipeline alternativo
> (`experiments/atlas_proto/`), sem entrar no pacote canônico até o G4.

---

## 8. Paint pass v2 — executado (2026-10-22)

Depois da decisão de manter o vetor, o paint pass v2 foi implementado. **Dois bugs
reais do renderizador** apareceram no caminho, e ambos afetavam todo o pacote
desde o G2:

### Bug 1 — `auto_shadow` / `auto_highlight` pintavam a peça inteira

A implementação deslocava a silhueta no sentido (dx,dy) e **intersectava** com a
base. A interseção de uma silhueta com ela mesma deslocada 3 px é ~90 % da área.
Medido num antebraço de 4.067 px: **2.447 px na cor de sombra e ZERO na cor base**.

Era a causa principal do aspecto chapado e "sujo" dos membros: a cor base
praticamente não existia.

Correção: **subtração** (`base − base_deslocada(−s)`), que produz uma faixa na
borda oposta ao deslocamento, com espessura limitada a 10 % da peça.

### Bug 2 — `capsule_offset` cortava o membro ao meio

`shapes.limb()` usava `capsule_offset`, que devolve uma cápsula do **mesmo
tamanho**, só deslocada. Metade dela caía fora do membro e o `clip_fill` cortava
reto no meio — virando uma **banda escura atravessando o braço**.

Correção: `edge_band()`, que constrói a faixa rente à borda (offset para dentro,
não cápsula deslocada).

### Redesenho aplicado

| Peça | Antes | Depois |
|---|---|---|
| crânio | 46 px estreito | +3 px por lado, mais área para o rosto |
| olho | esclera grande + pupila mínima | íris preenche ~60 %, cílio fino, brilho |
| sobrancelha | fundida no cílio (máscara preta) | separada por 3 px, mais fina |
| pescoço | **não existia** | cápsula do queixo ao decote, com sombra |
| tronco | "saco" reto | silhueta em V, decote com sombra interna, nó da faixa, 6 dobras |
| braço | cano | deltoide com bulge, munhequeira, mão maior, rim light |
| perna | cano | coxa com volume, topo de bota, cadarço no cano |
| paleta | sombra 0.72 | rampa mais funda, outlines quentes, `back_darken` 0.74 |

### Resultado

- 23 clipes · **0 falhas** (nenhuma métrica de fluidez mudou)
- 18 GIFs regerados (7,7 MB, eram 6,8)
- Comparativo em escala real: `experiments/style_v2/v1_vs_v2_1x.png`

O que o v2 **não** resolveu: ver §9 (aberto) e §10 (resolvido).

---

## 9. Problema 1 resolvido — braço de trás (2026-10-22)

### Diagnóstico

A hipótese inicial era z-order. **Estava errada**: o braço de trás já era
desenhado atrás do tronco (z 60 < 90). O defeito tinha três camadas:

1. **Pose.** `attack_whiff` f14 tinha `spread_b: 26`, que levava o antebraço de
   trás a atravessar a *lateral* do tronco. Medido: só **31,8 %** do braço
   ficava visível — o resto estava dentro do tronco. A sobra era uma lasca bege
   na borda esquerda, que lia como excrescência.
2. **Geometria do rig.** O braço superior de trás tem ~33 px (ombro → cotovelo)
   enquanto o ombro está a 25 px do eixo e o tronco tem ~20 px de meio-largura.
   **O braço superior nunca consegue sair da silhueta do tronco em vista 3/4.**
   Nenhuma pose resolve isso: qualquer pose que exponha o antebraço deixa o
   braço superior enterrado, e o membro lê como desmembrado.
3. **Decisão por peça.** Qualquer heurística que esconda peças isoladamente
   produz membro desmembrado: o braço some e o antebraço fica flutuando.

### Correção

**Ordem de camadas** (`standards/layer_order.json`): o membro de trás passa a
ser desenhado **acima do tronco**, como no AQWorlds.

| slot | antes | depois |
|---|---|---|
| `upper_arm_b` | 60 | **92** |
| `forearm_b` | 61 | **93** |
| `hand_b` | 62 | **94** |

O `back_darken = 0.74` continua aplicado, então o braço mantém a leitura de
profundidade. Ele fica abaixo de `thigh_f` (100), `head` (110) e do braço da
frente (130) — a cabeça ainda cobre o braço quando ele passa atrás dela.

**Pose** (`tools/aura/clips.py`, `attack_whiff` f14): `spread_b` 26 → **40** e
`elbow_b` −30 → **−60** — cotovelo para fora, antebraço caindo, em vez de
atravessar a lateral do tronco.

### O que foi tentado e descartado

- guard de oclusão por peça (medir fração visível e esconder lascas): **removido**.
  Calibrado por histograma chegou a apagar braço legítimo no idle e produzia
  membro desmembrado quando só o antebraço passava do limite.
- `spread_b` alto (60–100): resolvia a visibilidade (80–91 %) mas jogava o
  antebraço para trás da cabeça, virando "coxa de frango" ao lado do rosto.
- fade parcial do braço: virava braço fantasma sobre o gi no `walk`.

### Verificação

- 23 clipes · **0 falhas**; `validate_standards.py` 0 erros
- contato visual conferido em `idle`, `walk`, `run`, `idle_combat`,
  `attack_whiff` f13/f14, `attack_light_1` f8, `attack_heavy` f12, `hurt_crit`,
  `cast`, `block_impact`, `turn_180`

### Efeito colateral corrigido junto

O pescoço era o **último** op de `_torso` (para o gi não cobrir), mas com a
cabeça inclinada ele aparecia como bloco solto sobre o ombro. Passou para o
início de `_torso` (atrás do gi), mais estreito e mais baixo: agora só aparece a
parte acima do decote e ele conecta queixo → tronco em todas as poses.

---

## 10. Problemas 2 e 3 — planos
