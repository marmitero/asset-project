# DRAGON BALL — AQW-STYLE ASSET PACK
### codinome **AURA**

Pacote de assets 2D modulares para construir um **MMORPG de ação em tempo real** com a linguagem visual e de movimento de *AdventureQuest Worlds* e a identidade canônica de *Dragon Ball*.

> **Estado atual: Fase 1 (Documentação) concluída.**
> Existem **20 documentos**, **10 padrões legíveis por máquina** e a infraestrutura de produção.
> **Ainda não há assets de arte.** O primeiro modelo (Goku) será criado na Fase 2 e validado por GIF antes de qualquer produção em escala.

---

## O que é este pack

Não é uma coleção de ilustrações. É um **sistema de produção**:

- **Personagens paper-doll** — 29 slots de render (21 camadas canônicas + 8 extensões), peças substituíveis, pivôs exatos.
- **Rig determinístico** — 29 ossos, IK de perna, secundárias por mola.
- **Animação em dados** — timelines JSON, autoria a 24 fps, render a 60 fps.
- **Equipamentos modulares** — armaduras que substituem partes, armas com grip, capas com física.
- **VFX componentizados** — cast, carga, projétil, beam, impacto, explosão.
- **Cenários 2.5D** — camadas, parallax, tiles, colisão, oclusão.
- **UI kit de MMO** — HUD, 12 telas, ícones, 9-slice.
- **Documentação para IA** — schemas, IDs estáveis, handbook de consumo.

Tudo é **engine-agnóstico**: PNG + JSON. Godot, Unity, GameMaker e web consomem o mesmo pack.

---

## Fluxo do projeto (gates)

```
G0 Documentação ──► G1 Infra ──► G2 Primeiro modelo ──► G3 Validação por GIF
                                                              │
                              G5 Escala ◄── G4 Matriz congelada ◄┘
```

Nenhum segundo personagem é produzido antes de o primeiro passar em **18 GIFs de validação** (idle, caminhada, corrida, ataques, miss, crítico, dano recebido, morte, etc.) e a Matriz ser congelada.

Detalhes: [`PLAN.md`](../PLAN.md) e [`docs/14_ROADMAP_AND_SESSIONS.md`](docs/14_ROADMAP_AND_SESSIONS.md).

---

## Estrutura

```
dragonball-aqw-asset-pack/
├── docs/            20 documentos + índice + matrix/
├── standards/       JSON + schemas (fonte de verdade)
├── references/      paletas, pranchas de proporção, folhas de personagem
├── characters/      base_bodies, canonical_heroes, canonical_villains, npcs, transformations, rigs
├── equipment/       armor, weapons, helmets, hairstyles, capes, gloves, boots, accessories
├── enemies/         common, elite, bosses
├── pets/            companions, creatures, summons
├── skills/          icons, projectiles, auras, melee, beams, explosions, buffs, transformations
├── environments/    backgrounds, midgrounds, foregrounds, ground_tiles, props, buildings, portals, maps
├── ui/              hud, inventory, equipment, skills, quests, shop, chat, dialogs, character_creation, icons
├── exports/         individual_png, spritesheets, atlases, metadata, previews
├── production/      ledger, backlog, registry, continuity, relatórios, QA
├── examples/        cenas de integração
└── tools/           renderizador, validador, empacotador
```

---

## Comece por aqui

| Se você é… | Leia |
|---|---|
| **Agente de IA** | [`docs/17_AI_AGENT_HANDBOOK.md`](docs/17_AI_AGENT_HANDBOOK.md) + `standards/*.json` |
| **Artista** | [`docs/01_VISUAL_BIBLE.md`](docs/01_VISUAL_BIBLE.md) + [`docs/03_ANATOMY_RIG_PAPERDOLL.md`](docs/03_ANATOMY_RIG_PAPERDOLL.md) |
| **Dev/engine** | [`docs/02_TECHNICAL_SPECIFICATION.md`](docs/02_TECHNICAL_SPECIFICATION.md) + [`docs/11_INTEGRATION_GUIDE.md`](docs/11_INTEGRATION_GUIDE.md) |
| **Designer de jogo** | [`docs/16_GAME_BLUEPRINT.md`](docs/16_GAME_BLUEPRINT.md) |
| **QA** | [`docs/12_QUALITY_GATES.md`](docs/12_QUALITY_GATES.md) + [`docs/05_FLUIDITY_AND_GIF_VALIDATION.md`](docs/05_FLUIDITY_AND_GIF_VALIDATION.md) |

---

## Índice de documentos

| # | Documento | Conteúdo |
|---|---|---|
| 00 | Project Charter | visão, escopo, pilares, ADRs, governança, IP |
| 01 | Visual Bible | estilo, linha, cor, luz, proporções, faces, cabelo, do/don't |
| 02 | Technical Specification | coordenadas, escala, canvas, atlas, alpha, performance |
| 03 | Anatomy, Rig & Paper-doll | 29 ossos, juntas, pivôs, 29 slots, máscaras, rigs |
| 04 | Animation Standard | 24/60 fps, curvas, 35 clipes, walk/run, combate, secundárias |
| 05 | Fluidity & GIF Validation | F1–F6, 18 GIFs, métricas, rubrica, congelamento |
| 06 | Equipment Standard | slots, sets, armas, helms, capas, clipping |
| 07 | VFX Standard | categorias, camadas, kits canônicos, blend, timing |
| 08 | Environment Standard | 2.5D, parallax, tiles, props, colisão, map.json |
| 09 | UI Standard | HUD 1280×720, 12 telas, 9-slice, ícones, acessibilidade |
| 10 | Naming & Metadata | IDs, arquivos, schemas, versão, rename log |
| 11 | Integration Guide | skeletal/baked, state machine, IK, Godot/Unity/web |
| 12 | Quality Gates | status, G0–G5, checklists, severidade, relatórios |
| 13 | Pipeline & Tooling | auditoria real, módulos, CLI, orçamento, continuidade |
| 14 | Roadmap & Sessions | fases, sessões S00–S60, backlog, metas |
| 15 | Character Catalog | T0–T3, transformações, inimigos, pets |
| 16 | Game Blueprint | loop, combate, 8 classes, quests, economia |
| 17 | AI Agent Handbook | como consumir e expandir o pack |
| 18 | Glossary | 60+ termos PT/EN |
| 19 | Research: AQW Teardown | fontes, achados, adota/rejeita |
| — | [`docs/INDEX.md`](docs/INDEX.md) | mapa master-prompt → arquivos e ordem de leitura |

---

## Padrões legíveis por máquina

| Arquivo | Conteúdo |
|---|---|
| `standards/canvas_and_scale.json` | escala, canvas, física, budgets, GIF/APNG |
| `standards/layer_order.json` | 29 camadas z 0–160 |
| `standards/skeleton_humanoid.json` | rig completo, slots, sockets, secundárias |
| `standards/palette_master.json` | 12 personagens, 13 formas, 10 elementos, UI, 8 biomas |
| `standards/clip_matrix.json` | 35 clipes, fases, eventos, 18 GIFs, hitstop |
| `standards/easing_library.json` | 14 curvas + 6 molas, limites de métrica |
| `standards/rig.schema.json` | schema de rig |
| `standards/animation.schema.json` | schema de clipe |
| `standards/asset_manifest.schema.json` | schema de manifesto |
| `standards/naming.json` | regex de ID, categorias, estados, arquivos |

---

## Estado / roadmap

| Fase | Status |
|---|---|
| 0 — Auditoria | ✅ |
| 1 — Documentação | ✅ |
| 2 — Primeiro modelo (Goku) | ⬜ próxima |
| 3 — Validação por GIF | ⬜ |
| 4 — Matriz congelada | ⬜ |
| 5–13 — Escala | ⬜ |

Ver `production/continuity_state.json` para o ponto exato.

---

## Instalação do pipeline

```bash
pip install --break-system-packages -r requirements.txt
python -m tools.cli validate --all
```

Ambiente de referência: Python 3.11, Pillow 13, NumPy 2.4, ImageMagick 6.9. Sem ffmpeg (previews em GIF/APNG).

---

## Licença e propriedade intelectual

Este é um projeto **derivado e inspiracional**, não oficial.
Dragon Ball pertence à Shueisha/Toei/Bird Studio; AdventureQuest Worlds pertence à Artix Entertainment. Nenhum arquivo oficial foi copiado. Distribuição comercial exige autorização dos titulares.

Leia **[`LICENSE_NOTES.md`](LICENSE_NOTES.md)** antes de usar.

---

*Battle on.*

## Estado atual

- Fase 1 (documentação) concluída — 21 documentos, 10 padrões JSON.
- Fase 2: renderizador `tools/aura/` + rig de 29 ossos + primeiro modelo
  `DB_CHAR_HERO_GOKU_BASE` com 23 clipes e 18 GIFs de validação em
  `production/previews/` e `exports/`.
- Gate G2 ✅ · G3 aguardando revisão humana · matriz **não congelada** (0.0.0).
- Detalhes em `docs/20_RENDERER_AND_RIG_IMPLEMENTATION.md` e
  `production/session_reports/S02_first_model.md`.
