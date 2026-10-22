# 03 — ANATOMIA, RIG E PAPER-DOLL
**Projeto AURA · v1.0.0**
Define o esqueleto, as juntas, os pivôs, os slots, as máscaras e as regras de montagem. É a base de tudo que se move no pack.

---

## 1. O modelo

O personagem **não é uma imagem**. É uma pilha ordenada de peças presas a ossos.

```
IMAGE (512²)
└── ACTOR (root no chão, 256,448 em image)
    ├── sombra
    ├── esqueleto (28–40 ossos)
    ├── slots (29 camadas) → cada slot referencia 1 attachment (PNG)
    └── máscaras de recoloração
```

- Cada **osso** tem posição de repouso, comprimento, ângulo e pai.
- Cada **slot** aponta para um osso, uma camada e um attachment.
- Cada **attachment** é um PNG com pivô declarado e, opcionalmente, máscaras.
- Trocar equipamento = trocar attachments em slots, sem tocar no esqueleto.
- Trocar transformação = trocar cabelo/olhos/aura, sem tocar no esqueleto (salvo mudança anatômica).

---

## 2. Hierarquia canônica (humanoide)

```
root
└── pelvis
    ├── spine
    │   └── chest
    │       ├── neck
    │       │   └── head
    │       │       ├── hair_front      (slot 115)
    │       │       ├── face            (slot 111)
    │       │       └── helm            (slot 116)
    │       ├── clavicle_f
    │       │   └── upper_arm_f
    │       │       └── forearm_f
    │       │           └── hand_f
    │       │               └── weapon_f
    │       ├── clavicle_b
    │       │   └── upper_arm_b
    │       │       └── forearm_b
    │       │           └── hand_b
    │       │               └── weapon_b
    │       ├── shoulders           (slot 120, preso ao chest)
    │       ├── cape_01             (slot 30, preso ao chest)
    │       │   └── cape_02
    │       │       └── cape_03
    │       ├── hair_back_01        (slot 40, preso ao head, com offset)
    │       │   └── hair_back_02
    │       └── pet_anchor          (slot 10)
    ├── thigh_f → shin_f → foot_f → toe_f
    └── thigh_b → shin_b → foot_b → toe_b
```

> `_f` = **front/near** (mais próximo da câmera). `_b` = **back/far**. Não são “esquerda/direita”: com o personagem virado para +X, são o lado visível e o lado oculto.

---

## 3. Juntas e medidas de repouso

Coordenadas em **world px** (y para cima, chão = 0), personagem adulto de 220 px. Todas as medidas são normativas para o rig `humanoid_male_a`.

| Junta | X | Y | Pai | Comprimento | Limite de rotação |
|---|---|---|---|---|---|
| `root` | 0 | 0 | — | — | translação 2D livre |
| `pelvis` | 0 | 104 | root | 16 | −12°..12° |
| `spine` | 0 | 120 | pelvis | 32 | −18°..24° |
| `chest` | 0 | 152 | spine | 26 | −12°..16° |
| `neck` | 0 | 178 | chest | 6 | −30°..30° |
| `head` | 0 | 184 | neck | 36 | −28°..28° |
| `clavicle_f` | 6 | 174 | chest | 16 | −20°..28° |
| `upper_arm_f` | 22 | 176 | clavicle_f | 38 | −40°..200° |
| `forearm_f` | 36 | 141 | upper_arm_f | 34 | 0°..150° (só flexão) |
| `hand_f` | 50 | 112 | forearm_f | 16 | −35°..45° |
| `weapon_f` | 58 | 100 | hand_f | — | attach rígido + sway opcional |
| `clavicle_b` | −4 | 174 | chest | 16 | −20°..28° |
| `upper_arm_b` | 12 | 176 | clavicle_b | 38 | −40°..200° |
| `forearm_b` | 26 | 141 | upper_arm_b | 34 | 0°..150° |
| `hand_b` | 40 | 112 | forearm_b | 16 | −35°..45° |
| `thigh_f` | 9 | 104 | pelvis | 46 | −45°..115° |
| `shin_f` | 11 | 58 | thigh_f | 44 | 0°..155° |
| `foot_f` | 12 | 14 | shin_f | 14 | −40°..45° |
| `toe_f` | 26 | 6 | foot_f | 10 | −10°..35° |
| `thigh_b` | −9 | 104 | pelvis | 46 | −45°..115° |
| `shin_b` | −11 | 58 | thigh_b | 44 | 0°..155° |
| `foot_b` | −12 | 14 | shin_b | 14 | −40°..45° |
| `toe_b` | −26 | 6 | foot_b | 10 | −10°..35° |
| `cape_01` | 0 | 176 | chest | 44 | −70°..90° |
| `cape_02` | 0 | 132 | cape_01 | 44 | −80°..100° |
| `cape_03` | 0 | 88 | cape_02 | 44 | −80°..100° |
| `hair_back_01` | 0 | 212 | head | 20 | −60°..60° |
| `hair_back_02` | 0 | 192 | hair_back_01 | 20 | −70°..70° |

**Convenção de ângulo:** `0°` = direção de repouso do osso (para membros superiores, “para baixo”; para tronco, “para cima”). Positivo = horário na tela.

> Os valores de X de ombro/quadril codificam a **vista 3/4**: o lado `_f` fica 4–13 px à frente do eixo central, o `_b` atrás. Isso é o que faz o personagem “ler” como AQW e não como um boneco plano.

---

## 4. Pivôs das peças

O pivô de um attachment **coincide com a junta** do osso que o anima. A peça é desenhada de forma que a rotação em torno desse ponto não abra fenda.

| Peça | Pivô | Regra de forma |
|---|---|---|
| `head` | `neck` (0,184) | base do pescoço; crânio acima |
| `torso` | `pelvis` (0,120) | base da caixa torácica; cobre a pelve em 3 px |
| `pelvis` | `pelvis` (0,104) | centro de gravidade; topo coberto pelo torso |
| `upper_arm` | `shoulder` | topo arredondado com raio = largura/2 + 1,5 px |
| `forearm` | `elbow` | topo arredondado; sobrepõe o braço em 2–3 px |
| `hand` | `wrist` | pulso dentro do antebraço em 2 px |
| `thigh` | `hip` | topo arredondado; cobre a pelve em 4 px |
| `shin` | `knee` | topo arredondado; sobrepõe a coxa em 3 px |
| `foot` | `ankle` | calcanhar atrás do tornozelo em 4 px |
| `cape_01` | `cape_base` (0,176) | topo largo preso ao dorso |
| `hair_back` | `hair_base` (0,212) | raiz no topo do crânio |
| `weapon` | `grip` | cabo alinhado ao eixo do osso `weapon_f` |

### 4.1 Overlap de junta (obrigatório)
- Toda peça distal **entra 2–3 px** dentro da proximal.
- O topo da peça distal tem **tampa arredondada** (semicírculo) para cobrir o vão em qualquer ângulo.
- Em flexão máxima (cotovelo 150°, joelho 155°), a soma de overlap deve impedir qualquer pixel de fundo entre as peças. Teste automatizado em doc 05 §6.

---

## 5. Slots e attachments

`standards/layer_order.json` define a ordem; `rig.schema.json` define a estrutura.

| Slot | Camada | Osso | Tipo | Obrigatório |
|---|---|---|---|---|
| `shadow` | 0 | `root` | procedural | sim |
| `pet` | 10 | `pet_anchor` | externo | não |
| `aura_back` | 20 | `root` | VFX | não |
| `cape` | 30 | `cape_01` | equip | não |
| `wings` | 31 | `chest` | equip | não |
| `hair_back` | 40 | `hair_back_01` | corpo | sim* |
| `weapon_back` | 50 | `hand_b` | equip | não |
| `thigh_b` | 70 | `thigh_b` | corpo | sim |
| `shin_b` | 71 | `shin_b` | corpo | sim |
| `foot_b` | 72 | `foot_b` | corpo | sim |
| `pelvis` | 80 | `pelvis` | corpo | sim |
| `torso` | 90 | `chest` | corpo | sim |
| `upper_arm_b` | 92 | `upper_arm_b` | corpo | sim |
| `forearm_b` | 93 | `forearm_b` | corpo | sim |
| `hand_b` | 94 | `hand_b` | corpo | sim |
| `thigh_f` | 100 | `thigh_f` | corpo | sim |
| `shin_f` | 101 | `shin_f` | corpo | sim |
| `foot_f` | 102 | `foot_f` | corpo | sim |
| `head` | 110 | `head` | corpo | sim |
| `face` | 111 | `head` | corpo | sim |
| `hair_front` | 115 | `head` | corpo | sim* |
| `helm` | 116 | `head` | equip | não |
| `shoulders` | 120 | `chest` | equip | não |
| `upper_arm_f` | 130 | `upper_arm_f` | corpo | sim |
| `forearm_f` | 131 | `forearm_f` | corpo | sim |
| `hand_f` | 132 | `hand_f` | corpo | sim |
| `weapon_f` | 140 | `weapon_f` | equip | não |
| `attack_fx` | 150 | `weapon_f` | VFX | não |
| `aura_front` | 160 | `root` | VFX | não |

\* Obrigatório em personagens com cabelo; carecas usam attachment vazio declarado.

### 5.1 Substituição por equipamento
- Armadura **substitui** `torso`, `pelvis`, `upper_arm_*`, `forearm_*`, `thigh_*`, `shin_*`, `foot_*` conforme cobertura declarada em `covers[]`.
- Um set pode cobrir só parte (ex.: peitoral cobre `torso` e `shoulders`, não as pernas).
- O slot `face` nunca é substituído por armadura; helms `morph` substituem `head`+`face`+`hair_front`.

---

## 6. Rig ID e famílias

| Rig ID | Base | Altura | Ossos | Notas |
|---|---|---|---|---|
| `humanoid_male_a` | — | 220 | 29 | referência |
| `humanoid_female_a` | male_a | 218 | 29 | larguras diferentes, mesmos pivôs Y |
| `humanoid_muscular_b` | male_a | 236 | 29 | escalas 1,07 em tronco/braço |
| `humanoid_child_a` | male_a | 158 | 29 | escala 0,72; cabeça 34 px (não escala uniforme) |
| `saiyan_male_a` | male_a | 220 | 32 | + `tail_01..03` |
| `saiyan_female_a` | female_a | 218 | 32 | + cauda |
| `namekian_a` | male_a | 226 | 31 | + `antenna_01..02`; 4 dedos |
| `majin_a` | male_a | 210 | 30 | + `head_tentacle`; sem pescoço visível |
| `android_a` | male_a | 222 | 32 | placas, juntas segmentadas |
| `frieza_race_a` | male_a | 206 | 29 | membros finos, cabeça alongada |
| `creature_small_a` | — | 108 | 10–14 | pet/verme |
| `quadruped_a` | — | 120 | 16–22 | 4 patas + cauda |
| `boss_giant_a` | male_a | 330–520 | 40–52 | múltiplos segmentos de cauda/asa |

Regra: reutilizar rig sempre que a anatomia permitir. **Nunca** forçar Namekuseijin, Majin ou Oozaru no rig humanoide sem declarar as adaptações.

---

## 7. Máscaras de recoloração

Cada personagem/armadura exporta máscaras em `.../masks/`:

| Máscara | Conteúdo | Recolorível |
|---|---|---|
| `skin` | toda a pele | cor de pele, tom |
| `hair` | cabelo | cor de cabelo |
| `eyes` | íris/pupila | cor de olho (não a esclera) |
| `cloth_primary` | tecido principal | cor primária (CC1) |
| `cloth_secondary` | tecido secundário | cor secundária (CC2) |
| `metal` | metais | tom metálico |
| `trim` | detalhes/bordas | cor de detalhe |
| `energy` | partes energéticas | cor de energia |

- Formato: PNG **8-bit grayscale**, mesmo canvas da peça, bordas duras.
- Aplicação: LUT de paleta → recolor **somente** dentro da máscara, preservando a rampa de 3 tons.
- Máscara de cabelo em transformação SSJ é obrigatória (recolor por LUT é aceitável **apenas** para variações de cor; forma nova exige peça nova).
- Nunca recolorir personagem canônico de forma que descaracterize (Goku não fica com gi azul por padrão).

---

## 8. Sockets

| Socket | Osso | Offset (bone-local px) | Uso |
|---|---|---|---|
| `hand_f` | `hand_f` | (8, 0) | arma, projétil de mão |
| `hand_b` | `hand_b` | (8, 0) | arma secundária |
| `weapon_tip` | `weapon_f` | (comprimento, 0) | trail, VFX de ponta |
| `chest` | `chest` | (0, 10) | aura, beam |
| `mouth` | `head` | (10, 6) | ki blast curto |
| `forehead` | `head` | (8, 24) | beam especial |
| `back` | `chest` | (−12, 8) | capa, asas |
| `feet` | `foot_f` | (6, 0) | poeira, impacto |

Sockets são **dados**, não pixels: o VFX se posiciona em runtime.

---

## 9. Montagem e teste

### 9.1 Receita de montagem
1. Colocar `root` em (256, 448) image.
2. Aplicar a pose de repouso do rig.
3. Desenhar slots em ordem crescente de `z`.
4. Desenhar sombra primeiro, com alpha 0,34.
5. Aplicar `0,82` de luminosidade nos slots `_b`.
6. Aplicar contorno de 3,0 px apenas nas peças; nunca no conjunto final (evita linha dupla).

### 9.2 Teste de montagem obrigatório
- **T-pose/A-pose**: peças encaixam sem fenda visível em 100% e 200%.
- **Flexão máxima**: cotovelo 150°, joelho 155°, ombro 200° — zero fenda.
- **Torção**: spine +24°, head −28° — zero fenda no pescoço/cintura.
- **Troca de equipamento**: 3 sets diferentes montados na mesma base.
- **Silhueta**: preenchimento preto a 48 px.

### 9.3 Erros que reprovam
- Peça “flutuando” por pivô errado.
- Fenda de fundo em junta.
- Peça frontal mais escura que a traseira.
- Ordem de camada violada (ex.: cabelo atrás do rosto).
- Escala do membro mudando entre poses.
- Contorno dobrado no meio da peça.

---

## 10. Anatomia por família (deltas)

| Família | Delta em relação ao humanoide |
|---|---|
| **Saiyajin** | cauda `tail_01..03` presa ao `pelvis`, comprimento 96 px; controlada por spring |
| **Namekuseijin** | antenas `antenna_01/02` no `head`; orelhas pontiagudas; 4 dedos; ombros 54 px |
| **Majin** | sem `neck` visível; cabeça 42 px; tentáculo `head_tentacle`; tronco mais largo na base |
| **Androide** | `chest` com placa; juntas com anel metálico; antebraço 36 px |
| **Raça de Frieza** | cabeça 38 px alongada; membros 0,92× diâmetro; cauda opcional |
| **Oozaru** | rig próprio `quadruped_a` escalado 3,2×; cauda `tail_01..05`; mãos 2× |
| **Boss gigante** | rig `boss_giant_a`, cadeia de cauda 4–6 ossos, asas 3 ossos cada |

---

## 11. Estrutura do rig em JSON (resumo)

```json
{
  "rig_id": "humanoid_male_a",
  "version": "1.0.0",
  "height_px": 220,
  "units": "px",
  "coordinate_system": "world_y_up",
  "bones": [
    {"name": "root", "parent": null, "pos": [0, 0], "len": 0},
    {"name": "pelvis", "parent": "root", "pos": [0, 104], "len": 16},
    {"name": "spine", "parent": "pelvis", "pos": [0, 120], "len": 32},
    {"name": "chest", "parent": "spine", "pos": [0, 152], "len": 26}
  ],
  "slots": [
    {"name": "torso", "bone": "chest", "layer": 90, "attachment": "goku_gi_torso"},
    {"name": "head", "bone": "head", "layer": 110, "attachment": "goku_head"}
  ],
  "sockets": [
    {"name": "hand_f", "bone": "hand_f", "offset": [8, 0]}
  ]
}
```

Schema completo: `standards/rig.schema.json`.
Esqueleto de referência com todos os ossos: `standards/skeleton_humanoid.json`.
