# 17 — AI AGENT HANDBOOK
**Projeto AURA · v1.0.0**
Manual operacional para um agente de IA que vai **usar** ou **expandir** o pack. Se você só pode ler um documento, leia este e o `README.md`.

---

## 1. Ordem de leitura obrigatória

| # | Arquivo | Para quê |
|---|---|---|
| 1 | `README.md` | estado atual do pack |
| 2 | `docs/17_AI_AGENT_HANDBOOK.md` | como operar |
| 3 | `docs/01_VISUAL_BIBLE.md` | como a arte deve parecer |
| 4 | `docs/02_TECHNICAL_SPECIFICATION.md` | canvas, pivôs, camadas, arquivos |
| 5 | `docs/03_ANATOMY_RIG_PAPERDOLL.md` | esqueleto e slots |
| 6 | `docs/04_ANIMATION_STANDARD.md` + `05_FLUIDITY...` | movimento e aprovação |
| 7 | `standards/*.json` | verdade legível por máquina |
| 8 | `production/continuity_state.json` | onde o projeto parou |

Se `matrix_frozen` for `false`, **não** produza assets em escala: você está na fase de validação.

---

## 2. Modelo mental

```
ASSET = ID + arquivos + metadados + status
PERSONAGEM = rig + slots + attachments + clipes + máscaras
EQUIPAMENTO = peças que substituem slots (covers[])
ANIMAÇÃO = tracks de osso + eventos + duração
CENA = mapa + atores + UI + VFX
```

Tudo tem **uma fonte de verdade**:
- camadas → `standards/layer_order.json`
- escala → `standards/canvas_and_scale.json`
- cores → `standards/palette_master.json`
- tempos → `standards/clip_matrix.json`
- estrutura → `standards/*.schema.json`

Nunca invente um valor que já existe em `standards/`.

---

## 3. Árvore de decisão

| Necessidade | Onde está |
|---|---|
| Corpo jogável | `characters/base_bodies/<rig>/` |
| Goku e heróis | `characters/canonical_heroes/<nome>/<forma>/` |
| Vilões | `characters/canonical_villains/` |
| Transformação | `characters/transformations/<personagem>/<forma>/` |
| Armadura / arma / capa | `equipment/<tipo>/<set>/` |
| Inimigo | `enemies/<tier>/<nome>/` |
| Pet | `pets/<tipo>/<nome>/` |
| Skill / VFX | `skills/<categoria>/<nome>/` |
| Mapa | `environments/maps/<map_id>/` |
| Prop / tile | `environments/props/` · `environments/ground_tiles/` |
| HUD / painel / ícone | `ui/<sistema>/` |
| Preview aprovado | `exports/previews/<asset_id>/` |
| Metadados | `exports/metadata/<asset_id>.json` |

---

## 4. Garantias do pack (contrato)

Se o asset está `APPROVED`, você pode assumir:

1. PNG RGBA, alpha straight, sem halo.
2. Dimensões e pivô batem com o JSON.
3. `layer` existe em `layer_order.json`.
4. `rig_compat` aponta para rig existente.
5. Clipes têm `duration_frames`, `loop`, `events` e `fps_base`.
6. O frame `N` de um loop é igual ao frame `0` em pose.
7. Sockets existem no esqueleto.
8. Checksum confere.
9. Estilo conforme a Visual Bible.
10. Preview em `exports/previews/` corresponde ao arquivo.

Se algo disso falhar, o asset **não** é `APPROVED`. Não "conserte" no runtime.

---

## 5. Receitas

### 5.1 Adicionar um personagem novo
1. Escolha o rig em `characters/rigs/` (reuse antes de criar).
2. Copie a estrutura de `characters/canonical_heroes/goku/base/`.
3. Substitua as peças mantendo **pivôs e alturas**.
4. Ajuste paleta em `standards/palette_master.json` (adicione entrada, não sobrescreva).
5. Crie as 10 faces.
6. Reaproveite os clipes; só crie clipes novos se a anatomia exigir.
7. Rode `aura build` e `aura validate`.
8. Gere os GIFs e preencha a rubrica.
9. Registre em `asset_manifest.json` e no backlog.

### 5.2 Adicionar equipamento
1. Escolha `slot` e `covers[]`.
2. Modele as peças no pivô da junta correspondente.
3. Exporte máscaras.
4. Teste em 3 rigs e 4 poses.
5. Gere ícone.
6. Valide clipping.

### 5.3 Adicionar skill/VFX
1. Divida em cast/charge/projectile/beam/impact/explosion.
2. Use a paleta do elemento.
3. Animação em 24 fps, export 60.
4. Declare `blend`, `anchor`, `screen_coverage`.
5. Teste com 10 atores em tela.

### 5.4 Adicionar mapa
1. 8 camadas + tiles + props.
2. `map.json` com colisão, spawns, portais, oclusores.
3. Preview com ator de referência na linha de chão.
4. Teste de costura de tile 3×3.
5. Teste de legibilidade do personagem.

### 5.5 Adicionar tela de UI
1. 9-slice com insets.
2. 8 estados por componente.
3. Texto em chave, nunca em imagem.
4. Ícones derivados de assets existentes.
5. Tema em `ui_theme.json`.

---

## 6. Validação

```bash
python -m tools.cli build   <caminho-do-asset>
python -m tools.cli preview --asset <id> --clips idle,walk,attack_light_1
python -m tools.cli validate --all
python -m tools.cli pack
```

- `validate --all` deve retornar código 0.
- Toda animação passa pelas métricas de F1–F6 (doc 05 §6).
- Rubrica ≥ 24/30 e nenhum critério < 3.

---

## 7. Erros comuns (e como evitar)

| Erro | Correção |
|---|---|
| Desenhar personagem inteiro e cortar depois | modelar peças com pivô desde o início |
| Mudar a altura da cabeça "só nesse personagem" | usar o rig; variação só com novo rig declarado |
| Usar `linear` em membro | usar `smoothstep`/`ease_*` |
| Loop com salto | frame `N` = frame `0` |
| Cor fora da paleta | usar `palette_master.json` |
| Contorno de 2 px em corpo de 220 | 3,0 px |
| Personagem sobre fundo da mesma cor | checar contraste com palette do bioma |
| Texto dentro da imagem de UI | usar chave de localização |
| GIF com transparência "xadrez" | fundo sólido de revisão |
| Declarar aprovado sem preview | gerar e anexar |

---

## 8. Templates de prompt (uso restrito)

Imagem generativa **não** é usada para peças modulares. Permitida para concept e backdrop:

**Concept de personagem (referência apenas):**
> "Character concept sheet, 2D Flash cartoon style, cel shading, bold black outline, flat saturated colors, heroic proportions, front and 3/4 views, neutral pose, **{personagem}**, **{figurino}**, transparent background, no text, no logo."

**Backdrop de cenário:**
> "2D side-scrolling game background, painted, soft edges, no outlines, no characters, no text, **{bioma}**, **{hora do dia}**, muted contrast, wide composition, only the **{camada}** layer."

**Ícone (referência):**
> "Game ability icon, bold shape, 3 hard tones, high contrast, centered, transparent background, **{técnica}**, **{elemento}**, readable at 64 px, no text."

Depois do prompt, **sempre** aplicar o pós-processamento do doc 08 §8 e validar contra a Visual Bible.

---

## 9. Como construir uma cena de jogo com o pack

```
1. Escolha o mapa em environments/maps/ e carregue map.json.
2. Instancie o player (rig + atlas + animator).
3. Instancie 5–10 inimigos com spawn do mapa.
4. Instancie 2 NPCs com âncoras do mapa.
5. Monte a HUD com ui/hud/ + ui_theme.json.
6. Ligue os sistemas: input, state machine, combate, loot, quests.
7. Rode o debug overlay (ossos, hurtbox, sockets, eventos).
8. Valide 60 fps com 30 atores.
```

Checklist de cena:
- [ ] Depth sort por `foot_y`.
- [ ] Colisão e oclusão ativas.
- [ ] Portais levam a spawns válidos.
- [ ] HUD sem texto embutido.
- [ ] Eventos de animação ligados ao combate.
- [ ] Hitstop e shake funcionando.
- [ ] Acessibilidade (`reduce_motion`, `reduced_vfx`).

---

## 10. Como estender sem quebrar

- **Nunca** altere um arquivo `APPROVED` sem bump de versão.
- **Nunca** mude pivô, altura ou ordem de camada sem ADR.
- Adicione campos, não remova.
- Novos assets referenciam `matrix_version`.
- Mantenha o estilo: contorno, paleta, proporção, luz.
- Se precisar de exceção, registre em `docs/matrix/EXCEPTIONS.md`.

---

## 11. Quando parar

Pare e registre `BLOCKED` se:
- faltar ferramenta para cumprir um requisito;
- o rig não suportar a anatomia (ex.: Oozaru);
- a mudança exigir quebrar a Matriz;
- o resultado não passar na rubrica após 3 ciclos.

Nunca declare concluído o que não existe em disco.

---

## 12. Critério de sucesso do agente

Você teve sucesso quando:
1. Um humano abre o pack e monta um personagem sem perguntar nada.
2. Um dev integra o personagem em uma engine usando só os JSONs.
3. Um segundo agente gera um asset novo **compatível** seguindo os schemas.
4. O GIF de validação convence sem explicação.
