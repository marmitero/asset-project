**Documentação Completa e Detalhada: Estilo de Sprites e Assets do Adventure Quest Worlds (AQW) – Versão 2D Flash Original**

Esta documentação é baseada em análise profunda de fontes oficiais (Design Notes da Artix Entertainment, aq2d.com, aq.com), guias de artistas fãs (aqwart.wikidot.com), extratores de SWF, templates oficiais/fãs, posts de artistas como Nulgath/Miltonius, Dage, Lae, J6 e outros, screenshots, e processos de conversão para AQW Infinity/Unity. O objetivo é fornecer **tudo** necessário para um Agent AI (como o do Arena.ai) recriar um **asset pack completo** inspirado em AQW: estética cartoon fantasia 2D vetorial modular, mecânicas de MMO casual real-time, classes, customização, etc. Seja extremamente fiel ao estilo clássico Flash (2008–atual, pré-rasterização pesada).

**Aviso legal/inspiração**: Use apenas para inspiração e criação original. Não copie assets oficiais (violação de ToS). Foque em “estética/mecânica inspirada”.

### 1. Estilo de Arte Geral (Core Aesthetic)
- **Tipo**: Cartoon fantasy comic-book exagerado, vibrante, heroico/cômico. Mistura de anime ocidentalizado + comic americano + chibi-heróico. Não é pixel art; é **vetorial limpo** (Adobe Flash/Animate originalmente).
- **Características-chave**:
  - Linhas pretas ousadas e limpas (hairline preferencialmente 0.10 pt para performance e estilo clássico). Evite linhas grossas irregulares.
  - Preenchimentos flat (sólidos) com cel-shading: blocos de cor sólida para sombras e highlights (não blending suave excessivo).
  - Cores saturadas e vibrantes (vermelhos intensos, azuis elétricos, dourados brilhantes, pretos profundos para facções “evil”). Paleta limitada por item (5–8 tons principais).
  - **Fonte de luz consistente**: Sempre de cima-frente (slightly above and in front of the head). Sombras caem para baixo-trás. Isso cria o “look AQW” icônico.
  - Shading clássico (especialmente Miltonius/Nulgath early style e otimizações): 
    - 1 cor base + 1–2 tons escuros (sombra) + 1–3 highlights.
    - “Half-shadow”/silhueta: Membros traseiros (braço/perna de trás) frequentemente escurecidos ou pretos puros para depth, otimização de lag (Flash single-core) e estilo. Membros da frente mais detalhados e iluminados.
    - Evite gradients excessivos (causam lag; use só para efeitos especiais como metal brilhante ou fogo). Prefer solid shapes.
    - Materiais distintos: Metal (highlights afiados + trims), Couro (sombras suaves), Tecido (folds suaves), Glow/mágico (add blend ou cores neon).
  - Proporções estilizadas (não realistas): Cabeça relativamente grande (heroic/chibi), torso atlético, membros alongados ou musculosos conforme classe/armadura. Homens mais angulares/musculares; mulheres curvilíneas mas balanceadas (não hiper-sexualizadas no base). Altura base ~ heroico médio. Armas **oversized** (fantasia exagerada).
  - Silhueta forte e legível mesmo em miniatura. Detalhes ornamentados (spikes, runas, gemas, asas) especialmente em sets “prestige” (Nulgath Nation, Undead Legion/Dage, Chaos Lords).
  - Evolução: Early (simples, low-lag) → Mid (camadas complexas, blend modes) → Late (mais detalhe, animações embutidas). Para pack: Misture, priorizando legibilidade + performance.
- **Ferramentas originais**: Adobe Flash/Animate (vetor + MovieClips/símbolos + timeline). Para replicar moderno: Adobe Animate, Inkscape, Illustrator + export raster, ou Aseprite/Photoshop para sheets + Spine/DragonBones para skeletal se quiser evoluir. Em engines (Unity/Godot): Sprite sheets + atlases (potências de 2: 512/1024/2048).

**Dicas de artistas (de guias fãs e Lae/Nulgath)**: Zoom out frequentemente para checar flow geral. Consistência de ângulo/luz. Trims (detalhes de borda) adicionam muito. Salve obsessivamente. Evite symbols por peça de membro (um symbol por limb com layers internas reduz lag/file size).

### 2. Composição dos Sprites / Personagens (Modular System – O Coração do AQW)
Personagens são **extremamente modulares** (é o que permite milhares de itens e customização). Tudo é MovieClip/símbolo separado com pivots/registration points precisos para joints.

**Base Body (Templates masculinos e femininos separados)**:
- Partes: Cabeça (com face base, olhos, boca para blink/expressões), Torso/Upper Body, Upper Arms (L/R), Forearms/Hands (L/R, com poses de grip para armas), Thighs (L/R), Shins/Calves (L/R), Feet (front view + side view para profundidade).
- Skin base color customizável.
- Underwear/clothes base (para armors parciais).
- Pivots críticos: Ombros, cotovelos, pulsos, quadris, joelhos, tornozelos, pescoço. Centro de gravidade para shadows/hitboxes.
- Proporções tipicas (relativas à cabeça = 1 unidade): Torso ~1–1.5, pernas ~2–2.5 total, braços proporcionais. Ajuste por gender (fêmeas com hips mais largos, peito sutil).
- Templates fãs/oficiais existem (ex: body packs com arms/hands/thighs/shins/feet). Use como base.

**Camadas de Equip (Z-order/layering estrito)**:
1. Shadow no chão (elipse simples, escala com personagem).
2. Cape/Back item (atrás de tudo, animado com sway).
3. Back limbs (escurecidos).
4. Torso/Armor body.
5. Front limbs.
6. Helm (sobre cabeça; pode incluir hair color custom separado).
7. Hair (se helm não cobre).
8. Weapon (na mão da frente, com grip poses).
9. Pet (offset atrás/lado, follow behavior).
10. Effects/Auras (sobre ou sob).
- Armors: Peças separadas (chestplate, pauldrons L/R, greaves, gauntlets, boots, belt) ou full-body overlays. Muitas usam color masks (áreas específicas recoloráveis: skin, cloth, metal accents, eyes).
- Helms: Full face-cover ou hat+hair. Faces estilizadas (olhos grandes expressivos).
- Capes: Longas, flowing, com cloth physics simples (keyframes de sway).
- Gender morph: Muitos itens têm versões M/F.

**Animações (MovieClips com timeline ou frame-by-frame + tweens)**:
- Idle: Breathing sutil + blink (2–4 frames eyes) + slight sway. Loop seamless.
- Walk/Run: Classic cycle (8–12 frames). Opposite arm/leg, bounce no torso, foot plant. Direção: Face movement ou target.
- Attack/Auto-attack: Swing weapon + body twist (4–8 frames). Hit frame com impact.
- Skills: Full body pose + VFX trigger. Unique por classe.
- Jump, Death (fall + dissolve/poof), Emotes (wave, dance, laugh – muitos exclusivos Legend).
- Combat: Target lock, skill cast com wind-up.
- FPS original ~24 (Flash limit). Para moderno: 30–60 com smooth.
- Em Infinity/conversão: Muitas viram skeletal (bones) ou sprite sheets com pivots. Normal monsters: frame sheets; bosses: bones para breathing/subtle.

**Escala**: Personagens base ~150–250px altura dependendo da resolução da cena. Consistente entre players/NPCs. Monstros variam (tiny to screen-filling bosses).

### 3. Movimentação e Mecânicas de Personagem
- Original: Click-to-move (mouse hover + click; setas douradas/prata no chão para screens/rooms).
- Moderno inspirado: WASD + mouse look/target.
- Free 2D plane (não grid rígido), com colliders (árvores, rochas, players não se sobrepõem perfeitamente).
- Facing: Direção de movimento ou inimigo.
- Multiplayer rooms: Limite de players, instâncias.
- Classes: Base (Warrior/Mage/Rogue/Healer) + avançadas (100+). Cada tem skill bar única (geralmente 5 skills + auto). Stats: HP/MP, Str/Int/Dex etc., enhancements.
- Combat real-time: Auto-attack + skills com mana/CD. AoE, DoT, buffs/debuffs, auras.

### 4. Efeitos, Skills e VFX
- **Hand-drawn frame-by-frame** + particles (Infinity mistura).
- Exemplos: Fogo (sprite sheet de chamas individuas frames), slashes (arcs brilhantes), magia (círculos, orbs, lightning bolts), heals (glows verdes/dourados), explosions, auras (outline glow + floating particles).
- Blend modes: Add/Screen para glows, Multiply para sombras.
- Skills: Ícones no battle bar (com CD radial gray-out). Anim no char + projectile/AoE + screen shake + hit flash/numbers.
- Auras: Stacks visíveis, timers, tooltips. Party/target tracking.
- Performance: Otimize (poucos layers, atlas).

**Para pack**: Packs de VFX por elemento (Fire/Ice/Energy/Dark/Light/Chaos) + generic (slash, impact, buff).

### 5. Mascotes / Pets
- Companheiros que follow o player (offset atrás/lado).
- Variados: Animais fofos, monstrinhos, Moglins (icônicos, fofos com orelhas/chifres), objetos animados, battlepets (atacam).
- Anims: Idle bob/float, walk, attack (se battle), special.
- Color custom ou temáticos. Bank pets (storage).
- Tamanho pequeno (1/3–1/2 do player). Z-order atrás.

**Quantidade no pack**: 20–50 samples (cute, epic, funny, elemental).

### 6. Itens, Armaduras, Armas, Helms, Capes etc.
- **Armaduras**: Full sets temáticos (ex: Undead Legion blue-fire, Nulgath spiky dark, Chaos chaotic, starter simple). Peças modulares ou full. Detalhe alto em prestige (layers stacked).
- **Armas**: Swords, daggers, staves, axes, guns, polearms, bows, wands, gauntlets, whips... Oversized, detalhados (runas, glows, effects embutidos). Grip poses.
- **Helms/Back/Capes**: Complementam. Capes animated.
- **Outros**: House items, ground items, consumables icons.
- Color custom: Máscaras específicas (ex: cloth parts recoloráveis independentemente de metal).
- Raridade visual: Free (simples), AC/Member (elaborados), Rare/Seasonal (únicos).
- Ícones de inventário: Versões simplificadas/cropped dos sprites.

**Para pack**: Bases + 5–10 sets completos por tema (Good/Evil/Elemental/Starter/Prestige) + 50+ armas + helms/capes.

### 7. HUD / Interface do Usuário
- **Layout clássico**:
  - Top-left: Portrait (rosto do char), Nome, Classe + Rank, HP bar (vermelho), MP bar (azul), Level, Quest log (“!”).
  - Bottom (Battle Bar): Skills icons (com CD), Chat input + log (cores: blue players, gold mods, purple PM, green guild, red warnings), Gold counter, XP bar (roxo), Class Points bar (verde), botões (Inventory, Options, Book of Lore, House, Quests, Character panel).
  - Chat expandível, emotes.
  - Outros: Mini progress meters (wars), party frames, aura displays (draggable), loot bags, map arrows (gold/silver).
- Estilo: Fantasy ornate frames (dourado/bege com bevels, glows), botões 3D-ish, cores accent (gold, red, blue, purple). Clean mas themed. Hide UI option.
- APOPs (NPC popups): Speech bubbles + colunas de botões (Quest/Shop/Talk). Auto-generated em Infinity, manual no Flash.
- Inventário: Grid/list com tabs, enhance, equip, trash. Temporary inventory para quest items.
- Ícones: Consistentes, legíveis.

**Para pack**: Full UI kit (bars, frames, buttons, icons, fonts stylized, portraits base, skill icon templates, chat bubbles).

### 8. Mapas, Backgrounds, Ambientes
- Cenas hand-drawn layered (FG/MG/BG para depth/parallax leve).
- Multi-screen rooms conectados por arrows.
- Temas: Towns (Battleon hub com shops/inn/forge/library), Forests, Castles, Caves, Dungeons, Seasonal (Halloween, Christmas), Chaos/Undead/Elemental zones.
- Elementos: Props animados (água, fogo, flags, NPCs idle), colliders, portals, spawn points, interactive.
- Tiles/props reutilizáveis + large unique backgrounds.
- White map etc. para screenshots.

**Para pack**: Tile sets + 5–10 full maps sample (hub + dungeon + outdoor) + props pack + parallax layers.

### 9. NPCs, Monstros, Lojas, Skills Icons, Tudo Mais
- **NPCs**: Estilo player mas designs únicos (quest givers, shopkeepers como Cysero, Twilly Moglin). Idle anims (blink, sway), dialogue trees, APOPs. Full actor em Infinity (player anims).
- **Monstros**: Modular ou full body. Sizes variados. Anims obrigatórias: Idle, Walk, Attack, Die, Hit. Bosses complexos (bones ou multi-parts). Drop loot bags. Portraits.
- **Lojas**: UI inventário-like (buy/sell, currencies Gold/AC). Categorias.
- **Skills Icons**: Square/circular, themed, com glow variants.
- **Cutscenes**: Dialog (talking heads) + Cinematic (full anim com player inserted). Speech bubbles, fades.
- **Outros**: Emotes, house guests, badges, character page backgrounds, loading screens, logos.

### 10. Como Replicar Completamente para Asset Pack (Instruções para Agent AI)
**Estrutura do Pack Recomendada**:
1. **Style Guide PDF/MD**: Light source diagram, shading steps (com exemplos Lae-style), line weights, proportions chart, color palettes por facção, dos/don’ts (no heavy gradients, consistent light, half-shadow option).
2. **Base Templates**: Male/Female body parts (PNG layers + pivots JSON ou PSD/AI/FLA). Mr. Guy/Ms. Girl gray/white dummies para testing/color custom.
3. **Modular Equip System**: Slots definidos (Armor body, Helm, Cape, Weapon L/R, Pet, Aura...). Prefabs com Z-order.
4. **Animation Sets**: Sprite sheets (ou skeletal) para Idle/Walk/Attack/Skills/Death/Emotes. Frame data JSON. 8–16 frames típicos.
5. **VFX Pack**: Elemental sheets + particles + blend instructions.
6. **Item Libraries**:  Categories (Armors 20+, Weapons 50+, Pets 30+, Helms/Capes 20+, etc.) com color masks, icons, variants M/F.
7. **HUD/UI Kit**: Todos os elementos + states (hover, pressed, disabled, CD).
8. **Environment Pack**: Tiles, props,  sample maps (com collision data), backgrounds layered.
9. **Characters**: Sample classes (base 4 + 5 advanced), NPCs 10+, Monsters 20+ (mobs + bosses).
10. **Extras**: Skill icons, loot, shop UIs, cutscene templates, fonts, SFX suggestions (upbeat rock/fantasy), music loops.
11. **Tech Specs**: Resolutions (base 800x600-ish original, scalable), atlas packing, pivot docs, export pipelines (vector → raster flatten com masks), performance notes (limit layers/transparency), engine examples (Unity 2D, Godot).
12. **Mechanics Inspiration Doc**: Class system, combat loop, quest structure (weekly releases feel), inventory, multiplayer rooms, progression (XP/CP/Ranks), currencies, customization flow.
13. **Variations**: Early simple vs late detailed; Good vs Evil aesthetics; Seasonal.

**Processo de Criação Recomendado (para AI ou artistas)**:
- Comece com templates base.
- Desenhe em vetor (ou raster high-res com outlines clean).
- Aplique shading solid blocks + light source.
- Separe layers/pivots.
- Anime key poses → inbetweens.
- Teste em dummy com color custom.
- Exporte sheets (power-of-2) + metadata.
- Para complex: Stack layers, add blend/effects.
- Otimize: Reduza symbols, flatte n quando possível.

**Referências Visuais Chave** (pesquise/inspire-se em): Screenshots aq.com, AshiraZone catalog, AQ Closet (live try-on), Design Notes art, fan galleries (Pinwheel etc.), Infinity behind-the-scenes (hand-drawn fire sheets + particles), templates DeviantArt/fãs.

**Nível de Detalhe**: Da base (linhas 0.10, luz upper-front, 5 tons) até avançado (camadas blend, skeletal breathing, color masks precisas, multi-screen maps com arrows, full skill VFX pipelines, APOP systems). Tudo documentado com exemplos descritivos, medidas relativas, checklists de consistência.

Este pack permitirá criar um jogo completo com a “alma” AQW: customização infinita, classes divertidas, mundo em expansão semanal, cartoon vibrante e combat casual real-time. Se precisar de expansões (ex: JSON schemas específicos, prompts de geração de imagem para AI art, ou samples de código), forneça mais detalhes!

**Battle on!** Fontes principais citadas implicitamente via pesquisa (aq.com, aq2d.com, wikis, artist guides, Reddit/X posts de devs/artistas).