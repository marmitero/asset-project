Para criar um **Asset Pack completo** inspirado no clássico estilo 2D Flash de *AdventureQuest Worlds (AQW)* e fornecer um manual técnico e artístico perfeito para o **Agent AI do Arena.ai**, precisamos desconstruir a anatomia do jogo. 

O AQW original foi feito no Adobe Flash (hoje Adobe Animate), usando arte vetorial e animação modular (Skeletal/Tweening). Para replicar isso hoje em engines modernas (Unity, Godot, etc.), o sistema ideal é o de **Paper Doll (Boneco de Papel)** com animação esqueletal (estilo Spine 2D ou DragonBones).

Abaixo está o **Documento de Design Técnico e Artístico (GDD/TDD)** detalhado. O Agent AI deve seguir estas diretrizes estritamente para gerar os assets.

---

# 📚 DOCUMENTO DE DIRETRIZES: PROJETO AQW-LIKE (ASSET PACK)

## 1. ESTILO DE ARTE E IDENTIDADE VISUAL (A ESTÉTICA)
A arte de AQW é uma mistura de alta fantasia, anime e elementos exagerados (armas gigantes, caveiras brilhantes). A estética baseia-se fortemente em gráficos vetoriais convertidos para sprites.

*   **Lineart (Contornos):** Linhas pretas (ou cores muito escuras) fortes, grossas e nítidas nos contornos externos. Linhas internas para detalhes musculares ou da armadura devem ser ligeiramente mais finas. A espessura da linha deve ser **consistente** em todos os itens.
*   **Pintura e Sombreamento (Cel-Shading):** Nada de gradientes suaves (exceto em efeitos mágicos). O sombreamento usa a regra de 3 tons:
    1.  **Cor Base:** Cor sólida e plana.
    2.  **Sombra (Hard Shadow):** Recortes secos e definidos (geralmente preto em 20-30% de opacidade, ou uma versão muito mais escura da cor base).
    3.  **Brilho (Hard Highlight):** Recortes nítidos de luz pura (branco ou cor clara em baixa opacidade), geralmente nas bordas superiores ou metálicas.
*   **Proporções:** Cabeças ligeiramente maiores que o normal (para destacar os capacetes e feições), mãos simplificadas (muitas vezes parecendo luvas ou com dedos menos detalhados), pés grandes e estáveis. Tronco atlético, mas estilizado.

---

## 2. ESTRUTURA DO PERSONAGEM (SISTEMA PAPER-DOLL)
O Agent AI **NÃO** deve desenhar personagens inteiros e estáticos. Tudo deve ser gerado como peças modulares soltas em um fundo transparente (PNG) e depois empacotadas em um Sprite Sheet (potências de 2: 1024x1024, 2048x2048).

### 2.1. Lista de Partes do Corpo (Z-Index do Fundo para a Frente)
O AI deve separar cada design de armadura e corpo nas seguintes partes exatas, com seus respectivos **Pontos de Pivô (Pivot Points / Joints)**:
1.  **Capa/Asas (Cape/Back):** Fica atrás de tudo. Pivô: Base do pescoço/costas.
2.  **Cabelo Traseiro (Back Hair):** Fica atrás da cabeça/corpo.
3.  **Arma Traseira (Back Weapon - se empunhadura dupla):** Atrás do corpo.
4.  **Braço Traseiro - Superior (Back Upper Arm):** Pivô: Ombro traseiro.
5.  **Braço Traseiro - Inferior (Back Lower Arm):** Pivô: Cotovelo traseiro.
6.  **Mão Traseira (Back Hand):** Pivô: Pulso traseiro.
7.  **Perna Traseira - Coxa (Back Upper Leg):** Pivô: Quadril traseiro.
8.  **Perna Traseira - Canela/Bota (Back Lower Leg):** Pivô: Joelho traseiro.
9.  **Pé Traseiro (Back Foot):** Pivô: Tornozelo.
10. **Pélvis/Cintura (Pelvis):** Pivô: Centro de gravidade (Root bone).
11. **Tronco/Peitoral (Torso/Chest):** Pivô: Base da coluna (conecta na Pélvis).
12. **Perna Frontal - Coxa (Front Upper Leg):** Pivô: Quadril frontal.
13. **Perna Frontal - Canela/Bota (Front Lower Leg):** Pivô: Joelho frontal.
14. **Pé Frontal (Front Foot):** Pivô: Tornozelo.
15. **Cabeça (Base Head/Face):** Pivô: Pescoço. Contém as expressões faciais.
16. **Capacete / Cabelo Frontal (Helm / Front Hair):** Substitui ou sobrepõe o cabelo, ancorado na cabeça.
17. **Ombreiras (Shoulders):** Ancoradas no tronco, mas cobrindo as juntas dos ombros.
18. **Braço Frontal - Superior (Front Upper Arm):** Pivô: Ombro frontal.
19. **Braço Frontal - Inferior (Front Lower Arm):** Pivô: Cotovelo frontal.
20. **Mão Frontal (Front Hand):** Pivô: Pulso frontal.
21. **Arma Frontal (Main Weapon):** Fica presa à mão frontal.

**Instrução para a AI (Geração de Assets):** Ao gerar uma "Nova Armadura", a AI deve gerar todas essas partes separadamente com um design coeso.

---

## 3. ANIMAÇÃO E MOVIMENTAÇÃO (SKELETAL RIGGING)
Em vez de desenhar frame-por-frame (o que gera lag e gasta memória), AQW usa interpolação (tweening) das peças modulares. O AI precisa entender o fluxo dos frames-chave para replicar o loop:

*   **Idle (Parado):** Respiração. O torso achata levemente no eixo Y e expande no eixo X. Os braços giram poucos graus para cima e para baixo. A capa ondula usando deformação de malha (mesh deformation) suave.
*   **Run (Correndo):** Um ciclo de caminhada clássico de Flash. O torso inclina-se para a frente (~15 graus). Pernas alternam em movimentos de pêndulo amplos. Os braços balançam exageradamente no sentido oposto das pernas. A arma frontal acompanha a mão rotacionando ligeiramente para trás pela gravidade.
*   **Attack (Ataque Melee):** O personagem recua o braço e o torso (antecipação), dá uma estocada ou balanço rápido para frente (impacto) e retorna à pose de Idle.
*   **Cast (Magia):** Personagem levanta a mão frontal ou a arma aos céus. O tronco estica.

---

## 4. ITENS, ARMADURAS E ARMAS (EQUIPAMENTOS)
A economia visual do jogo depende de itens incrivelmente chamativos. 
*   **Armas (Weapons):** Extremamente exageradas, maiores que as reais. Espadas costumam ter quase o tamanho do personagem. 
    *   *Tipos:* Espadas, Adagas (Daggers - empunhadura dupla), Cajados (Staffs - topo pesado com joias/cristais brilhantes), Machados e Lanças.
    *   *Âncora (Anchor Point):* O Sprite da arma deve ter o cabo claramente definido onde o ponto central (pivot) se alinhará com a Mão Frontal.
*   **Armaduras (Armors):** No AQW original, as armaduras não vestem "por cima" de um corpo base. Elas **substituem** os braços, pernas, tronco e pélvis da arte padrão por novas versões desenhadas com a armadura.
*   **Helmos/Capacetes (Helms):** Têm versões "Morph" (substituem a cabeça toda por um rosto de monstro, por exemplo) ou "Hat" (encaixam por cima do rosto base do personagem).

---

## 5. MASCOTES (PETS) E MONSTROS
*   **Pets:** Acompanham o jogador. Proporção: Geralmente 1/3 a 1/4 da altura do jogador. Para evitar peso de processamento, têm rigs ultrassimplificados. Um dragãozinho de estimação pode ter apenas 4 partes: Cabeça, Tronco, Asa Traseira e Asa Frontal (animadas em loop de voo).
*   **Monstros:** O método de criação é o mesmo do jogador (separado em partes), mas a estrutura óssea muda. Um dragão chefe terá: Focinho, Mandíbula, Pescoço (várias partes), Tronco, Patas e Cauda (dividida em várias seções para fazer um movimento de chicote). O AI deve gerar essas partes soltas.

---

## 6. EFEITOS VISUAIS E SKILLS (VFX)
A mágica de AQW não usa simulação complexa de partículas, mas sim **sprites vetoriais animados em Blend Modes (Screen / Additive).**
*   **Ataque Básico:** Um rastro de luz de corte (Slash), gerado como um arco branco e amarelo/vermelho com opacidade desvanecendo (fade out).
*   **Feitiços (Spells):** Formas geométricas puras (Círculos mágicos com runas, explosões em forma de estrelas ou chamas simplificadas). Cores vibrantes (Ciano, Magenta, Laranja fluorescente).
*   **Instruções para AI:** Para VFX, a AI deve desenhar Sprites Mágicos como folhas de textura independentes (ex: 5 frames de uma labareda de fogo subindo), com fundo transparente para ser inserido com brilho na engine do jogo.

---

## 7. CENÁRIOS, MAPAS E AMBIENTES (ENVIRONMENTS)
Os mapas do jogo simulam profundidade 3D em um espaço bidimensional (2.5D ou perspectiva plana).
*   **Camadas do Mapa (Parallax Layers):**
    1.  **Far Background (Céu/Sol/Lua):** Move-se muito pouco.
    2.  **Mid Background (Montanhas, Castelos, Florestas ao fundo):** Move-se com velocidade moderada.
    3.  **Playable Area (Chão/Terreno):** Onde os jogadores andam. A perspectiva não é totalmente de lado (plataforma), mas sim levemente isométrica, permitindo que o personagem suba e desça no eixo Y.
    4.  **Foreground (Árvores, Colunas, Sombras na frente da câmera):** Fica na frente do jogador e move-se mais rápido para criar ilusão de profundidade.
*   **Instrução para AI:** Ao gerar um "Mapa de Floresta Sombria", a AI deve produzir PNGs de **árvores soltas, arbustos soltos, chãos texturizados ladrilháveis (tileable platforms/ground) e fundos de céu pintados.** Tudo sem contornos grossos nos cenários (ao contrário dos personagens, os cenários têm contornos sutis ou inexistentes para não roubarem a atenção da tela).

---

## 8. INTERFACE DE USUÁRIO (HUD / UI)
O layout do AQW é utilitário, evocando a estética de MMOs antigos (ex: WoW), mas minimalista.
*   **Estilo Visual da UI:** Bordas em pedra, mármore negro ou metal desgastado. Detalhes em ouro velho e joias incrustadas nas quinas.
*   **Top-Left (Jogador):** Retrato do jogador com moldura circular, Barra de Vida (Vermelho forte), Barra de Mana (Azul forte) horizontais.
*   **Top-Center (Alvo):** Mesmo estilo do jogador, mas para o monstro sendo mirado.
*   **Bottom-Center (Action Bar):** Slots quadrados (1, 2, 3, 4, 5). Ícones das habilidades devem ser minimalistas (uma espada pingando sangue, um raio azul, um coração verde cruzado) com um leve chanfro interno e brilho.
*   **Menus (Inventário e Lojas):** Painéis retangulares opacos (fundo escuro com leve transparência - alpha 80%), botões de fechar (X vermelho clássico em cima à direita).

---

## 🚀 INSTRUÇÕES DE PROMPTING (ENGENHARIA) PARA O AGENT AI DO ARENA.AI
Para que a Inteligência Artificial consiga entender e montar isso, toda requisição que o Agent AI fizer (para seu próprio sistema de geração de imagens) deve obedecer ao seguinte formato rigoroso:

### Template de Geração de Personagem/Armadura:
> *"Gere um sprite sheet de armadura de fantasia estilo 2D Flash game em resolução 4K (Power of 2). O estilo de arte deve ser cel-shaded vetorial com contornos pretos, fortes e nítidos. Sem fundo (transparent PNG). As partes do corpo devem estar espalhadas em T-pose desmembrada, sem se tocarem. As partes devem incluir: cabeça separada, tronco separado, ombros separados, braço superior, braço inferior, mãos em formato de luva/garra, pélvis, coxa, canela e bota. Cores base planas com apenas uma camada dura de sombra e uma camada dura de iluminação (hard edge shadows). O design deve ser [INSERIR TEMA: ex. Cavaleiro das Sombras com detalhes em roxo brilhante]."*

### Template de Geração de Arma:
> *"Gere um sprite 2D de uma [TIPO DE ARMA: ex. Espada Larga] de fantasia exagerada, estilo Flash game de navegador. Contornos pretos fortes, preenchimento vetorizado cel-shaded. A lâmina deve ser absurdamente grande em relação ao cabo. O cabo deve estar alinhado reto horizontal ou verticalmente para permitir a configuração exata do ponto de pivô (anchor point) pelo desenvolvedor. Fundo transparente."*

### Template de Geração de Cenário:
> *"Gere componentes 2D para um mapa de jogo side-scrolling plano. Arte digital polida, cores vibrantes com paleta atmosférica, sem contornos grossos. O cenário não deve ser mesclado. Gere como camadas distintas (Layers): Um fundo de céu infinito (Far BG), silhuetas de montanhas com detalhes estilizados (Mid BG), o terreno texturizado achatado para área de caminhada e adereços (Props) como árvores e pedras separadas, permitindo a montagem e organização pelo eixo-Z para efeitos de parallax. Tema: [INSERIR TEMA]."*

### Metadados (Para o Asset Pack ser funcional)
O Agente AI deve gerar, junto com a imagem, um arquivo estruturado JSON que define a localização das partes. Por exemplo (esquema genérico):
```json
{
  "item_type": "Armor",
  "name": "Shadow_Knight_Armor",
  "parts": {
    "Torso": { "x": 100, "y": 200, "width": 80, "height": 120, "pivotX": 0.5, "pivotY": 0.9 },
    "LeftArmUpper": { "x": 300, "y": 200, "width": 40, "height": 60, "pivotX": 0.5, "pivotY": 0.1 }
  }
}
```

Seguindo esse manual, o **Agent AI do Arena.ai** será capaz de gerar centenas de itens, monstros, feitiços e mapas que se encaixam de forma 100% harmoniosa, permitindo montar um "clone" ou sucessor espiritual do AQW com precisão mecânica, baixo peso de performance e o charme inconfundível dos antigos RPGs de navegador.