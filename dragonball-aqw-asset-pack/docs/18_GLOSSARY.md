# 18 — GLOSSARY
**Projeto AURA · v1.0.0**

| Termo | EN | Definição |
|---|---|---|
| **Actor** | actor | Instância jogável de um personagem: rig + slots + animator + estado. |
| **Attachment** | attachment | PNG preso a um slot/osso (peça de corpo, arma, cabelo). |
| **Atlas** | atlas | Textura potência de 2 com vários sprites + JSON de coordenadas. |
| **Baked** | baked | Animação pré-renderizada em spritesheet, em vez de calculada em runtime. |
| **Bone** | bone / osso | Segmento do esqueleto com posição, rotação e pai. |
| **Cancel window** | cancel window | Intervalo de frames em que uma animação pode ser interrompida. |
| **Cel-shading** | cel shading | Sombreamento em blocos chapados, sem gradiente. |
| **Clip** | clip | Animação completa (idle, run, attack…). |
| **Combo window** | combo window | Janela para encadear o próximo ataque. |
| **Continuity** | continuity | Origem canônica (DB, DBZ, DBS, GT, filmes). |
| **Coverage** | covers[] | Quais slots uma peça de equipamento substitui. |
| **Depth sort** | depth sorting | Ordenação de atores por `foot_y` para simular profundidade. |
| **Easing** | easing | Curva de aceleração de um keyframe. |
| **FOOT_Y** | foot y | Coordenada Y do pé no chão; define ordem de desenho. |
| **Frame de fechamento** | closing frame | Frame `N` idêntico ao `0` que fecha um loop. |
| **Gap de junta** | joint gap | Pixel de fundo visível entre duas peças articuladas. |
| **GIF** | gif | Preview de validação a 25 fps; não é master. |
| **Grip** | grip | Ponto de empunhadura de uma arma. |
| **Hitbox / Hurtbox** | hitbox / hurtbox | Área que causa dano / área que recebe dano. |
| **Hitstop** | hitstop | Congelamento breve no impacto para dar peso. |
| **Hold** | hold | Manter uma pose por 1–4 frames. |
| **IK** | inverse kinematics | Cálculo de juntas a partir da posição do pé/mão. |
| **Interpolação** | tweening | Cálculo de poses intermediárias entre keyframes. |
| **Key pose** | key pose | Pose principal que define a ação. |
| **Layer** | layer | Ordem de desenho (0–160) definida em `layer_order.json`. |
| **Ledger** | ledger | Registro de sessões e gerações. |
| **Loop** | loop | Animação cíclica. |
| **Máscara** | mask | PNG grayscale que define área recolorível. |
| **Matriz** | matrix | Conjunto congelado de padrões (rig, escala, paleta, clipes). |
| **Overlap** | overlap | Sobreposição de 2–3 px nas juntas para evitar fenda. |
| **Paper-doll** | paper doll | Personagem montado por peças substituíveis. |
| **Parallax** | parallax | Deslocamento relativo das camadas de cenário. |
| **Pivô** | pivot | Ponto de rotação de uma peça; coincide com a junta. |
| **Potência de 2** | power of two | 512, 1024, 2048 — tamanhos de canvas/atlas. |
| **Retarget** | retarget | Reutilizar animação de um rig em outro compatível. |
| **Rest pose** | rest pose | Pose de repouso (A-pose) do esqueleto. |
| **Rubrica** | rubric | Ficha de avaliação de fluidez (30 pontos). |
| **SemVer** | semver | Versionamento MAJOR.MINOR.PATCH. |
| **Secundária** | secondary motion | Movimento derivado (cabelo, capa, cauda). |
| **Skeletal** | skeletal | Animação por ossos em runtime. |
| **Slot** | slot | Camada lógica que recebe um attachment. |
| **Smear** | smear | Frame de borrão/arco que exagera velocidade. |
| **Socket** | socket | Ponto de emissão (mão, boca, peito) preso a um osso. |
| **Spritesheet** | sprite sheet | Grade de frames em uma textura. |
| **Spring** | spring | Mola amortecida usada em secundárias. |
| **Straight alpha** | straight alpha | Alpha não premultiplicado (padrão do pack). |
| **Tier** | tier | Prioridade T0–T3 do catálogo. |
| **Trail** | trail | Rastro de arma/energia. |
| **Transformation** | form | Estado do personagem (SSJ, SSB, UI…). |
| **Trim** | trim | Recorte de bounding box com offset registrado. |
| **VFX** | visual effects | Efeitos: slash, impacto, explosão, aura. |
| **9-slice** | nine-slice | Técnica de painel escalável com insets. |
| **ADR** | architecture decision record | Registro de decisão com contexto e consequências. |
| **Gate** | gate | Ponto de aprovação obrigatório (G0–G5). |
| **A-pose** | A-pose | Pose de repouso com braços a 22° do tronco. |
| **Baked sheet** | baked sheet | Ver *spritesheet*. |
| **Chroma key** | chroma key | Fundo removível por cor; proibido no pack. |
| **Draw call** | draw call | Chamada de render; orçamento ≤ 26/personagem. |
| **PPU** | pixels per unit | 100 px = 1 m no pack. |
| **Sprint/Corrida** | run | Ciclo de 16 frames a 340 px/s. |
| **Walk** | walk | Ciclo de 24 frames a 140 px/s. |
| **Whiff** | whiff | Ataque que erra; animação `attack_whiff`. |
| **UI theme** | ui theme | `ui_theme.json` com cores, fontes e insets. |
