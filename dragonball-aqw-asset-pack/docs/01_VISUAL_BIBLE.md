# 01 — VISUAL BIBLE
**Projeto AURA · Versão 1.0.0 · Fase 1**
Este é o documento de autoridade visual. Todo asset — personagem, arma, VFX, mapa, ícone — deve poder ser julgado por ele sem consultar outro arquivo.

---

## 1. DNA do estilo em uma página

| Atributo | Regra |
|---|---|
| **Linguagem** | Cartoon-heroico vetorial, derivado do Flash. Não é pixel art, não é pintura digital, não é anime detalhado. |
| **Contorno** | Preto quase puro (`#0E0B12`), fechado, de espessura constante, com cantos levemente arredondados. |
| **Preenchimento** | Cor chapada + **1 sombra dura** + **1 brilho duro**. Sem gradiente suave (exceto energia). |
| **Luz** | Única, vinda de cima e à frente (`azimute 315°`, `elevação 55°`). Sombra sempre para baixo/trás. |
| **Proporção** | Heroica estilizada: cabeça grande, mãos expressivas, pés firmes, membros longos. |
| **Leitura** | Silhueta reconhecível a 48 px de altura. Arma e cabelo carregam a identidade. |
| **Movimento** | Peso e antecipação; nunca flutuação. Ver doc 04. |
| **Contraste** | Personagem saturado e escuro no contorno; cenário mais claro, menos saturado, sem contorno grosso. |
| **Densidade** | Máximo 8 cores por design + contorno. Detalhe interno só onde agrega leitura. |

### 1.1 O que "parecer AQW" significa (e o que não significa)

**Significa:** silhueta limpa, cel-shading duro, membros traseiros escurecidos, armas exageradas, equipamento que substitui partes do corpo, expressão facial cartoon, VFX sem contorno.

**Não significa:** copiar traço de artista específico, reproduzir itens, usar a fonte ou a paleta exata da Artix, imitar o HUD pixel a pixel.

---

## 2. Linha (line art)

### 2.1 Pesos canônicos

Referência: personagem adulto = **220 px** de altura (`standards/canvas_and_scale.json`).

| Uso | Peso @220 px | Peso @440 px (2×) | Cor |
|---|---|---|---|
| Contorno externo (silhueta) | **3,0 px** | 6,0 px | `#0E0B12` |
| Contorno interno de peça (divisória de armadura, dobra forte) | **1,8 px** | 3,6 px | `#0E0B12` a 92% |
| Linha de detalhe (costura, emenda, unha) | **1,2 px** | 2,4 px | `#0E0B12` a 75% |
| Linha de expressão (sobrancelha, boca) | **1,6 px** | 3,2 px | `#2A1F2E` |
| Linha de cabelo interna | **1,4 px** | 2,8 px | `#0E0B12` |

**Fórmula de escala:** `peso_px = 3.0 × (altura_px / 220)`, arredondado para 0,1. Todo asset de personagem declara sua altura e deriva os pesos.

### 2.2 Regras de traço
- Contorno **fechado**: nenhuma lacuna acidental. Lacunas intencionais (energia atravessando) são declaradas.
- Cantos externos arredondados em raio `0,6 × peso`; pontas de arma podem ser agudas.
- Linhas internas **não** tocam o contorno externo, exceto quando representam uma divisão real de peça.
- Proibido: linha tremida, linha dupla, contorno com alpha parcial, contorno borrado.
- O contorno é gerado por dilatação da máscara de alpha (não por `stroke` de polígono), garantindo espessura uniforme em curvas.

### 2.3 Contorno por categoria

| Categoria | Contorno externo | Observação |
|---|---|---|
| Personagem / equipamento / prop interativo | 3,0 px (escala 220) | Fechado, preto. |
| Pet | 2,4 px | Um pouco mais leve para não competir. |
| Inimigo comum | 3,0 px | Igual ao player. |
| Boss | 3,6–5,0 px | Escala com o tamanho; nunca “linha fina em corpo grande”. |
| VFX | **sem contorno** | Formas puras, aditivas. |
| Cenário (mid/far) | 0–0,8 px, cor mais escura da própria massa | Sem contorno preto. |
| Prop de primeiro plano | 1,2 px, cor escura | Leve, para separar do personagem. |
| UI | 2,0 px em molduras; 1,0 px em ícones | Moldura pode ter bisel. |

---

## 3. Cor

### 3.1 Arquitetura de rampa

Todo material usa **3 tons** derivados de uma cor-base `B` (HSL):

| Tom | Fórmula | Uso |
|---|---|---|
| **Base** `B` | cor canônica | 60–70% da área |
| **Sombra** `S` | `L × 0,72`, `S × 1,05`, matiz −4° (para o roxo/azul) | 25–35%, sempre no lado oposto à luz |
| **Brilho** `H` | `L + 0,22·(1−L)`, `S × 0,95`, matiz +3° | 5–10%, só em borda superior ou metal |
| **Profundidade** `D` (opcional) | `L × 0,48` | Só em cavities (axila, sob o queixo, dentro de capa) |

Regras:
- A sombra é **uma forma só**, recortada, com borda dura. Não usar blur.
- O brilho é **uma faixa ou um losango**, nunca um degradê.
- Não usar preto puro para sombrear cor; usar a rampa.
- Não usar branco puro para iluminar tecido; reservar branco puro para metal e energia.

### 3.2 Limite de cores
- Design de personagem/armadura: **≤ 8 cores** (fora contorno) — 2–3 materiais × 3 tons, reaproveitando tons.
- Arma: **≤ 5 cores**.
- Ícone: **≤ 6 cores**.
- Cenário: **≤ 12 cores** por camada.
- VFX: **≤ 4 cores** + alpha.

### 3.3 Paleta-mestra do projeto

As cores abaixo são **âncoras canônicas**; as rampas são derivadas pela fórmula §3.1. O arquivo completo e legível por máquina está em `standards/palette_master.json`.

#### Personagens

| Personagem / forma | Base | Sombra | Brilho | Secundária | Detalhe |
|---|---|---|---|---|---|
| Goku — gi | `#F08A2E` | `#C25E16` | `#FFB65C` | azul `#2F4FA8` | faixa `#E8D9B8` |
| Goku — pele | `#F6C9A0` | `#D79A72` | `#FFE1C4` | — | — |
| Goku — cabelo base | `#17121C` | `#0B0810` | `#3A3244` | — | — |
| Vegeta — armadura | `#EDEDEA` | `#B9BCC4` | `#FFFFFF` | azul `#243A7A` | ombreira `#D9A441` |
| Piccolo — pele | `#4E9B4A` | `#2F6B32` | `#7FC177` | roxo `#5B2E7A` | branco `#EDEAE1` |
| Frieza — final | `#F2F3F5` | `#C3C7CE` | `#FFFFFF` | roxo `#6C3FA0` | olho `#C81E2E` |
| Cell — perfect | `#3E8C3A` | `#245C25` | `#6DBB5E` | preto `#141414` | roxo `#6C3FA0` |
| Majin Buu | `#F09AD0` | `#C46AA6` | `#FFC7E8` | branco `#F4EFE6` | ouro `#D9A441` |
| Kuririn | `#F6C9A0` | `#D79A72` | `#FFE1C4` | laranja `#E57A2A` | — |
| Bulma (DB) | `#F6C9A0` | `#D79A72` | `#FFE1C4` | cabelo `#2E6FA8` | roupa `#E9E4D8` |
| Gohan — gi | `#7B3FA0` | `#54266F` | `#A566C6` | vermelho `#C0392B` | — |
| Trunks — jaqueta | `#2E3A4E` | `#1B2433` | `#4D5F7A` | cabelo `#8FB8D8` | — |
| Beerus | `#6C4A9A` | `#4A2F6E` | `#9268C4` | ouro `#D9A441` | olho `#F2D34A` |

#### Transformações (cabelo + aura)

| Forma | Cabelo base | Sombra | Brilho | Aura núcleo | Aura externa |
|---|---|---|---|---|---|
| Base | `#17121C` | `#0B0810` | `#3A3244` | — | — |
| Super Saiyan 1 | `#F7D24A` | `#C79A1E` | `#FFF0A8` | `#FFFBE0` | `#FFD84D` |
| Super Saiyan 2 | `#FFDF5C` | `#D1A321` | `#FFF6C4` | `#FFFDF0` | `#FFE066` |
| Super Saiyan 3 | `#FFE06A` | `#C99C1C` | `#FFF9D6` | `#FFFDF0` | `#FFE066` |
| Super Saiyan God | `#D94F6E` | `#A32E4C` | `#F58FA6` | `#FFD9E2` | `#E8405F` |
| Super Saiyan Blue | `#4FC3F7` | `#1E79B8` | `#B9ECFF` | `#E8FBFF` | `#35B8FF` |
| SSB Evolution | `#2E8FE0` | `#145C9B` | `#8FD3FF` | `#E0F6FF` | `#1E78FF` |
| Ultra Instinct Sign | `#2B2F3A` | `#151823` | `#565E70` | `#DCE8FF` | `#8FB8FF` |
| Ultra Instinct | `#D8DEE8` | `#98A2B4` | `#FFFFFF` | `#FFFFFF` | `#C9E4FF` |
| Super Saiyan Rosé | `#F08CB4` | `#B84E7C` | `#FFC3D8` | `#FFE8F0` | `#FF6FA5` |
| Golden Frieza | `#F2C14E` | `#B98A1E` | `#FFF0A8` | `#FFF4C2` | `#FFB92E` |
| Beast | `#E8EDF5` | `#A9B6CC` | `#FFFFFF` | `#FFFFFF` | `#7FD4FF` |

#### Elementos de energia

| Elemento | Núcleo | Meio | Borda | Blend |
|---|---|---|---|---|
| Ki padrão | `#FFFFFF` | `#FFD84D` | `#FF9A1E` | Add |
| Ki azul | `#FFFFFF` | `#5CC8FF` | `#1E78FF` | Add |
| Ki divino | `#FFFFFF` | `#C9A6FF` | `#8E5BD9` | Add |
| Fogo | `#FFF3C4` | `#FFB020` | `#E03A12` | Add |
| Gelo | `#FFFFFF` | `#A8E4FF` | `#3A9FD8` | Add |
| Escuridão | `#3A1B4A` | `#6C2E8A` | `#B44BE0` | Normal/Add |
| Sagrado | `#FFFFFF` | `#FFF2B8` | `#F2C14E` | Add |
| Elétrico | `#FFFFFF` | `#B9ECFF` | `#2E8FE0` | Add |

#### UI e cenário

| Uso | Cor |
|---|---|
| Fundo de painel | `#171A22` a 88% |
| Painel | `#232734` |
| Painel claro / hover | `#2E3446` |
| Moldura ouro | `#D9A441` · brilho `#F2CF7A` · sombra `#8A5E17` |
| Texto principal | `#F2E9D8` |
| Texto secundário | `#A9A28C` |
| HP | `#D7382F` → claro `#FF6A5E` |
| Ki / MP | `#2F80D8` → claro `#6FB6FF` |
| XP | `#8E5BD9` |
| Cura | `#3FBF6A` |
| Perigo / bloqueado | `#C0392B` |

---

## 4. Luz e sombreamento

### 4.1 Direção
- Luz principal: **cima + frente** (azimute 315°, elevação 55°).
- Consequência: toda forma recebe luz na **borda superior e frontal** e sombra na **borda inferior e traseira**.
- Não existe segunda fonte de luz, exceto:
  - **Rim light** de aura (cor do elemento) em transformações.
  - **Bounce** fraco do chão em cenas específicas (documentado no asset).

### 4.2 Receita por material

| Material | Base | Sombra | Brilho | Extra |
|---|---|---|---|---|
| **Pele** | cor canônica | 1 forma no lado inferior/traseiro do membro | 1 traço curto no topo da maçã do rosto / ombro | sem especular |
| **Tecido** | cor do tecido | 2–3 dobras em cunha (3–6 px de largura) | 1 aresta iluminada na dobra convexa | costura tracejada 1 px se peça de armadura |
| **Metal** | cor metálica | 1 sombra ampla + 1 sombra de cavidade | **2 brilhos**: um branco puro, um tingido | rim light de 1 px na borda oposta |
| **Couro** | marrom/cor | 1 sombra + vinco escuro | brilho curto e estreito | rebites/pontos de costura |
| **Ouro** | `#D9A441` | `#8A5E17` | `#FFE9A8` + branco | sempre com contorno interno |
| **Cabelo** | cor canônica | 1 faixa de sombra na raiz e no lado de baixo | 1 faixa de brilho em “banana” no topo | mechas agrupadas em 3–5 massas |
| **Energia** | 3 camadas | — | núcleo branco | sem contorno; blend aditivo |
| **Pelagem** | cor | manchas de sombra | faixa de brilho dorsal | sem fios individuais |

### 4.3 Membros traseiros
- Braço/perna **traseiros** recebem multiplicação de **0,82** na luminosidade e contorno **1,2× mais fino**.
- Opcional (estilo “silhueta”): membro traseiro a **0,55** para leitura em poses extremas. Só quando o clipe exigir.
- Regra de ouro: o membro frontal nunca é mais escuro que o traseiro.

### 4.4 Sombras projetadas
- Sombra no chão: elipse, `rgba(0,0,0,0.34)`, 92×22 px para adulto, centrada no root, não gira com o personagem (acompanha a escala do root).
- Em salto: elipse encolhe para 60% e clareia para 0,18.
- Sombras de contato entre personagem e props: opcional, 1 por cena, nunca por peça.

---

## 5. Proporções

### 5.1 Régua canônica

- **1 unidade = 1 px** na escala 1×.
- **Adulto heroico = 220 px**.
- Unidade de proporção = **altura da cabeça (crânio + queixo) = 36 px** → **6,1 cabeças**.
- Todos os rigs derivam dessa régua; variações mudam a *silhueta*, não a unidade.

### 5.2 Corpo heroico masculino A (rig `humanoid_male_a`)

| Segmento | Medida (px) | Acumulado do chão |
|---|---|---|
| Pé (altura do tornozelo ao chão) | 14 | 0–14 |
| Canela (tornozelo→joelho) | 44 | 14–58 |
| Coxa (joelho→quadril) | 46 | 58–104 |
| Pelve | 16 | 104–120 |
| Tronco (pelve→ombro) | 58 | 120–178 |
| Pescoço | 6 | 178–184 |
| Cabeça | 36 | 184–220 |
| **Total** | **220** | |

| Largura / comprimento | Medida |
|---|---|
| Ombro a ombro (externo) | 58 |
| Peito (largura) | 52 |
| Cintura | 34 |
| Quadril | 38 |
| Cabeça (largura) | 30 |
| Braço superior | 38 |
| Antebraço | 34 |
| Mão (comprimento) | 16 |
| Pé (comprimento) | 30 |
| Pescoço (largura) | 14 |

Ângulos de repouso (A-pose): braço 22° afastado do tronco; antebraço 8°; pernas 3° abertas; pés paralelos, ponta para +X (frente).

### 5.3 Variações de rig

| Rig | Cabeças | Altura | Silhueta |
|---|---|---|---|
| `humanoid_male_a` | 6,1 | 220 | Ombros 58, cintura 34 |
| `humanoid_female_a` | 6,2 | 218 | Ombros 50, cintura 28, quadril 42, peito sutil |
| `humanoid_muscular_b` | 6,4 | 236 | Ombros 68, peito 64, braço 42, perna 48 |
| `humanoid_child_a` | 4,6 | 158 | Cabeça 34, membros curtos, mãos grandes |
| `saiyan_male_a` | 6,1 | 220 | Igual ao male_a + cauda opcional |
| `saiyan_female_a` | 6,2 | 218 | Igual ao female_a + cauda opcional |
| `namekian_a` | 6,3 | 226 | Antenas, 4 dedos, orelhas pontudas, ombros 54 |
| `majin_a` | 5,8 | 210 | Volumes arredondados, sem pescoço aparente, tentáculo |
| `android_a` | 6,2 | 222 | Articulações segmentadas, placas |
| `frieza_race_a` | 5,8 | 206 | Muito esguio, membros finos, cabeça alongada |
| `creature_small_a` | 3,0 | 108 | Quadrúpede/bípede compacto |
| `quadruped_a` | — | 120 (altura) | 4 patas, cauda segmentada |
| `boss_giant_a` | 6,0 | 330–520 | Escala própria, mesmo esqueleto-base adaptado |

### 5.4 Regras de proporção
- Cabeça nunca menor que 1/7 da altura; mãos nunca menores que 0,7 cabeça.
- Pés sempre legíveis: comprimento ≥ 0,8 cabeça em adulto.
- Braço total (ombro→ponta do dedo) ≈ 0,42 da altura.
- Perna total (quadril→chão) ≈ 0,47 da altura.
- Em transformações musculares (SSJ, Ultra Ego, Broly), aumentar ombros e braços em 8–12%, **nunca** a cabeça.
- Em formas infantis, cabeça = 22% da altura.

---

## 6. Rosto e expressão

### 6.1 Estrutura
- Visão **3/4 frontal**, olhar para +X (direita). O pack é espelhado para a esquerda em runtime.
- Crânio: massa arredondada; queixo pequeno e anguloso; bochecha com 1 plano de sombra.
- Olho: esclera branca `#F7F2EA`, íris/pupila escura, **brilho especular de 1 px** no canto superior.
- Sobrancelha: massa espessa, 2 px, cor do cabelo, angulada.
- Nariz: 1 traço curto ou 1 cunha, nunca narina detalhada.
- Boca: 1 traço de 1,6 px; variação por expressão.

### 6.2 Biblioteca facial mínima (obrigatória em todo personagem jogável)

| Face | Uso | Olho | Sobrancelha | Boca |
|---|---|---|---|---|
| `neutral` | Idle | aberto, pupila centrada | reta | linha neutra |
| `combat` | Idle de combate | levemente estreitado | inclinada 8° | linha firme |
| `angry` | Ataque | estreitado | inclinada 18° | aberta, dentes |
| `strain` | Esforço/cast | fechado 40% | inclinada 12° | aberta curta |
| `hurt` | Dano | fechado 60% | para cima no centro | aberta |
| `crit` | Dano crítico | fechado, “X” | para cima | aberta grande |
| `shock` | Miss/erro | muito aberto | alta | “o” |
| `smirk` | Vitória/taunt | meio fechado | arqueada | canto subido |
| `dead` | Morte | “X” | caída | linha |
| `blink` | Piscar | fechado | normal | normal |

- Piscar: 3 frames (fechar 1, fechar 1, abrir 1) a 24 fps → 125 ms. Intervalo aleatório de 2,4–5,0 s.
- Faces são **attachments** da cabeça; trocar face não muda o resto do rig.

---

## 7. Cabelo

- Modelar em **3–5 massas** principais; espinhos individuais ≤ 12 em qualquer penteado.
- Cada massa tem contorno próprio quando se sobrepõe a outra.
- Cabelo frontal (sobre a testa) e traseiro são **peças separadas** (camadas 2 e 16).
- Brilho em “banana” no topo da massa, 1 por massa.
- Super Saiyan: adicionar **+6 a +10 massas** de espinhos para cima, comprimento +18%, volume +25%; nunca mudar o crânio.
- SSJ3: cabelo desce até a cintura e perde o contorno de sobrancelha.
- Ultra Instinct: massa com bordas mais suaves e brilho em prata.
- Cabelo deve ter **physics**: cadeia de 2–3 ossos (`hair_back_01..02`) com spring. Ver doc 04 §8.

---

## 8. Mãos, pés e empunhadura

- Mão fechada: **bloco + polegar**, 3 sulcos no máximo. Não desenhar 5 dedos individualmente em escala de jogo.
- Mão aberta (cast): 4 dedos como massas fundidas + polegar separado.
- Grip de arma: a mão tem **2 poses** — `fist` (fechada) e `open` (aberta). Armas declaram qual usam.
- O ponto de empunhadura (`grip`) fica no centro da mão fechada, nunca na ponta.
- Pé: bota ou pé descalço, com **sola** de 2–3 px e bico definido. Vista lateral/3-4.
- Dedos do pé: nunca individualizados, exceto em personagens descalços (2 sulcos).

---

## 9. Silhueta

Teste obrigatório antes de aprovar qualquer design:

1. Preencher a silhueta com preto puro.
2. Reduzir para **48 px de altura**.
3. Ainda é possível dizer quem é e o que empunha? Se não, refazer.
4. Repetir a 96 px e 220 px.

Regras:
- A arma deve criar uma **diagonal dominante** distinta da linha do corpo.
- Cabelo e ombreiras definem o topo da silhueta; botas definem a base.
- Evitar “ruído” de pontas pequenas (< 3 px) que desaparecem em escala.
- Cada personagem deve ter **1 exagero assinatura** (cabelo, capa, arma, ombreira, cauda).

---

## 10. Equipamentos dentro da estética

- Armadura **substitui** a peça do corpo (não veste por cima). Peças: tronco, ombreiras, braços, pernas, botas, cinto.
- Ombreira é a peça de leitura mais importante: mínimo 1,3× a largura do ombro.
- Armas: comprimento 0,9–1,4× a altura do personagem (espadas), 1,5× (cajados).
- Capa: comprimento até 85% da altura; 2–3 ossos; nunca sólida demais (deve deixar ver as pernas).
- Helms: `hat` (sobre o cabelo) ou `morph` (substitui cabeça). Nunca os dois no mesmo asset.
- Metais sempre com 2 brilhos; tecidos nunca com brilho branco puro.
- Todo equipamento declara `slot`, `layer`, `anchor` e `rig_compat`.

---

## 11. VFX

- **Sem contorno.** Formas puras com 3 camadas (núcleo branco, meio saturado, borda com alpha 40–60%).
- Blend padrão: **Add** para energia/luz, **Normal** para fumaça/detritos, **Multiply** para sombras.
- Timing agressivo: ataque com 2–4 frames de *smear*; impacto com 1 frame de flash branco.
- Tamanho: nunca cobrir a cabeça do personagem por mais de 3 frames (exceto ultimate/boss).
- Paleta do elemento obrigatória (doc 07).
- Partículas: círculos e losangos; nunca textura fotorrealista.

---

## 12. Cenários

- Cenário **não compete** com personagem: dessaturar 15%, reduzir contraste em 20%, sem contorno preto grosso.
- Camadas: céu → horizonte → mid → estruturas → decoração → chão → props → foreground → occluders.
- Chão caminhável: textura legível, mas sem detalhe de 1 px; linhas de perspectiva coerentes com 2.5D.
- Profundidade por valor: fundo claro/azulado, frente escura/saturada.
- Props interativos têm contorno de 1,2 px para se destacarem do cenário.
- Nenhum texto embutido em mapa (exceto placas decorativas declaradas).

---

## 13. UI

- Painéis escuros (`#171A22` a 88%) com moldura ouro (`#D9A441`) de 2 px e bisel interno de 1 px.
- Cantos com ornamento mínimo (1 losango ou 1 parafuso), nunca arabesco denso.
- Barras: HP vermelho, Ki azul, XP roxo, com brilho superior de 1 px e sombra inferior.
- Ícones: fundo transparente, forma central ocupando 72% do quadro, contorno 1 px escuro, brilho duro no topo.
- Tipografia: display serifada/fantasia para títulos (substituível), sans legível para números. Nunca texto em imagem que o jogo possa localizar.
- Estados obrigatórios: normal, hover, pressed, selected, disabled, cooldown, locked, new.
- 9-slice com insets documentados; nada de esticar ornamento.

---

## 14. Do / Don't

| ✅ Faça | ❌ Não faça |
|---|---|
| 1 sombra chapada, recortada | degradê suave em tecido |
| contorno 3,0 px constante | contorno fino no corpo e grosso na arma |
| membro traseiro 0,82 | membro traseiro mais claro que o frontal |
| 8 cores no máximo | 20 cores “porque o personagem tem detalhe” |
| silhueta testada a 48 px | design que só funciona em 4K |
| arma 1,0–1,4× a altura | arma 3× a altura sem ser boss |
| VFX sem contorno | explosão com lineart preto |
| cenário dessaturado | fundo tão saturado quanto o herói |
| piscar a cada 2,4–5 s | olhos parados por 30 s |
| peso e antecipação | movimento linear e flutuante |

---

## 15. Checklist visual (aprovar/reprovar)

- [ ] Contorno fechado, 3,0 px (±0,1) na escala 220.
- [ ] Luz coerente com cima/frente em todas as peças.
- [ ] 1 sombra dura + 1 brilho por material.
- [ ] ≤ 8 cores (+ contorno).
- [ ] Proporções dentro de ±2% da prancha do rig.
- [ ] Silhueta legível a 48 px.
- [ ] Membro traseiro 0,82 e mais fino.
- [ ] Sem gradiente, sem blur, sem textura fotorrealista.
- [ ] Sem detalhe inútil abaixo de 2 px.
- [ ] Face legível e expressiva a 100%.
- [ ] Peça encaixa no vizinho sem costura (overlap 2–3 px).
- [ ] Paleta corresponde ao `palette_master.json`.
- [ ] Estilo indistinguível dos assets já aprovados.

---

## 16. Referências internas
`standards/palette_master.json` · `standards/canvas_and_scale.json` · `standards/layer_order.json` · `docs/03_ANATOMY_RIG_PAPERDOLL.md` · `docs/19_RESEARCH_AQW_TEARDOWN.md`
