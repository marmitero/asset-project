# 15 — CATÁLOGO DE PERSONAGENS
**Projeto AURA · v1.0.0**
Roster canônico organizado por continuidade, com prioridade, rig, figurino e transformações. É a fonte para o backlog de personagens.

> "Canônico", neste projeto, significa **fidelidade ao design oficial** da franquia, incluindo GT e filmes como continuidades separadas. Não afirma que todas pertencem à mesma cronologia.

---

## 1. Tiers de prioridade

| Tier | Critério | Uso |
|---|---|---|
| **T0** | primeiro vertical slice + heróis icônicos | Fases 2–5 |
| **T1** | elenco jogável principal + vilões icônicos | Fases 5–8 |
| **T2** | variedade de saga, NPCs importantes, bosses | Fases 6–8 |
| **T3** | completude, filmes, seasonais, emotes | Fase 12+ |

---

## 2. T0 — primeira onda (12)

| Personagem | ID base | Rig | Figurino | Formas | Notas |
|---|---|---|---|---|---|
| **Goku** | `DB_CHAR_HERO_GOKU` | `humanoid_male_a` | gi laranja + azul, faixa, botas | base, SSJ1–3, SSG, SSB, UI | personagem-molde |
| **Vegeta** | `DB_CHAR_HERO_VEGETA` | `humanoid_male_a` | armadura saiyajin branca/azul | base, SSJ1–2, SSG, SSB, UE | ombreiras |
| **Gohan** | `DB_CHAR_HERO_GOHAN` | `humanoid_male_a` | gi roxo + vermelho (adulto) | base, SSJ1–2, Ultimate, Beast | 3 fases de idade |
| **Piccolo** | `DB_CHAR_HERO_PICCOLO` | `namekian_a` | gi roxo, turbante, capa | base, Orange | capa + antenas |
| **Trunks** | `DB_CHAR_HERO_TRUNKS` | `humanoid_male_a` | jaqueta + espada | base, SSJ1–2 | arma canônica |
| **Kuririn** | `DB_CHAR_HERO_KURIRIN` | `humanoid_male_a` | gi laranja Turtle | base | careca, baixo |
| **Bulma** | `DB_CHAR_NPC_BULMA` | `humanoid_female_a` | roupa DB/CC | — | NPC + criação |
| **Freeza** | `DB_CHAR_VILLAIN_FRIEZA` | `frieza_race_a` | forma final | final, Golden, Black | 4 formas |
| **Cell** | `DB_CHAR_VILLAIN_CELL` | `humanoid_muscular_b` | perfect | imperfect, semi, perfect | rig próprio por forma |
| **Majin Buu** | `DB_CHAR_VILLAIN_MAJIN_BUU` | `majin_a` | calça branca, capa | fat, super, kid | 3 rigs |
| **Beerus** | `DB_CHAR_VILLAIN_BEERUS` | `humanoid_male_a` | egípcio/divino | base | boss |
| **Broly** | `DB_CHAR_VILLAIN_BROLY` | `humanoid_muscular_b` | armadura + saia | base, LSSJ, DBS | escala 1,15× |

---

## 3. T1 — elenco principal (24)

| Personagem | ID base | Continuidade | Rig | Formas |
|---|---|---|---|---|
| Goku criança | `DB_CHAR_HERO_GOKU_CHILD` | DB | `humanoid_child_a` | base, Oozaru |
| Gohan criança | `DB_CHAR_HERO_GOHAN_CHILD` | DBZ | `humanoid_child_a` | base, SSJ1–2 |
| Gohan adolescente | `DB_CHAR_HERO_GOHAN_TEEN` | DBZ | `humanoid_male_a` | base, SSJ1–2 |
| Goten | `DB_CHAR_HERO_GOTEN` | DBZ | `humanoid_child_a` | base, SSJ |
| Trunks criança | `DB_CHAR_HERO_TRUNKS_KID` | DBZ | `humanoid_child_a` | base, SSJ |
| Bardock | `DB_CHAR_HERO_BARDOCK` | DBZ | `humanoid_male_a` | base, SSJ |
| Raditz | `DB_CHAR_VILLAIN_RADITZ` | DBZ | `humanoid_male_a` | base |
| Nappa | `DB_CHAR_VILLAIN_NAPPA` | DBZ | `humanoid_muscular_b` | base |
| Zarbon | `DB_CHAR_VILLAIN_ZARBON` | DBZ | `humanoid_male_a` | base, monstro |
| Dodoria | `DB_CHAR_VILLAIN_DODORIA` | DBZ | `humanoid_muscular_b` | base |
| Capitão Ginyu | `DB_CHAR_VILLAIN_GINYU` | DBZ | `humanoid_muscular_b` | base |
| Recoome / Burter / Jeice / Guldo | `DB_CHAR_VILLAIN_RECOOME` etc. | DBZ | `humanoid_muscular_b` / `creature_small_a` | base |
| Androide 17 / 18 | `DB_CHAR_VILLAIN_ANDROID_17` / `_18` | DBZ | `android_a` / `humanoid_female_a` | base |
| Androide 16 / 19 / 20 | `..._ANDROID_16` etc. | DBZ | `android_a` | base |
| Dabura | `DB_CHAR_VILLAIN_DABURA` | DBZ | `humanoid_male_a` | base |
| Videl | `DB_CHAR_HERO_VIDEL` | DBZ | `humanoid_female_a` | base, Great Saiyaman 2 |
| Mr. Satan | `DB_CHAR_NPC_MR_SATAN` | DBZ | `humanoid_muscular_b` | base |
| Dende | `DB_CHAR_NPC_DENDE` | DBZ | `humanoid_child_a` | base |
| Rei Kaiô | `DB_CHAR_NPC_KING_KAI` | DBZ | `humanoid_male_a` (adaptado) | base |
| Chi-Chi | `DB_CHAR_NPC_CHICHI` | DB | `humanoid_female_a` | base, adulta |
| Yamcha | `DB_CHAR_HERO_YAMCHA` | DB | `humanoid_male_a` | base |
| Tenshinhan | `DB_CHAR_HERO_TENSHINHAN` | DB | `humanoid_muscular_b` | base |
| Chaos | `DB_CHAR_NPC_CHIAOTZU` | DB | `humanoid_child_a` | base |
| Mestre Kame | `DB_CHAR_NPC_MASTER_ROSHI` | DB | `humanoid_male_a` (adaptado) | base, buff |

---

## 4. T2 / T3 — catálogo por continuidade

### 4.1 Dragon Ball clássico
Pilaf, Shu, Mai, Oolong, Puar, Lunch, Android 8, Tao Pai Pai, Rei Cutelo (Ox-King), Karin, Kami-Sama, Mr. Popo, Piccolo Daimaoh, Chi-Chi criança, Yamcha, Nam, General Blue, Mercenary Tao.

### 4.2 Dragon Ball Z
Gotenks, Vegito, Gogeta (Z), Supreme Kai, Kibito, Babidi, Yajirobe, Korin, Porunga (NPC), Rei Cold, Cooler, Metal Cooler, Turles, Lord Slug, Garlic Jr., Dr. Gero, Cell Jr., Saibaman, Bardock, King Vegeta, Tarble, Launch, Marron, Ox-King, Grand Kai.

### 4.3 Dragon Ball Super
Whis, Champa, Vados, Hit, Cabba, Caulifla, Kale, Kefla, Jiren, Toppo, Dyspo, Zamasu, Goku Black, Fused Zamasu, Zen'oh, Grand Priest, DBS Broly, Gogeta (DBS), Moro, Granolah, Merus, Android 21 (marcar `canon: false` se não canônico).

### 4.4 Dragon Ball GT
Goku GT, Vegeta GT, Pan, Trunks GT, Giru, Baby, Super Baby Vegeta, Super Android 17, Omega Shenron, Nuova Shenron, Eis Shenron, Haze Shenron, Rage Shenron, Oceanus Shenron, Naturon Shenron, Syn Shenron, SSJ4 Goku/Vegeta/Gogeta.

### 4.5 Filmes
Cooler, Metal Cooler, Turles, Lord Slug, Janemba, Tapion, Hirudegarn, Bojack, Zangya, Broly (Z), Paragus, Garlic Jr., Androides 13/14/15, Dr. Wheelo, Slug's henchmen.

---

## 5. Matriz de transformações

| Forma | Cabelo | Olhos | Sobrancelha | Aura | Rig | VFX de ativação |
|---|---|---|---|---|---|---|
| `base` | canônico | canônico | canônica | nenhuma | base | — |
| `oozaru` | — | vermelhos | — | nenhuma | `quadruped_a` 3,2× | explosão + lua |
| `ssj` | dourado, +18% | turquesa `#2FBF9E` | dourada | `#FFD84D` | base | 24 f + choque |
| `ssj2` | dourado, +22% | turquesa | dourada | `#FFE066` | base | 32 f + raio |
| `ssj3` | até a cintura, sem sobrancelha | turquesa | — | `#FFE066` | base (cabelo extra) | 40 f + choque |
| `ssg` | vermelho `#D94F6E` | vermelho | vermelha | `#E8405F` | base (magro) | 30 f |
| `ssb` | azul `#4FC3F7` | azul | azul | `#35B8FF` | base | 32 f + explosão |
| `ssbe` | azul escuro | azul | azul | `#1E78FF` | base | 36 f |
| `ui_sign` | preto/prata | prata | preta | `#8FB8FF` | base | 30 f |
| `ui` | prata `#D8DEE8` | prata | prata | `#C9E4FF` | base | 36 f |
| `blue_evolution` | azul intenso | azul | azul | `#1E78FF` | base | 36 f |
| `ultra_ego` | roxo | roxo | roxa | `#8E5BD9` | muscular | 36 f |
| `beast` | prata, +30% | vermelho | prata | `#7FD4FF` | base | 40 f |
| `golden` (Freeza) | — | vermelho | — | `#FFB92E` | frieza | 32 f |
| `black` (Freeza) | — | vermelho | — | `#3A1B4A` | frieza | 36 f |
| `orange` (Piccolo) | — | laranja | — | `#FF9A1E` | namekian | 30 f |
| `majin` | — | — | — | `#B44BE0` | base | 24 f (M stamp) |
| `potara` / `fusion` | combinado | combinado | combinado | variável | base/adaptado | 48 f |

Regras:
- Formas que **não** mudam anatomia reutilizam o rig: troca de cabelo, olhos, sobrancelha, aura e paleta.
- Formas que mudam anatomia (Oozaru, Kid Buu, formas de Freeza/Cell) têm rig próprio e ID próprio.
- A transformação é um **estado** do personagem, não um asset novo completo: `DB_CHAR_HERO_GOKU_SSJ` referencia as mesmas peças de corpo + cabelo SSJ.

---

## 6. NPCs (mínimo 10 jogáveis de conversa)

Cysero-equivalente (ferreiro), comerciante de cápsulas, mestre de classe, banqueiro, treinador de artes marciais, curandeiro, mensageiro, guarda, aldeão, ferreiro namekuseijin, sacerdote, mestre de torneio.

Cada NPC: 1 rig, 1 figurino, 3 faces, idle + talk, retrato 256², APOP (diálogo) com 3 opções.

---

## 7. Inimigos

### 7.1 Comuns (20)
Saibaman (verde/azul), soldado de Freeza (2 variantes), soldado Red Ribbon (2), Cell Jr., capanga de Babidi, robô RR, lobo selvagem, dinossauro pequeno, criatura de Namek, planta carnívora, bandido, morcego gigante, golem de pedra, esqueleto, slime, pirata espacial, drone, morto-vivo, guarda de templo.

### 7.2 Elites (10)
Raditz, Nappa, Zarbon, Dodoria, Recoome, Burter, Jeice, Androide 19, Androide 20, Dabura.

### 7.3 Bosses (12)
Piccolo Daimaoh, Vegeta (Saga Saiyajin), Freeza, Cell, Majin Buu, Beerus, Goku Black, Zamasu fundido, Jiren, Broly, Janemba, Omega Shenron.

Cada boss: silhueta distinta, escala própria (1,2–3,0×), idle, 2 ataques básicos, 2 especiais, reação, morte, retrato 512², ícone de alvo, VFX assinatura, sockets.

---

## 8. Pets

Puar, Oolong, Giru, Icarus/Haiya, Bubbles, Gregory, dinossauro bebê, Namek frog, Moglin-equivalente original, robô auxiliar, nuvem voadora (item), esfera do dragão viva (original), mini-dragão, gato, falcão, javali, sapo, espírito de ki, slime, morcego, tartaruga, lobo, pequeno saiyajin (não-canônico), mini Cell Jr.

Escala: 25–33% da altura do player. Animações: idle, follow, move, attack, hit, celebrate, sleep.

---

## 9. IDs — exemplos canônicos

```
DB_CHAR_HERO_GOKU_BASE_IDLE
DB_CHAR_HERO_GOKU_SSJ_ATTACK01
DB_CHAR_HERO_VEGETA_SSB_CAST
DB_CHAR_VILLAIN_FRIEZA_FINAL_HURT_CRIT
DB_CHAR_VILLAIN_CELL_PERFECT_IDLE
DB_CHAR_VILLAIN_MAJIN_BUU_KID_IDLE
DB_ENEMY_COMMON_SAIBAMAN_GREEN_ATTACK
DB_ENEMY_BOSS_BEERUS_IDLE
DB_PET_COMPANION_PUAR_FOLLOW
DB_RIG_HUMANOID_MALE_A
```

---

## 10. Regras de cobertura

- Todo personagem jogável tem: 18–26 peças, 8 máscaras, 10 faces, 9 clipes mínimos, retrato e ícone.
- Toda transformação tem: hair/eyes/aura + `transform_in/out` + ícone.
- Toda continuidade tem pelo menos 1 herói, 1 vilão e 1 mapa.
- Nenhum personagem é "pintura de cor" de outro: silhueta, cabelo e figurino mudam.
- Gênero e etnia de corpo são representados nos rigs (`male_a`, `female_a`, `muscular_b`, `child_a`), não por estereótipo.
- Personagens de filmes/GT declaram `continuity` e não são misturados com DBS.
