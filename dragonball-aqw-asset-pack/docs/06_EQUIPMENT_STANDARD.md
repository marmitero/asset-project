# 06 — EQUIPMENT STANDARD
**Projeto AURA · v1.0.0**
Norma de armaduras, armas, helms, capas, luvas, botas e acessórios. O objetivo é que **qualquer peça encaixe em qualquer corpo compatível** sem redesenho.

---

## 1. Regra fundamental

No AQW, equipamento **substitui** partes do corpo; não veste por cima. O AURA adota o mesmo modelo, com cobertura declarada.

- Cada peça declara `covers[]` — quais slots do corpo ela substitui.
- Uma peça pode cobrir vários slots (peitoral cobre `torso` + `shoulders`).
- O que não é coberto continua visível (skin ou roupa base).
- Nenhuma peça cobre `face` — apenas helms `morph` substituem `head`.

### 1.1 Slots de equipamento

| Slot de equip | Cobre | Camada |
|---|---|---|
| `armor_torso` | `torso` | 90 |
| `armor_pelvis` | `pelvis` | 80 |
| `armor_arms` | `upper_arm_*`, `forearm_*` | 60/61/130/131 |
| `armor_legs` | `thigh_*`, `shin_*` | 70/71/100/101 |
| `boots` | `foot_*` | 72/102 |
| `gloves` | `hand_*` | 62/132 |
| `shoulders` | `shoulders` | 120 |
| `belt` | `pelvis` (acima) | 82 |
| `helm` | `helm` ou `head`+`face`+`hair_front` | 116 |
| `hair` | `hair_front`, `hair_back` | 40/115 |
| `cape` | `cape` | 30 |
| `wings` | `wings` | 31 |
| `weapon_f` | `weapon_f` | 140 |
| `weapon_b` | `weapon_b` (slot 50) | 50 |
| `accessory` | livre, declarado | 116–140 |
| `aura` | `aura_back` / `aura_front` | 20/160 |

---

## 2. Estrutura de um conjunto de armadura

Cada set exporta **peças separadas**, no mesmo canvas do corpo:

```
armor/<set_id>/
  torso.png · pelvis.png · shoulders_l.png · shoulders_r.png
  upper_arm_f.png · upper_arm_b.png · forearm_f.png · forearm_b.png
  hand_f.png · hand_b.png
  thigh_f.png · thigh_b.png · shin_f.png · shin_b.png
  foot_f.png · foot_b.png
  belt.png (opcional)
  masks/{cloth_primary,cloth_secondary,metal,trim}.png
  <set_id>.json
  icon_128.png
```

- **16 peças** para um set completo (8 pares simétricos + torso/pelve).
- Slots simétricos usam a mesma arte espelhada, salvo assimetria declarada.
- Cada peça tem pivô na junta correspondente (doc 03 §4).
- Overlap obrigatório: 2–3 px nas juntas, 4 px no quadril.

### 2.1 Cobertura parcial
Sets incompletos são válidos e declarados:

```json
"covers": ["torso", "shoulders"],
"body_visible": ["pelvis", "arms", "legs", "feet"]
```

---

## 3. Sets iniciais (T0 — primeira onda)

| Set ID | Tema | Cobertura | Facção | Observação |
|---|---|---|---|---|
| `set_goku_gi` | Gi laranja | torso, pelvis, arms, legs, feet, hands | Herói | base do primeiro modelo |
| `set_goku_gi_weighted` | Gi com pesos (Kanji 界王) | idem + acessório de costas | Treino | variação por máscara + prop |
| `set_vegeta_saiyan` | Armadura saiyajin clássica | torso, shoulders, legs, feet, hands | Saiyajin | branco + azul + ombreira |
| `set_vegeta_cell_saga` | Armadura com ombreiras amarelas | idem | Saiyajin | segunda leitura |
| `set_piccolo` | Roupa namekuseijin | torso, pelvis, arms, legs, feet + capa | Namek | capa + turbante |
| `set_turtle_school` | Gi de treino (Kame) | torso, pelvis, arms, legs, feet | Kame | Kuririn/Yamcha/Goku criança |
| `set_saiyaman` | Grande Saiyaman | completo + capa + helm | Herói | teste de excesso |
| `set_frieza_soldier` | Uniforme de Freeza | torso, shoulders, legs, feet, hands | Freeza | inimigo comum |
| `set_red_ribbon` | Uniforme Red Ribbon | torso, legs, boots | RR | inimigo comum |
| `set_galactic_patrol` | Patrulha Galáctica | torso, shoulders, legs, boots | GP | Jaco/Vegeta DBS |
| `set_fusion_vest` | Colete de fusão | torso, shoulders | Fusão | Gotenks/Gogeta |
| `set_king_kai_training` | Roupa de treino do Rei Kaiô | torso, legs, feet | Treino | Goku/Vegeta |

Cada set recebe **3 variantes de cor** via máscaras (CC1/CC2/trim) quando fizer sentido; nunca recolorir metais canônicos.

---

## 4. Armas

### 4.1 Categorias e dimensões

| Categoria | Comprimento (× altura) | Grip | Pivô | Exemplos |
|---|---|---|---|---|
| **Espada** | 0,9–1,3× | 1 mão ou 2 | base do cabo | Espada de Trunks, Z-Sword |
| **Espada gigante** | 1,4–1,8× | 2 mãos | base do cabo | Broly, Tapion |
| **Adaga** | 0,3–0,45× | 1 mão (par) | cabo | inimigos ágeis |
| **Cajado** | 1,4–1,7× | 2 mãos | centro do cabo | cajados, lanças |
| **Lança** | 1,6–2,0× | 2 mãos | 35% do cabo | inimigos |
| **Machado** | 0,9–1,2× | 1–2 mãos | base do cabo | guerreiros |
| **Marreta** | 1,0–1,4× | 2 mãos | base do cabo | elites |
| **Manoplas / gauntlet** | 0,3× | mão | centro | lutadores |
| **Arma de ki** | 0,8–1,2× | 1 mão | empunhadura | original (marcar como não-canônico) |
| **Bastão mágico** | 1,2–1,4× | 1 mão | centro | Bulma/Chi-Chi |
| **Leque / abanador** | 0,5× | 1 mão | base | NPC |

### 4.2 Grip e alinhamento
- O eixo do cabo é **vertical** no arquivo (ou horizontal declarado), com `grip` a 25–35% da base.
- `grip` no metadata; `weapon_f` socket alinha ao centro da mão fechada.
- Duas poses de mão: `fist` (padrão) e `open` (cast). A arma declara `grip_pose`.
- Empunhadura dupla (`two_handed: true`) exige animação específica e `weapon_b` opcional.

### 4.3 Armas traseiras e dual wield
- Armas de duas mãos em repouso usam `weapon_back` (camada 50) e migram para `weapon_f` no ataque (`attachment_swap` no clipe).
- Dual wield: arma principal em `weapon_f`, secundária em `weapon_b`; ataques alternam.
- Armas gigantes têm **trail socket** na ponta (`weapon_tip`) para VFX.

### 4.4 Regras visuais
- Comprimento máximo sem ser boss: 1,8× a altura.
- Contorno 3,0 px; lâmina com **2 brilhos duros** e fio branco de 1 px.
- Cabo sempre legível: cor distinta da lâmina.
- Nenhuma arma canônica é inventada; armas originais são marcadas `canon: false`.

---

## 5. Helms e cabelos

| Tipo | Comportamento | Slots | Exemplo |
|---|---|---|---|
| `hat` | sobrepõe cabelo | `helm` | chapéu, coroa, turbante |
| `morph` | substitui cabeça + face + cabelo | `head`, `face`, `hair_front` | capacete fechado, máscara |
| `hair` | substitui cabelo | `hair_front`, `hair_back` | SSJ, penteados |
| `face_accessory` | sobrepõe face | `face` (extra) | scouter, óculos |

- Helm `hat` não pode cobrir os olhos.
- Helm `morph` declara `head_height_px` e `eye_line_y` para reposicionar o retrato.
- Cabelos têm 2 peças (frente/trás) + 2 ossos de secundária.
- Chapéus com aba larga recebem 1 osso de sway opcional.

---

## 6. Capas, asas e caudas

| Item | Ossos | Camada | Regras |
|---|---|---|---|
| Capa curta | 2 | 30 | até 50% da altura; sway 20° |
| Capa longa | 3 | 30 | até 85% da altura; sway 32°; nunca cobre os pés em idle |
| Asas | 3 por asa | 31 | abertura 1,2× a largura do corpo; flap 24 f |
| Cauda saiyajin | 3 | 50 | presa ao pelvis; não colide com a perna |
| Faixa/obi | 2 | 82 | sway 14° |

- Capa e asas **nunca** são desenhadas com blur; movimento por ossos, não por smear.
- Teste obrigatório: caminhada, corrida, ataque e morte sem atravessar o corpo.

---

## 7. Máscaras e color customization

- Todo set exporta `cloth_primary`, `cloth_secondary`, `metal`, `trim` (quando aplicável).
- 3 variantes pré-aprovadas por set + possibilidade de recolor em runtime.
- A rampa de 3 tons é recalculada a partir da nova cor-base; nunca se aplica cor chapada sobre a sombra existente.
- Metais canônicos e cores de facção não são recolhíveis por padrão (`lock: true`).

---

## 8. Compatibilidade e clipping

### 8.1 Matriz de compatibilidade
Todo set declara:

```json
"compatible_rigs": ["humanoid_male_a", "humanoid_muscular_b", "humanoid_female_a"],
"incompatible": ["majin_a"],
"clipping_risk": ["cape_longo + set_piccolo"],
"tested_poses": ["idle", "run", "attack_heavy", "death"]
```

### 8.2 Testes obrigatórios
1. Montagem em 3 rigs compatíveis.
2. Idle, run, attack_heavy e death sem clipping.
3. Troca em runtime com 3 sets diferentes, sem popping.
4. Sentar e levantar (peças rígidas não podem furar).
5. Escala 50% e 200%.

### 8.3 Falhas que reprovam
- Ombreira flutuando quando o braço sobe.
- Cinto cortando o tronco em flexão.
- Capa atravessando a perna na corrida.
- Bota abrindo no tornozelo.
- Luva com pivô diferente da mão.

---

## 9. Ícones de equipamento

- Derivados do asset, não redesenhados: renderizar peça isolada em 512², enquadrar, reduzir.
- Fundo transparente, forma ocupando 72% do quadro.
- Contorno 1 px escuro para leitura em slot de 64 px.
- 3 tamanhos: 64, 128, 256.
- Estados: normal, selecionado, bloqueado, cooldown.

---

## 10. IDs e nomes

```
DB_EQUIP_ARMOR_SET_GOKU_GI_TORSO
DB_EQUIP_WEAPON_SWORD_TRUNKS
DB_EQUIP_HELM_HAT_TURBAN_PICCOLO
DB_EQUIP_CAPE_LONG_PICCOLO
DB_EQUIP_ACCESSORY_SCOUTER_BLUE
```

- `set_id` agrupa peças; peças têm ID próprio.
- Variantes: `_CC1_BLUE`, `_GOLD`, `_BROKEN`.
- Versão por peça; o set agrega a maior versão.

---

## 11. Checklist de equipamento

- [ ] Pivôs coincidem com as juntas do rig.
- [ ] Overlap de 2–3 px nas juntas.
- [ ] Ordem de camada correta.
- [ ] Máscaras exportadas e testadas.
- [ ] Compatível com ao menos 2 rigs.
- [ ] Sem clipping em 4 poses-chave.
- [ ] Contorno e paleta dentro da Visual Bible.
- [ ] Ícone derivado e legível a 64 px.
- [ ] Metadados completos e válidos.
