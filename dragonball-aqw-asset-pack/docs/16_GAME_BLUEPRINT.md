# 16 — GAME BLUEPRINT
**Projeto AURA · v1.0.0**
Blueprint de mecânicas para um MMORPG 2D de ação inspirado em AQW. É o documento que uma IA lê para saber **o que o pack precisa suportar** e **como usar** cada tipo de asset.

> Não é uma cópia de AQW. É um conjunto de regras de design coerentes com a linguagem do pack.

---

## 1. Pilares de design

1. **Combate casual em tempo real** — alvo travado, auto-attack + 5 skills, leitura clara.
2. **Customização como meta** — paper-doll, centenas de itens, aparência acima de stats.
3. **Mundo em salas** — cada tela é uma sala com spawns, NPCs, portais.
4. **Progressão por classe** — trocar de classe é trocar de "personagem de combate", não de corpo.
5. **Conteúdo semanal** — quests, loja e bosses rotativos.
6. **Fantasia Dragon Ball** — ki, transformações, técnicas icônicas, esferas do dragão.

---

## 2. Loop principal

```
Explorar sala → aceitar quest → derrotar inimigos → coletar loot/XP
      → subir nível/rank → desbloquear skill/transformação
      → comprar/equipar visual → nova sala/boss → repetir
```

Sessão curta (5–15 min) precisa render: 1 quest, 3 combates, 1 drop, 1 decisão de visual.

---

## 3. Controles

| Ação | Mouse/teclado | Gamepad |
|---|---|---|
| Mover | clique no chão / WASD | analógico |
| Selecionar alvo | clique no inimigo / Tab | R1 |
| Auto-attack | clique duplo / tecla 1 | X |
| Skills | 2–6 / clique na barra | botões |
| Rest | botão coração | Select |
| Inventário | I | Start |
| Mapa | M | — |
| Interagir | clique no NPC/objeto | Y |

- Movimento **clique-para-andar** por padrão (herança AQW), com WASD opcional.
- Sem pulo no combate corpo a corpo; pulo apenas visual/emote (evita quebrar o 2.5D).
- Facing automático para o alvo ao atacar.

---

## 4. Câmera e apresentação

- Câmera 2.5D lateral fixa em Y, rola em X.
- Viewport 1280×720; personagem 220 px.
- Depth sort por `foot_y`; escala 1,00 → 0,86 do fundo para a frente.
- Oclusores do cenário escondem atores atrás.
- Screen shake e hitstop conforme doc 04 §7.

---

## 5. Combate

### 5.1 Estrutura
- **Alvo travado**: 1 alvo por vez; barra de HP no topo-centro.
- **Auto-attack**: 2,0 s de cooldown; dano por arma; sem mana.
- **5 skills**: cooldowns de 2–25 s; custo de mana; ranks desbloqueiam.
- **Transformação**: slot extra (7) desbloqueado no nível 20; dura 20 s, cooldown 90 s.
- **Hitstop** e flash em todo acerto; crítico com shake maior.

### 5.2 Fórmulas (referência)

```
dano_base   = weapon_damage × skill_multiplier
dano_final  = dano_base × (1 + atk_power/50) × mitigação
mitigação   = 100 / (100 + armor)
crítico     = dano_final × 1,75
chance_crit = 5% + dex × 0,2%  (cap 40%)
chance_miss = max(0, 5% − hit × 0,15%)
HP          = 100 + 22 × (level − 1)
Ki/MP       = 100 (fixo, como AQW) + bônus de classe
XP_next     = round(100 × level^1,55)
```

- Dano exibido com variação ±10%.
- Dano elemental aplica resistência/fraqueza (0,75× / 1,25×).
- Cura não pode exceder HP máximo; overheal é descartado.

### 5.3 Status
| Status | Efeito | Duração | VFX |
|---|---|---|---|
| Queimadura | 3% HP/s | 6 s | fogo no corpo |
| Congelamento | −30% velocidade | 4 s | gelo nos pés |
| Choque | −15% precisão | 5 s | faíscas |
| Sangramento | 2% HP/s | 8 s | gotas |
| Buff de ataque | +20% dano | 10 s | aura vermelha |
| Escudo | absorve X | 8 s | hexágono |
| Lentidão | −40% velocidade | 5 s | poeira |
| Silêncio | bloqueia skills | 3 s | símbolo na cabeça |
| Stun | não age | 1,5 s | estrelas |
| Transformação | +30% dano, +15% velocidade | 20 s | aura da forma |

- Máximo 5 status simultâneos; prioridade visual: stun > transformação > escudo > debuff.

---

## 6. Classes (8 iniciais)

Cada classe tem 5 skills + 1 passiva + transformação genérica. O **corpo** é o mesmo; muda o rig visual da classe (armadura) e as animações de skill.

### 6.1 Guerreiro (Warrior)
| Slot | Skill | CD | Mana | Efeito |
|---|---|---|---|---|
| 1 | Golpe Básico (auto) | 2,0 s | 0 | 100% arma |
| 2 | Investida | 8 s | 15 | dash 120 px + 150% dano |
| 3 | Golpe Decisivo | 12 s | 20 | 220% dano, 20% crit extra |
| 4 | Grito de Guerra | 20 s | 10 | +20% atk 10 s |
| 5 | Terremoto | 25 s | 30 | AoE 180% em 160 px |
| 6 | Guarda | 18 s | 15 | −40% dano 5 s |
| P | Pele de Ferro | — | — | +15% armor |

### 6.2 Mago do Ki (Mage)
| Slot | Skill | CD | Mana | Efeito |
|---|---|---|---|---|
| 1 | Ki Blast (auto, ranged) | 2,0 s | 0 | 80% |
| 2 | Rajada | 6 s | 18 | 160% em linha |
| 3 | Explosão | 10 s | 25 | 200% AoE 120 px |
| 4 | Barreira | 16 s | 15 | escudo 20% HP |
| 5 | Meteoro de Ki | 22 s | 35 | 280% AoE 200 px |
| 6 | Teleporte | 14 s | 20 | blink 180 px |
| P | Fluxo de Ki | — | — | +20% regen mana |

### 6.3 Ladino (Rogue)
| Slot | Skill | CD | Mana | Efeito |
|---|---|---|---|---|
| 1 | Adaga (auto, rápido) | 1,5 s | 0 | 65% |
| 2 | Faca nas Costas | 8 s | 12 | 200% se pelas costas |
| 3 | Veneno | 12 s | 15 | DoT 8 s |
| 4 | Esquiva | 10 s | 10 | invuln 0,8 s |
| 5 | Dança das Lâminas | 20 s | 25 | 5 hits de 60% |
| 6 | Fumaça | 18 s | 15 | −50% hit inimigo |
| P | Reflexos | — | — | +10% dodge |

### 6.4 Sacerdote (Healer)
| Slot | Skill | CD | Mana | Efeito |
|---|---|---|---|---|
| 1 | Golpe Sagrado (auto) | 2,0 s | 0 | 80% |
| 2 | Cura | 6 s | 20 | 25% HP |
| 3 | Cura em Grupo | 14 s | 35 | 15% HP em 4 aliados |
| 4 | Bênção | 18 s | 20 | +15% def 10 s |
| 5 | Ressurreição | 60 s | 50 | revive aliado com 30% HP |
| 6 | Luz Purificadora | 22 s | 25 | remove 1 debuff |
| P | Fé | — | — | +10% cura |

### 6.5 Guardião Namekuseijin (Tank)
6.6 **Mestre do Ki** (híbrido ranged/melee)
6.7 **Assassino Androide** (sustain/energy)
6.8 **Elite Saiyajin** (burst/transformação)

> As classes 5–8 seguem a mesma tabela de 5 skills + passiva, com identidade visual própria (armadura + cor de aura).

### 6.9 Regras de classe
- Trocar de classe fora de combate; manter nível de personagem, perder buffs.
- Cada classe tem 10 ranks; rank 1–5 desbloqueiam skills; rank 6–10 passivas e bônus.
- A transformação é **universal** (todos podem), mas a aura/cor muda por classe.
- Nenhuma classe precisa de asset novo de corpo — só de skill/armadura/aura.

---

## 7. Progressão

| Sistema | Regra |
|---|---|
| Nível | 1–60; +5 atributos por nível |
| Rank de classe | 1–10; XP de classe separado |
| Atributos | Força, Destreza, Inteligência, Vitalidade, Sorte |
| Skills | desbloqueadas por rank (1–5) |
| Transformações | nível 20 (SSJ), 35 (SSG), 45 (SSB), 55 (UI) |
| Equipamento | nível mínimo; sem "item level" inflado |
| Reputação | facções: Guerreiros Z, Patrulha Galáctica, Red Ribbon (hostil), Namek |
| Conquistas | 60 no lançamento |

---

## 8. Quests

| Tipo | Exemplo | Recompensa |
|---|---|---|
| Kill | "Derrote 8 Saibamans" | XP + ouro |
| Collect | "Colete 5 cápsulas" | XP + item |
| Talk | "Fale com Mestre Kame" | XP + desbloqueio |
| Escort | "Proteja o mensageiro" | XP + reputação |
| Boss | "Derrote Freeza" | item raro + desbloqueio |
| Daily | "Treino diário" | XP + token |
| Weekly | "Invasão do Broly" | cosmético raro |

- UI de quest: lista (máx. 10 ativas), rastreador no HUD, marcador no NPC.
- Diálogo com 2–4 opções e retrato.
- Recompensa sempre mostra ícone + quantidade.

---

## 9. Economia e itens

| Moeda | Uso |
|---|---|
| Ouro | lojas, reparo, treino |
| Tokens | eventos, cosméticos |
| Esferas do Dragão | evento semanal (7 esferas → desejo) |

- Raridade: Comum, Incomum, Raro, Épico, Lendário.
- Drop: 60% comum, 25% incomum, 10% raro, 4% épico, 1% lendário.
- Inventário 40 slots + banco 100.
- Itens: arma, armadura (6 peças), helm, capa, acessório, consumível, material, quest.
- Consumíveis: Senzu (cura 50%, 1 por combate), cápsula de treino (+10% XP 30 min).
- Nenhum item pay-to-win; premium apenas cosmético.

---

## 10. Mundo e salas

- Cada sala: 1280×720 de viewport, 1920–3200 px de largura.
- 5–12 inimigos, 1–3 NPCs, 1–2 portais.
- Respawn 20–40 s; elite 90 s; boss 5 min.
- Salas seguras (cidades) sem combate.
- Mapa-múndi com nós; portal com nome do destino.
- Oclusão e depth sort por `foot_y`.

Mapas iniciais: Monte Paozu → Kame House → Cidade do Oeste → Torneio → Namek → Arena de Cell → Planeta de Beerus → Torneio do Poder.

---

## 11. Social e multiplayer

- Party de 4; XP compartilhado.
- Guild até 50; chat de guilda.
- Canais de chat: local, party, guild, global, trade, PM.
- Boss mundial semanal (ex.: Broly) com HP global e recompensa por participação.
- PvP opcional em arena; não é escopo inicial.
- Servidor autoritativo a 20 Hz; cliente a 60 fps com predição.

---

## 12. Onboarding (primeiros 10 minutos)

1. Criação de personagem (raça, rosto, cabelo, cor, nome) com preview animado.
2. Cutscene curta com o mestre.
3. Tutorial de movimento (3 waypoints).
4. Tutorial de alvo + auto-attack (1 inimigo fraco).
5. Primeira skill desbloqueada + 2 inimigos.
6. Primeira quest + primeira recompensa visual (chapéu/cor).
7. Portal para a cidade; HUD completa.

Métricas: 90% completam o tutorial; primeira compra de cosmético em ≤ 15 min.

---

## 13. Conteúdo e cadência

| Ciclo | Entrega |
|---|---|
| Semanal | 1 quest line curta + 1 item de loja + 1 boss rotativo |
| Mensal | 1 mapa novo ou 1 classe nova |
| Sazonal | evento (Halloween/Namek/Freeza) com cosméticos |

- Todo conteúdo novo usa os mesmos 9 clipes + assets existentes.
- Nenhum conteúdo semanal exige rig novo.

---

## 14. Acessibilidade

- Escala de UI 100/125/150%.
- `reduce_motion` e `reduced_vfx`.
- Daltonismo: paletas alternativas.
- Remapeamento de teclas e suporte a gamepad.
- Legendas para cutscenes.

---

## 15. O que o pack precisa fornecer para este blueprint

| Sistema | Assets necessários |
|---|---|
| Personagens | corpo, gi, faces, cabelo, rig, 9 clipes |
| Classes | armadura de classe, ícones, VFX de skill |
| Combate | hit reactions, crit, miss, dano, morte, block, dodge |
| Transformações | cabelo/aura/olhos + ativação + ícone |
| Inimigos | 20 comuns, 10 elites, 12 bosses |
| Pets | 20+ com follow/attack |
| Mundo | 8 mapas com camadas, tiles, props, colisão |
| Quests | ícones, retratos de NPC, painel |
| Loja/economia | ícones de item/moeda, painel |
| UI | HUD, 12 telas, 100+ ícones |

---

## 16. MVP (o menor jogo utilizável)

- 1 mapa (Paozu) + 1 cidade (Kame House).
- 1 personagem jogável (Goku) + 3 inimigos + 1 boss.
- 3 skills + auto-attack + transformação SSJ.
- 5 quests, loja com 10 itens, inventário.
- HUD completa, save local, sem multiplayer.

O MVP é o alvo da Fase 13 (S56–S58) e serve de teste de integração do pack.
