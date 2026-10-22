# PLANO DE EXECUÇÃO — PROJETO AURA
### Asset Pack 2D modular · identidade Dragon Ball · linguagem visual e de movimento de AdventureQuest Worlds

> **Status:** Fase 0 (Auditoria e Planejamento) e Fase 1 (Documentação / Visual Bible) concluídas nesta sessão.
> **Nenhum asset de arte foi gerado ainda.** Todo o material produzido até aqui é especificação, padrão técnico, esquema de dados e infraestrutura de produção.
> **Próxima fase:** Fase 2 — criação do primeiro modelo (vertical slice) e validação por GIF.

---

## 1. Qual é a ideia do projeto

O repositório `asset-project` contém três documentos:

| Documento | Papel |
|---|---|
| `docs/asset_guide1.md` | Guia técnico-artístico do estilo AQW: paper-doll, camadas, pivôs, animação, UI, cenários. |
| `docs/asset_guide2.md` | Pesquisa profunda sobre o estilo AQW: lineart, cel-shading, modularidade, classes, VFX, HUD, mapas. |
| `docs/master-prompt.md` | Briefing-mestre: **asset pack temático de Dragon Ball** com **estrutura e estética AQW**, 18 critérios de aceitação, orçamento de gerações, pipeline e fases. |

A ideia, consolidada, é:

> **Construir uma biblioteca de produção 2D completa — personagens modulares (paper-doll), animações, equipamentos, VFX, cenários, UI e metadados — que permita a um desenvolvedor ou a uma IA montar um MMORPG 2D de ação em tempo real com a "alma" de AdventureQuest Worlds, vestido com a identidade canônica de Dragon Ball.**

O produto final **não é uma coleção de ilustrações**. É um **sistema**: peças soltas com pivôs exatos + rigs + timelines + spritesheets + JSON + documentação, de modo que qualquer engine 2D (Godot, Unity, GameMaker, web) consiga montar, animar e equipar um personagem sem redesenhar nada.

### 1.1 Por que AQW é a referência e o que exatamente copiamos dela

Copiamos a **linguagem**, jamais arquivos:

- **Silhueta cartoon-heroica** com contorno preto limpo, cel-shading de 3 tons e luz única vinda de cima/frente.
- **Paper-doll**: corpo em 21 camadas, equipamentos que substituem peças em vez de cobrir um corpo base.
- **Animação por interpolação de recortes** (o "MovieClip" do Flash), não frame-a-frame.
- **Leitura de combate**: posicionamento 2.5D em plano XY, auto-attack + 5 skills, alvo travado, números de dano flutuantes.
- **HUD de MMO clássico**: retrato + HP/MP no topo-esquerda, barra de skills embaixo, painéis opacos com moldura.
- **Cenários em camadas** com parallax leve e personagem legível em primeiro plano.

Não copiamos: sprites, ícones, mapas, personagens, nomes de itens, logotipos ou qualquer arquivo da Artix Entertainment. A estética Dragon Ball é aplicada como **identidade canônica de referência**, com as ressalvas de propriedade intelectual registradas em `LICENSE_NOTES.md`.

### 1.2 O que o produto precisa provar (critério de sucesso)

Um agente de IA (ou um dev) deve conseguir, **usando somente o pack**:

1. Montar um personagem jogável a partir de peças soltas e pivôs documentados.
2. Trocá-lo de armadura, arma, capacete e capa sem redesenho.
3. Reproduzir o ciclo completo de combate (idle → aproximação → ataque → crítico/erro → dano recebido → morte).
4. Montar um mapa jogável com camadas, colisão, oclusão e portais.
5. Montar a HUD e os painéis funcionais.
6. Entender as regras de estilo o bastante para gerar **novos assets compatíveis** seguindo os mesmos schemas.

---

## 2. Decisões estruturais (tomadas por mim, registradas)

O `master-prompt.md` deixa margem para decisões operacionais. Estas são as escolhas que definem o projeto. Todas têm justificativa técnica e impacto direto na fluidez.

| # | Decisão | Por quê |
|---|---|---|
| **D1** | **Pipeline "vector-first"**: a arte é autorada como peças vetoriais determinísticas (formas + recorte de sombra + contorno), com rig e animação em dados, renderizadas por um renderizador próprio em Python/Pillow. | Garante **pivô exato**, **peças 100% reutilizáveis** e **interpolação real** — os três requisitos que modelos de difusão não entregam de forma consistente entre dezenas de peças. Elimina o maior risco do projeto: 21 recortes gerados por IA que não encaixam. |
| **D2** | **A geração de imagem por IA é usada para referência/concept e para cenários pintados**, nunca como fonte de peças modulares de personagem. | Mantém o melhor dos dois mundos: conceito rápido onde a consistência não é crítica; determinismo onde ela é obrigatória. |
| **D3** | **Dois formatos de entrega**: (a) **skeletal** — PNGs de partes + JSON de rig/timeline, animado em runtime a 60 fps; (b) **baked** — spritesheets e GIFs gerados pelo mesmo rig, para engines simples e para validação visual. | Engine-agnóstico de verdade. AQW clássico era vetorial em runtime; AQW Infinity é bitmap com bones. Entregamos os dois caminhos a partir de uma fonte única de verdade. |
| **D4** | **Chave de autoria em 24 fps, amostragem de render em 60 fps.** | Preserva o "timing de desenho" do Flash (peso, holds, snappy attacks) e entrega fluidez de movimento moderna. O erro clássico é interpolar tudo em 60 — fica "escorregadio" e perde personalidade. |
| **D5** | **Fluidez é arquitetura, não polimento.** Cinco mecanismos obrigatórios desde o primeiro modelo: curvas C1, arcos, overlap/follow-through, foot-planting por IK e movimento secundário procedural (cabelo/capa/aura). | É o pedido central do usuário. Sem isso no rig, nenhuma quantidade de frames resolve. |
| **D6** | **Gate de congelamento da Matriz (G4)**: nenhum segundo personagem é produzido antes de o primeiro passar em todos os GIFs de validação e a Matriz ser assinada e travada por hash. | Evita retrabalho em escala. Um erro de pivô descoberto no personagem 30 custa 30× mais. |
| **D7** | **Primeiro modelo = Goku adulto (base), corpo "heroico masculino A" (6 cabeças).** | Personagem mais reconhecível da franquia, anatomia reaproveitável por Vegeta/Gohan/Trunks/Yamcha, e o gi laranja é o teste mais duro de contraste e legibilidade. |
| **D8** | **Escala canônica**: 1 unidade = 1 px; personagem adulto = **220 px** de altura; tela de referência 1280×720; canvas de render 512×512 com linha de chão em y=448. | Números fechados, conversíveis por potência de 2. Toda a documentação usa essa régua. |
| **D9** | **Camadas**: 29 slots de render = 21 camadas canônicas do paper-doll + 8 extensões (sombra, pet, aura back/front, asas, face, FX de ataque, split helm/cabelo), com ordem fixa em `standards/layer_order.json`. | Consistência entre todos os assets e z-fighting zero. |
| **D10** | **IDs imutáveis** no padrão `DB_[CAT]_[SUB]_[NAME]_[VARIANT]_[STATE]`, versionamento semântico por asset. | Rastreabilidade e migração segura. Nunca renomear silenciosamente. |
| **D11** | **Orçamento de gerações**: teto de 10 chamadas de imagem por sessão de produção, 6–8 para novos, 2–4 para correção — **quando houver geração de imagem**. Sessões de código/rig não consomem o orçamento. | Regra do master-prompt preservada, com semântica adaptada ao pipeline determinístico. |
| **D12** | **Idioma**: documentação em pt-BR; identificadores, nomes de arquivos, campos JSON e código em inglês. | O usuário trabalha em português; máquinas e engines trabalham em inglês. |
| **D13** | **Estrutura de pastas do master-prompt preservada** (`dragonball-aqw-asset-pack/`), com uma adição: `standards/` (schemas e constantes legíveis por máquina) e `tools/` (renderizador, validador, empacotador). | O pack precisa ser consumível por IA: JSON + schema vale mais que prosa. |

---

## 3. O princípio central: fluidez de sprites

Fluidez, aqui, tem definição mensurável. Um sprite é fluido quando, reproduzido a 60 fps:

1. **Não há costura visível** nas articulações em nenhum frame do arco de movimento (pivôs coincidentes, overlap de 2–3 px nas juntas).
2. **O movimento tem aceleração** — nenhuma rotação de membro é linear; toda ação tem antecipação, aceleração e assentamento (easing + spacing).
3. **O corpo tem massa** — o centro de gravidade sobe e desce em ciclo de 2 tempos; o impacto tem hitstop.
4. **Há sobreposição de ação** — cabelo, capa, aura e arma chegam 1–3 frames *depois* do corpo e continuam depois que ele para.
5. **O pé não escorrega** — contato plantado por IK durante toda a fase de apoio.
6. **O loop fecha** — o frame N+1 é idêntico ao frame 1 em pose, ou a emenda é invisível (diferença de centróide e de ângulo < 0,5 unidade).

Esses seis critérios são a rubrica de aprovação do Gate G3 (§5) e estão operacionalizados em `docs/05_FLUIDITY_AND_GIF_VALIDATION.md`.

### 3.1 Como a fluidez é garantida tecnicamente

| Mecanismo | Implementação |
|---|---|
| **Curvas C1** | Timelines guardam keyframes com `ease` por segmento; a biblioteca de easing cobre quad/cubic/back/elastic/bounce + Catmull-Rom para trajetórias. Nenhum movimento de membro usa `linear`. |
| **Arcos** | Rotação de ombro/quadril combinada com translação do root em curva de Bézier, nunca em linha reta. |
| **Overlap / follow-through** | Cadeias secundárias (`cape_01..03`, `hair_back_01..02`, aura) com atraso configurável em frames e amortecimento, dirigidas por *spring* simples ou por keys defasadas. |
| **Foot planting** | IK de 2 ossos para perna; alvo do pé travado no mundo durante a fase de apoio; tornozelo resolve o ângulo. |
| **Squash & stretch** | Escala não-uniforme no tronco/cabeça em impactos, com volume preservado (sx·sy ≈ 1). |
| **Hitstop / impacto** | Evento `hit_stop` congela 2–4 frames de 60 (33–66 ms) no frame de impacto. |
| **Amostragem** | Keys em 24 fps; render a 60 fps com interpolação; export GIF a 25 fps e APNG a 60 fps. |
| **Validação** | Métricas automáticas (jitter de pivô, slip do pé, emenda de loop) + revisão visual humana em GIF. |

---

## 4. Fluxo de execução solicitado

O usuário definiu o fluxo. Ele está implementado como **gates sequenciais** — cada gate tem entregável, critério objetivo e artefato de assinatura. Nada avança sem o gate anterior.

```
G0  DOCUMENTAÇÃO ──► G1  INFRA/PADRÕES ──► G2  PRIMEIRO MODELO ──► G3  VALIDAÇÃO GIF
                                                                          │
                                        G5  ESCALA (resto do pack) ◄── G4  CONGELAMENTO DA MATRIZ
```

### G0 — Documentação (concluído nesta sessão)
Visual Bible, spec técnica, padrão de animação, protocolo de fluidez, equipamentos, VFX, cenários, UI, naming/metadados, integração, QA, pipeline, roadmap, catálogo, blueprint de jogo, handbook para IA, glossário. **Critério:** 20 documentos + 10 padrões legíveis por máquina, todos internamente consistentes.

### G1 — Infraestrutura e padrões executáveis
Schemas JSON, constantes de canvas/camadas/esqueleto, manifesto vazio válido, ledger, backlog, estado de continuidade, validador de integridade, renderizador de prova. **Critério:** `tools/validate_standards.py` roda e acusa zero erros nos documentos e JSONs existentes.

### G2 — Primeiro modelo (Vertical Slice)
Goku adulto base completo: corpo nu (peças), gi, cabelo, sapatos, luvas, faixa; rig; 9 clipes mínimos; previews. **Critério:** 18 slots de corpo + equipamento montados sem costura; todos os clipes reproduzíveis; nenhuma peça faltante.

### G3 — Validação com GIF (o gate mais importante)
18 previews (idle, idle_combat, walk, run, jump/land, ataque leve, ataque pesado, combo, cast, **miss/whiff**, **crítico**, **dano leve**, **dano crítico**, morte, block/dodge, troca de equipamento, turnaround de silhueta, montagem de combate). **Critério:** rubrica de fluidez ≥ 24/30 e nenhum critério < 3; validações automáticas passando; aprovação visual do usuário.

### G4 — Congelamento da Matriz
Publicação de `matrix/FROZEN_MATRIX_v1.0.0.json` com hashes SHA-256 de: esqueleto, proporções, paleta, pesos de linha, ordem de camadas, matriz de clipes e schemas. Certificado assinado. **Critério:** qualquer mudança posterior exige ADR + plano de migração.

### G5 — Escala
Personagens, transformações, equipamentos, inimigos, bosses, pets, VFX, cenários, UI, atlas, exemplos de integração, QA final.

---

## 5. Cronograma por fases e sessões

Cada "sessão" é uma unidade de trabalho com objetivo, orçamento e relatório próprio (padrão do master-prompt §25).

| Fase | Sessões | Objetivo | Entregável central | Gate |
|---|---|---|---|---|
| **0 — Auditoria** | S00 | Ler docs, auditar ferramentas, decidir arquitetura | este plano + relatório de capacidades | G0 parcial |
| **1 — Documentação** | S01 | Padrões completos, schemas, backlog | `docs/` + `standards/` + `production/` | **G0** |
| **2 — Primeiro modelo** | S02–S06 | Corpo, gi, cabelo, rig, 9 clipes | `characters/canonical_heroes/goku/base/` | **G2** |
| **3 — Validação GIF** | S07 | Renderizar 18 previews, medir, corrigir | `exports/previews/DB_CHAR_HERO_GOKU_BASE_*` | **G3** |
| **4 — Congelamento** | S08 | Travar Matriz v1.0.0 | `matrix/FROZEN_MATRIX_v1.0.0.json` | **G4** |
| **5 — Heróis** | S09–S14 | Vegeta, Gohan, Piccolo, Trunks, Kuririn, Bulma | 6 personagens com camadas e clipes | — |
| **6 — Transformações** | S15–S18 | SSJ1–3, SSG, SSB, UI, Golden Frieza | swaps de cabelo/aura/olhos + VFX | — |
| **7 — Equipamentos** | S19–S24 | 8 sets de armadura, 50 armas, 30 helms/capas | peças modulares + ícones | — |
| **8 — Inimigos** | S25–S31 | 20 comuns, 10 elites, 10 bosses | rigs próprios + retratos | — |
| **9 — Pets** | S32–S34 | 20–50 mascotes | rigs simplificados 4–8 ossos | — |
| **10 — VFX** | S35–S40 | 40+ técnicas, projéteis, explosões, auras | kits componentizados | — |
| **11 — Cenários** | S41–S48 | 8 mapas 2.5D completos | camadas, tiles, colisão, props | — |
| **12 — UI** | S49–S54 | HUD + 11 telas + 100 ícones | 9-slice, estados, atlas | — |
| **13 — Integração/QA** | S55–S60 | exportadores, exemplos Godot/Unity/web, QA final | `examples/` + relatório | **G5** |

> As sessões são estimativas de granularidade, não promessas de calendário. O ritmo real depende do tempo de render/validação.

---

## 6. A Matriz (o que congela no G4)

"The Matrix" não é uma imagem: é o **conjunto de verdade** que garante que o asset 400 encaixe no asset 1.

1. **Esqueleto** — nomes de ossos, hierarquia, posição de repouso, comprimentos, limites articulares.
2. **Proporções** — 6 cabeças, medidas de cada segmento, mãos/pés, ângulo de repouso.
3. **Pivôs** — coordenada exata de cada junta, em px, no canvas 512².
4. **Camadas** — as 24 entradas de z-order, sem exceções.
5. **Paleta** — cores canônicas por personagem/transformação/material + rampa de 3 tons.
6. **Pesos de linha** — 3,0 px externo / 1,8 px interno (a 220 px de altura), com regra de escala.
7. **Matriz de clipes** — IDs, duração em frames, loop, hit frames, eventos, janelas de cancelamento.
8. **Schemas** — rig, animação, manifesto.
9. **Naming** — prefixos, sufixos, versionamento.

Congelar = publicar hash de cada item. Alterar depois = ADR + nova versão + migração documentada.

---

## 7. Estrutura do repositório

```
asset-project/
├── PLAN.md                         ← este plano
├── dragonball-aqw-asset-pack/
│   ├── README.md · VERSION.md · LICENSE_NOTES.md · asset_manifest.json
│   ├── docs/                       ← 19 documentos + matriz de congelamento
│   ├── standards/                  ← JSON/schema legíveis por máquina
│   ├── references/                 ← paletas, pranchas de proporção, folhas de personagem
│   ├── characters/                 ← base_bodies, canonical_heroes, villains, npcs, transformations, rigs
│   ├── equipment/                  ← armor, helmets, hairstyles, capes, gloves, boots, accessories, weapons
│   ├── enemies/ · pets/ · skills/ · environments/ · ui/
│   ├── exports/                    ← png, spritesheets, atlases, metadata, previews
│   ├── production/                 ← ledger, backlog, registry, continuity, relatórios, QA
│   ├── examples/                   ← cenas de integração por engine
│   └── tools/                      ← renderizador, validador, empacotador
└── docs/                           ← documentos-fonte originais (não alterar)
```

---

## 8. Entregáveis finais (o que o pack deve conter)

| Categoria | Meta | Observação |
|---|---|---|
| Rigs base | 10+ | humano M/F, musculoso, infantil, saiyajin M/F, namekuseijin, majin, androide, criatura pequena, quadrúpede, boss gigante, asas/cauda |
| Personagens jogáveis/NPCs | 30+ | com peças, rig e clipes |
| Transformações | 30+ | swaps + aura + VFX de ativação |
| Sets de armadura | 20+ | modulares, com máscaras de cor |
| Armas | 50+ | 8 categorias, grip points |
| Helms/cabelos/acessórios | 30+ | hat vs. morph |
| Pets | 20–50 | rigs de 4–8 ossos |
| Inimigos comuns | 20+ | idle/walk/attack/hit/death |
| Elites | 10+ | |
| Bosses | 10+ | escala própria, multi-fase |
| Mapas 2.5D | 8 | camadas, tiles, colisão, oclusão |
| Habilidades/VFX | 40+ | componentizados (cast/acúmulo/projétil/impacto) |
| Ícones | 100+ | 64/128/256, 5 estados |
| UI | 12 telas | 9-slice, estados, atlas |
| Documentação | 20 docs + schemas | suficiente para uma IA gerar novo conteúdo compatível |

---

## 9. Critérios de aceitação (Definition of Done)

Um asset só é `APPROVED` quando:

- [ ] Está no manifesto com ID único e versão.
- [ ] PNG RGBA com alpha verdadeiro, sem halo.
- [ ] Pivô documentado e validado em montagem.
- [ ] Camada correta conforme `layer_order.json`.
- [ ] Compatível com o rig congelado (ou rig próprio declarado).
- [ ] Animado e validado em GIF (para clipes) com rubrica ≥ 24/30.
- [ ] Metadados correspondem exatamente aos arquivos.
- [ ] Passa no `tools/validate_standards.py` sem erros.
- [ ] Preview composto existe e foi inspecionado.

O projeto inteiro só é declarado "completo" quando os 18 critérios do master-prompt §28 estiverem demonstrados com arquivos e previews — não antes.

---

## 10. Riscos e mitigação

| Risco | Prob. | Impacto | Mitigação |
|---|---|---|---|
| Peças geradas por IA não encaixarem (21 recortes inconsistentes) | Alta | Fatal | **D1/D2**: pipeline vetorial determinístico; IA só para concept. |
| Qualidade artística do render vetorial ficar abaixo do "padrão comercial" | Média | Alto | Iteração no primeiro modelo antes do freeze; shader de cel-shading em 4× supersampling; revisão em 3 tamanhos (100%, 50%, thumbnail). |
| Fluidez "escorregadia" (tudo interpolação suave, sem peso) | Alta | Alto | **D4**: keys em 24 fps com holds e spacing; curva de timing por clipe; hitstop; revisão em GIF a 25 fps. |
| Costura nas juntas | Alta | Alto | Overlap de 2–3 px, pivôs compartilhados, teste automatizado de gap por frame. |
| Loop com "pulo" | Média | Médio | Métrica de emenda (frame N+1 vs 1), revisão visual em loop triplo. |
| Escopo infinito (Dragon Ball tem centenas de personagens) | Alta | Alto | Priorização em tiers (T0–T3) no catálogo; gates; metas numéricas por fase. |
| Direitos autorais | Certa | Legal | `LICENSE_NOTES.md`, uso inspiracional, sem assets oficiais, sem declaração de licença oficial. |
| Perda de contexto entre sessões | Média | Alto | `continuity_state.json` + ledger + relatórios + reler README/Bible a cada retomada. |
| Ferramentas ausentes (sem ffmpeg, sem cairo, sem Inkscape) | Certa | Médio | Pipeline 100% Python/Pillow + ImageMagick; GIF/APNG nativos; MP4 opcional documentado. |

---

## 11. Próximos passos imediatos (Fase 2)

1. Implementar `tools/rig/` — modelo de esqueleto, transforms, IK, spring secundário, easing.
2. Implementar `tools/render/` — rasterizador de peças com contorno, cel-shading e supersampling.
3. Modelar o corpo heroico masculino A (peças + pivôs) e o rig `rig_humanoid_male_a`.
4. Modelar Goku base: gi, cabelo, luvas, botas, faixa.
5. Autorar os 9 clipes mínimos e renderizar os 18 previews.
6. Rodar a rubrica, corrigir, repetir até o gate G3.
7. Congelar a Matriz v1.0.0 (G4) e só então escalar.

---

## 12. Índice de decisões (ADRs)

| ADR | Tema | Arquivo |
|---|---|---|
| ADR-0001 | Pipeline vector-first e uso restrito de IA generativa | `docs/00_PROJECT_CHARTER.md` §6 |
| ADR-0002 | Escala, canvas e sistema de coordenadas | `docs/02_TECHNICAL_SPECIFICATION.md` §2 |
| ADR-0003 | Autoria a 24 fps / render a 60 fps | `docs/04_ANIMATION_STANDARD.md` §3 |
| ADR-0004 | Entrega dual skeletal + baked | `docs/11_INTEGRATION_GUIDE.md` §2 |
| ADR-0005 | Matriz congelável e controle de mudança | `docs/05_FLUIDITY_AND_GIF_VALIDATION.md` §7 |
| ADR-0006 | Orçamento de gerações e definição de sessão | `docs/13_PIPELINE_AND_TOOLING.md` §6 |
