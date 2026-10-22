# 19 — PESQUISA: TEARDOWN DE ADVENTUREQUEST WORLDS
**Projeto AURA · v1.0.0 · pesquisa realizada em 2026-10-22**
Registro das fontes consultadas, do que foi aprendido e do que o projeto adota ou rejeita. Pesquisa de **referência**, não de cópia.

---

## 1. Fontes consultadas

| # | Fonte | Tipo | O que fornece |
|---|---|---|---|
| 1 | [Monster Making 101 — aq2d.com](https://aq2d.com/posts/monster_making_101/) | oficial (Artix) | pipeline de monstros: peças, power-of-2, pivôs, animações obrigatórias, bones |
| 2 | [AQWorlds Infinity Q&A — aq2d.com](https://aq2d.com/posts/aqworlds_infinity_questions_and_answers/) | oficial | vetor → bitmap, 60 fps, arte "line art" |
| 3 | [AQWorlds Infinity Daily Updates #2 — aq2d.com](https://aq2d.com/posts/daily_updates_2025_02/) | oficial | preferência pelo "24 fps Flash" vs. interpolação extrema |
| 4 | [Player Handbook: Combat — aq.com](https://www.aq.com/info/handbook/combat.asp) | oficial | auto-attack, 100 mana, AoE, rest, ranks |
| 5 | [How To Play: The Battle Bar — aq.com](https://www.aq.com/lore/guides/battlebar) | oficial | 5 skills, 1ª é auto-attack, teclas 1–6, cooldown |
| 6 | [Warrior (Class) — aqwwiki](https://aqwwiki.wikidot.com/warrior-class) | wiki | auto-attack 2 s, mana por hit, skills por rank |
| 7 | [Classes — AdventureQuest Worlds Wiki](https://adventurequestworlds.fandom.com/wiki/Classes) | wiki | 5 skills + 2 passivas, 10 ranks |
| 8 | [Class Skills Breakdown — Design Notes](https://www.aq.com/gamedesignnotes/tag/class-skills-breakdown) | oficial | variações de cooldown (1,75 s) e modelos de classe |
| 9 | [AQW Infinity no Steam](https://store.steampowered.com/app/1979810/AdventureQuest_Worlds_Infinity/) | oficial | 60+ fps, cross-platform |
| 10 | [PREVIEW: AQW moving to Unity — MMObomb](https://www.mmobomb.com/adventure-quest-worlds-moving-to-unity-engine-adventure-quest-worlds-infinity) | imprensa | 60 fps vs. limitação do Flash |
| 11 | [Como aumentar o FPS — r/AQW](https://www.reddit.com/r/AQW/comments/118peu1/how_can_i_increase_the_frame_rate_of_the_game/) | comunidade | Flash limitado a ~24 fps |
| 12 | [AdventureQuest Worlds — Wikipédia](https://en.wikipedia.org/wiki/AdventureQuest_Worlds) | referência | Flash, lançamento 2008, MMORPG |
| 13 | [Art style and design research — UAL](https://amgap.myblog.arts.ac.uk/2026/02/18/art-style-and-design-research/) | análise | cel-shading, contornos, VFX sem contorno, smear frames |
| 14 | [Styleized Sprites (Adventure Quest Style) — Unity Discussions](https://discussions.unity.com/t/styleized-sprites-adventure-quest-style/563534) | comunidade | "paper puppet", partes animadas com parent-child |
| 15 | [AQW Design Notes — Class Skin](https://www.aq.com/gamedesignnotes/date/2026/07) | oficial | class variant vs. class skin |

> Acesso em 2026-10-22. Nenhum arquivo, sprite ou texto oficial foi copiado para o pack.

---

## 2. Achados técnicos

### 2.1 Pipeline original
- Todo o jogo foi desenhado e animado em **Flash/Adobe Animate** como **arte vetorial** ("line art") [**1, 2, 12**].
- Monstros, NPCs, armas, armaduras, pets e mapas são **MovieClips** com partes animadas dentro de partes animadas [**1**].
- Cada monstro tem um conjunto de **animações obrigatórias** (Idle, Attack, Walk, Die, etc.) e pode ter outras [**1**].
- Peças são organizadas em **sprite sheets potência de 2** (512, 1024, 2048) [**1**].
- Os **pivôs** eram exportados em arquivos de texto por script para permitir reimportação e alinhamento entre monstros que compartilham animação [**1**].
- AQW Infinity converte o vetor em **bitmap** e reanima com **bones**, com mesh deformation para bosses [**1, 2**].

### 2.2 Animação
- O cliente Flash roda a **~24 fps** (limite da engine, não escolha artística) [**11, 12**].
- Ainda assim, a equipe declara preferência estética pelo "24 fps Flash" — a sensação de anime vem do timing, não da taxa [**3**].
- Infinity roda a **60+ fps**, o que torna a interpolação mais suave — e exige cuidado para não perder peso [**2, 9, 10**].
- A animação é **paper puppet**: partes separadas, parent-child, tweening [**14**].
- VFX usam **smear frames** e não têm contorno [**13**].
- Ciclos de caminhada em jogos 2D dessa família ficam tipicamente entre **8 e 12 frames por passo**; o pack usa 12 por passo (24 por ciclo) para 24 fps.

### 2.3 Combate (verificado)
- 5 skills por classe; a **primeira é o auto-attack** [**5, 7**].
- Auto-attack com **cooldown de 2 s** na maioria das classes; variações de **1,75 s** existem [**6, 8**].
- **Mana é 100** para todos; a regeneração varia por classe [**4**].
- Alvo: clicar uma vez seleciona, clicar de novo ataca; skills sem alvo selecionado auto-selecionam [**4**].
- **Rest** recupera HP/MP fora de combate [**4, 5**].
- Skills são desbloqueadas por **rank** da classe (10 ranks) [**6, 7**].
- Existem **5 skills + 2 passivas** em classes modernas [**7**].

### 2.4 Estilo
- Cel-shading com **contornos pretos fortes** e cores saturadas; VFX sem contorno [**13**].
- Personagens mais saturados que cenários; fundo menos contrastado [**13**].
- AQW sofre com inconsistência entre artistas — o que reforça a necessidade de uma **Visual Bible** e de um **art director** (aqui, a Matriz) [comunidade].

---

## 3. O que o projeto ADOTA

| Achado | Decisão no AURA |
|---|---|
| Paper-doll com partes parent-child | rig de 29 ossos, 29 slots (doc 03) |
| Pivôs em arquivo separado | `rig.json` + `pivot_canvas_px` |
| Power-of-2 | 512² / 1024² / 2048² (doc 02) |
| Animações obrigatórias | matriz de 30 clipes (doc 04) |
| 24 fps como base | autoria 24 / render 60 (ADR-0003) |
| VFX sem contorno | regra dura (doc 07) |
| 5 skills + auto-attack | blueprint de combate (doc 16) |
| Mana 100 + regen por classe | fórmula (doc 16 §5) |
| Auto-attack 2 s | padrão; variantes 1,5–2,2 s |
| Rest fora de combate | HUD e loop (doc 16) |
| Classe = item trocável | sistema de classe (doc 16 §6.9) |
| Bones para bosses | `boss_giant_a` com 40–52 ossos |

## 4. O que o projeto REJEITA

- Copiar sprites, mapas, ícones, fontes ou UI oficiais.
- Reproduzir nomes de itens, facções ou personagens da Artix.
- Usar a estética "suja"/inconsistente de itens antigos.
- Depender de Flash/Animate, Spine ou Unity como formato de entrega.
- Travar o jogo em 24 fps: aqui o timing é 24, a exibição é 60.
- Gradientes suaves em personagem, sombras com blur, textura fotorrealista.
- Animações "ultra suaves" sem holds: perdem peso (risco que o próprio Artix critica em [3]).

---

## 5. Aplicação direta na fluidez (o foco do usuário)

A lição central da pesquisa é que **AQW parece fluido apesar de 24 fps** porque:

1. Usa poses extremas e claras (silhueta).
2. Usa **holds** de 2–4 frames nos momentos de impacto.
3. Usa **antecipação** curta e **recuperação** longa.
4. Usa **secundárias** (capa, cabelo, cauda) que continuam o movimento.
5. Usa **smear** e VFX para vender velocidade.

O AURA implementa exatamente esses cinco pontos de forma mensurável (doc 04 e 05), com a vantagem de renderizar a 60 fps — o melhor dos dois mundos: **timing de 24, suavidade de 60**.

---

## 6. Lacunas de pesquisa (a verificar em fases futuras)

- Número exato de frames dos ciclos originais por classe (não publicado).
- Especificação oficial de pivôs (não pública; inferida do pipeline descrito em [1]).
- Regras de mesh deformation usadas nos bosses de Infinity.
- Curvas de dano/crítico oficiais (wikis divergem).
- Layout exato da HUD por resolução.

Nenhuma dessas lacunas bloqueia o pack: os padrões internos são fechados por decisão própria e documentados.

---

## 7. Nota de propriedade intelectual

AdventureQuest Worlds é propriedade da Artix Entertainment. Dragon Ball é propriedade de seus respectivos titulares (Shueisha, Toei Animation, Bird Studio). Este documento é análise de referência; o pack não contém e não deve conter arquivos oficiais de nenhuma das obras.
