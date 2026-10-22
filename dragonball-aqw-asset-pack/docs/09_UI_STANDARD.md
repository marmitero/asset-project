# 09 — UI STANDARD
**Projeto AURA · v1.0.0**
Norma do kit de interface: HUD, painéis, ícones, estados, 9-slice e acessibilidade.

---

## 1. Filosofia

- Estrutura de MMO clássico (AQW), **pele** Dragon Ball: painéis escuros, moldura ouro, detalhes em laranja e azul.
- Legibilidade acima de ornamento: número e barra antes de arabesco.
- **Nenhum texto é embutido em imagem.** Todo texto vem de fonte + chave de localização.
- Tudo escala por 9-slice; nada é esticado deformando ornamento.

---

## 2. Layout de referência (1280 × 720)

```
┌──────────────────────────────────────────────────────────────┐
│ ┌─────────────┐                     ┌──────────────┐          │
│ │ RETRATO 96  │                     │ ALVO 72      │          │
│ │ nome/nível  │                     │ nome/HP      │          │
│ │ HP ▓▓▓▓▓▓   │                     └──────────────┘          │
│ │ KI ▓▓▓▓▓▓   │                                               │
│ └─────────────┘                                               │
│                                                               │
│                     ÁREA DE JOGO                              │
│                                                               │
│ ┌───────────────┐        ┌────────────────────┐  ┌─────────┐  │
│ │ CHAT 320×140  │        │ [1][2][3][4][5][6] │  │ MENU    │  │
│ └───────────────┘        └────────────────────┘  │ 48×6    │  │
│ XP ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ └─────────┘  │
└──────────────────────────────────────────────────────────────┘
```

| Componente | Posição | Tamanho | Conteúdo |
|---|---|---|---|
| Player frame | topo-esq (16,16) | 296 × 104 | retrato 88², nome, classe, nível, HP, Ki, status |
| Target frame | topo-centro | 260 × 88 | retrato, nome, nível, HP, debuffs |
| Action bar | base-centro | 6 × 56 slots + padding | skills, cooldown radial, teclas 1–6 |
| XP / CP | base, largura total | 1280 × 16 | XP roxo, classe verde |
| Chat | base-esq | 320 × 148 | log + input |
| Menu buttons | base-dir | 6 × 48² | inventário, personagem, quests, loja, opções, mapa |
| Minimap | topo-dir | 180 × 180 | opcional, com pinos |
| Buff bar | topo-centro-baixo | 200 × 32 | ícones + timers |
| Currency | topo-dir-baixo | 160 × 28 | ouro, AC, tokens |

---

## 3. Componentes e especificações

### 3.1 Barras
| Propriedade | Valor |
|---|---|
| Altura | 18 px (HP/Ki), 12 px (XP), 8 px (CP) |
| Borda | 2 px `#0E0B12` + moldura ouro 1 px |
| Preenchimento | cor cheia + brilho 1 px no topo + sombra 1 px na base |
| Fundo | `#0E0B12` a 70% |
| Texto | valor numérico 11 px, alinhado à direita, com contorno |
| Animação | “dano atrasado” (delayed damage) de 400 ms em branco |

### 3.2 Botões
| Estado | Visual |
|---|---|
| Normal | painel `#232734`, moldura ouro 2 px, texto `#F2E9D8` |
| Hover | painel `#2E3446`, brilho interno 1 px, ponteiro |
| Pressed | deslocamento 1 px, moldura `#8A5E17` |
| Selected | moldura dupla ouro + brilho externo |
| Disabled | dessaturado 70%, alpha 60%, sem hover |
| Cooldown | overlay radial escuro + número |
| Locked | cadeado + moldura cinza |

### 3.3 Slots de item/skill
- 56 × 56 (action bar), 64 × 64 (inventário), 48 × 48 (loja).
- Ícone ocupa 72% do slot.
- Rarity border: comum `#8A8F9A`, incomum `#3FBF6A`, raro `#2F80D8`, épico `#8E5BD9`, lendário `#D9A441`.
- Quantidade no canto inferior direito, 11 px.
- Cooldown: varredura radial 360→0, `rgba(0,0,0,0.65)`, número central.

### 3.4 Painéis (9-slice)
| Painel | Base | Insets (px) |
|---|---|---|
| Pequeno | 128 × 128 | 20 / 20 / 20 / 20 |
| Médio | 256 × 256 | 24 / 24 / 24 / 24 |
| Grande | 512 × 512 | 28 / 28 / 28 / 28 |
| Tooltip | 64 × 64 | 12 / 12 / 12 / 12 |

- Ornamento só nos cantos; bordas superior/inferior esticáveis.
- Nunca esticar cantos.
- Cantos: losango ou parafuso, 6–10 px.

### 3.5 Tooltip
- Largura 260, altura dinâmica.
- Título (nome + raridade), tipo, stats, descrição, custo, tempo.
- Fundo `#0E0B12` a 92%, moldura 1 px.

### 3.6 Retratos
- 256 × 256 master, exibido 88 × 88.
- Cabeça + ombros, fundo transparente + círculo de fundo da classe.
- Moldura circular ouro.
- Expressão `neutral`; variante `combat` e `dead` opcional.
- Gerados por **câmera de retrato** do rig (não redesenhados).

---

## 4. Telas (12)

| # | Tela | Conteúdo mínimo |
|---|---|---|
| 1 | HUD | player, target, action bar, XP, buffs, chat |
| 2 | Inventário | grid 8×5, abas, busca, ordenação, tooltip, equipar |
| 3 | Equipamento | boneco paper-doll com 12 slots, stats, comparação |
| 4 | Skills / Classe | 5 skills + passivas, rank, descrição, árvore simples |
| 5 | Quests | lista, detalhe, recompensas, rastreamento |
| 6 | Loja | categorias, grid, carrinho, moedas |
| 7 | Crafting | receitas, materiais, resultado |
| 8 | Chat | canais, emotes, histórico |
| 9 | Diálogo de NPC | retrato, nome, texto, opções |
| 10 | Criação de personagem | raça, rosto, cabelo, cor, nome, preview |
| 11 | Seleção de personagem | 4 slots, nível, classe, último login |
| 12 | Configurações | áudio, vídeo, controles, acessibilidade |

Extras: ranking, grupo, guilda, mapa-múndi, evento/boss mundial, recompensa, loja premium.

---

## 5. Ícones

| Propriedade | Valor |
|---|---|
| Grid de desenho | 512 × 512 |
| Export | 64 / 128 / 256 |
| Área segura | margem de 12% |
| Contorno | 1 px `#0E0B12` |
| Brilho | 1 losango duro no topo |
| Fundo | transparente |
| Cores | ≤ 6 |
| Legibilidade | reconhecível a 64 px |

Categorias: skills, transformações, armas, armaduras, consumíveis, materiais, quests, moedas, recursos, cápsulas, esferas do dragão, sensu, scouter, radar.

Estados: normal, selecionado, bloqueado, cooldown, desabilitado (gerados por filtro + overlay, não redesenhados).

---

## 6. Tipografia e localização

- **Display:** fonte fantasia serifada (ex.: Cinzel/Cormorant) para títulos — licenciamento documentado.
- **UI:** sans legível (ex.: Inter/Noto Sans) para números e corpo.
- **Placeholder no ambiente:** DejaVu Sans (documentado em `LICENSE_NOTES.md`).
- Tamanhos: 11 (micro), 13 (corpo), 16 (título de painel), 22 (título de tela), 34 (nome de boss).
- Todo texto é chave: `ui.hud.hp`, `quest.paozu.intro`, `item.gi_goku.name`.
- Nenhum texto em imagem; exceções decorativas são declaradas `decorative_text: true`.

---

## 7. Animação de UI

| Elemento | Animação | Duração |
|---|---|---|
| Barra de HP | transição + delayed damage | 200 ms / 400 ms |
| Slot de skill | flash ao usar | 120 ms |
| Tooltip | fade + 4 px slide | 120 ms |
| Painel | scale 0,96→1 + fade | 150 ms |
| Número de dano | pop 1,4× → 1,0 + subida | 700–900 ms |
| Cooldown | varredura radial | duração da skill |
| Level up | burst dourado + banner | 1200 ms |

- Animações de UI são opcionais (respeitar `reduce_motion`).

---

## 8. Acessibilidade

- Escala de UI: 100 / 125 / 150% sem perda de 9-slice.
- Modo daltônico: paleta alternativa para HP/Ki/XP.
- `reduce_motion`: desativa shake e reduz flashes.
- `reduced_vfx`: reduz tamanho/opacidade de efeitos.
- Contraste mínimo de texto 4,5:1.
- Todos os botões com estado de foco (teclado/gamepad).

---

## 9. Entrega técnica

```
ui/
  hud/{player_frame,target_frame,action_bar,xp_bar,chat,menu}.png + .9.json
  inventory/... · equipment/... · skills/... · quests/... · shop/...
  dialogs/... · character_creation/...
  icons/{skills,items,status}/...
  atlas/ui_hud_2048.png + .json
  ui_theme.json          (cores, fontes, insets, tamanhos)
```

- Cada elemento 9-slice tem `<nome>.9.json`: `{size, insets:[t,r,b,l], stretch:"xy"}`.
- Atlas de UI em 2048² com padding 4 px.
- `ui_theme.json` é a fonte de verdade para código (CSS/engine theme).

---

## 10. Checklist de UI

- [ ] Texto em chave, não em imagem.
- [ ] 9-slice com insets corretos.
- [ ] Todos os 8 estados por componente interativo.
- [ ] Contraste e legibilidade a 100% e 150%.
- [ ] Ícone legível a 64 px.
- [ ] Escala sem deformar ornamento.
- [ ] `reduce_motion` e `reduced_vfx` suportados.
- [ ] Atlas e tema exportados.
