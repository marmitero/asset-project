# 07 — VFX STANDARD
**Projeto AURA · v1.0.0**
Norma de efeitos visuais: o que compõe uma skill, como ela é fatiada, como ela se mistura e como não esconder o combate.

---

## 1. Princípios

1. **VFX não tem contorno.** Forma pura, cor saturada, alpha real.
2. **Toda skill é componentizada.** Nunca uma imagem única com personagem + feixe + explosão.
3. **Blend aditivo é padrão** para energia; normal para fumaça/detritos; multiply para sombras.
4. **O efeito serve à leitura**: o jogador precisa ver o corpo, a arma e o alvo.
5. **Curto e forte** vence longo e detalhado: impacto dura 6–14 frames.
6. **Cor = elemento**. A paleta é fixa por elemento (doc 01 §3.3).

---

## 2. Anatomia de uma habilidade

```
skills/<skill_id>/
  icon.png
  cast/            (pose de preparação do personagem — referência, não VFX)
  charge/          (energia concentrando, loop)
  projectile/      (núcleo + cauda, se houver)
  beam/            (núcleo, segmento extensível, ponta)
  trail/           (rastro)
  impact/          (contato)
  explosion/       (expansão)
  particles/       (poeira, faíscas, detritos)
  aura/            (se persistente)
  metadata.json
  preview.gif
```

Cada pasta contém frames PNG numerados + `manifest.json` com `frame_count`, `fps`, `blend`, `anchor`, `loop`.

---

## 3. Categorias e templates de timing

| Categoria | Frames | FPS | Loop | Forma | Blend |
|---|---|---|---|---|---|
| **Slash / corte** | 5–8 | 24 | não | arco fino, 3 camadas | Add |
| **Impacto** | 4–6 | 24 | não | estrela irregular + anel | Add |
| **Explosão** | 10–16 | 24 | não | bola + anel + detritos | Add + Normal |
| **Projétil** | 4–6 loop + 3 impacto | 24 | loop | orbe com cauda | Add |
| **Feixe / beam** | 6 (start) + 4 loop + 6 (end) | 24 | loop no meio | núcleo + 2 bordas + ponta | Add |
| **Aura** | 16–24 | 24 | sim | 3 camadas orgânicas | Add |
| **Carga (charge)** | 12–20 | 24 | sim | partículas convergindo | Add |
| **Buff** | 12–18 | 24 | sim | símbolo + anel ascendente | Add |
| **Cura** | 16 | 24 | sim | partículas subindo + brilho | Add |
| **Transformação** | 24–40 | 24 | não | explosão vertical + choque | Add |
| **Escudo** | 8 (in) + 12 loop | 24 | loop | hexágono/círculo | Add |
| **Teleporte** | 6 (out) + 6 (in) | 24 | não | silhueta + faíscas | Add |
| **Ambiente** | variável | 24 | sim | folhas, poeira, chuva | Normal |

Regra de impacto: **frame 0 = flash branco**, frame 1–2 = forma saturada, 3–5 = dissipação. O primeiro frame é 60% da leitura.

---

## 4. Camadas e paleta

Todo efeito de energia tem **3 camadas**:

| Camada | Cor | Alpha | Tamanho |
|---|---|---|---|
| Núcleo | branco `#FFFFFF` | 100% | 35–45% |
| Meio | cor do elemento | 85–100% | 70–85% |
| Borda | cor escura do elemento | 35–55% | 100% |

- Sem gradiente suave; as bordas podem ter 2–3 tons chapados.
- Partículas: círculos, losangos, riscos. Nunca textura fotorrealista.
- Fumaça: 2–3 tons de cinza-azulado, alpha 40–70%, blend normal.

---

## 5. Kits canônicos prioritários

| Técnica | Componentes | Frames totais | Cor | Observação |
|---|---|---|---|---|
| **Kamehameha** | carga 14 · pose 10 · beam start 6 · loop 4 · end 6 · impacto 8 · explosão 12 | 56 | azul | beam extensível por segmentos |
| **Galick Gun** | carga 12 · beam 6/4/6 · impacto 8 | 40 | roxo | beam mais fino e rápido |
| **Final Flash** | carga 20 · beam 8/4/8 · explosão 16 | 60 | amarelo | mais largo que o Kamehameha |
| **Big Bang Attack** | carga 10 · orbe 6 · explosão 14 | 34 | azul | projétil esférico |
| **Masenko** | pose 8 · beam 6/4/6 · impacto 8 | 34 | amarelo | disparo de testa |
| **Makankosappo** | carga 18 · espiral 10 · beam 6/4/6 · impacto 10 | 52 | verde | drill, 2 feixes helicoidais |
| **Genki Dama** | carga 30 · arremesso 12 · explosão 20 | 66 | azul-esverdeado | escala de tela |
| **Kienzan / Destructo Disc** | carga 10 · disco 6 loop · impacto 10 | 30 | amarelo | disco que retorna |
| **Solar Flare** | flash 4 · anel 6 · hold 6 | 16 | branco | tela inteira, sem dano |
| **Instant Transmission** | out 6 · in 6 | 12 | azul | silhueta + faíscas |
| **Kaioken** | aura 20 loop · ativação 12 | 32 | vermelho | aura persistente |
| **Death Beam** | 4 · 3 · 4 | 11 | roxo | rápido e fino |
| **Death Ball** | carga 12 · orbe 6 · explosão 18 | 40 | roxo | projétil grande |
| **Special Beam Cannon** | = Makankosappo | — | verde | nome alternativo |
| **Burning Attack** | pose 10 · orbe 6 · explosão 12 | 30 | laranja | Trunks |
| **Final Kamehameha** | carga 18 · beam 8/4/8 · explosão 18 | 60 | azul+amarelo | dois tons |
| **Stardust Breaker** | carga 14 · orbe 8 · explosão 16 | 40 | verde-azul | Gogeta |
| **Hakai** | carga 20 · esfera 8 · desintegrar 14 | 46 | roxo | partículas de desintegração |
| **Ki Blast básico** | 4 · 3 · 4 | 11 | amarelo | auto-attack à distância |
| **Aura SSJ** | 20 loop + ativação 24 | 44 | dourado | persiste |
| **Aura SSB** | 20 loop + ativação 24 | 44 | azul | persiste |
| **Aura UI** | 24 loop + ativação 30 | 54 | prata | persiste, partículas ascendentes |

> Cada kit é **dado**, não arte única: o runtime escolhe comprimentos de beam e escala de explosão.

---

## 6. Beams extensíveis

Um beam é composto por:

- `beam_start` (6 frames) — nasce na mão/boca/testa;
- `beam_mid` — segmento tileável de 64 px, esticado por escala no eixo do disparo;
- `beam_end` (6 frames) — ponta com “cabeça” luminosa;
- `impact` + `explosion` no alvo.

Regras:
- O segmento do meio tem topo e base **compatíveis** (sem costura visível).
- A largura do beam é declarada (`width_px`) e constante.
- O beam nunca é desenhado atravessando o corpo do personagem; sai do socket.
- Em multiplayer, o beam é predito no cliente e confirmado no servidor.

---

## 7. Trail, smear e impacto

- **Trail de arma:** 3–5 frames, alpha decrescente, cor do elemento ou branco; segue `weapon_tip`.
- **Smear de ataque físico:** 2 frames de arco branco com alpha 60%, sem contorno.
- **Impacto:** flash branco 1 frame + estrela 3 frames + anel 4 frames.
- **Screen shake:** leve 3 px/120 ms · pesado 6 px/180 ms · crítico 10 px/260 ms.
- **Hitstop:** sincronizado com o clipe (doc 04 §7.2).

---

## 8. Composição e legibilidade

| Regra | Valor |
|---|---|
| Cobertura máxima da tela (skill normal) | 25% |
| Cobertura máxima (ultimate/boss) | 55% |
| Oclusão da cabeça do personagem | ≤ 3 frames |
| Alpha máximo sobre o corpo | 0,75 |
| Nº de partículas simultâneas | ≤ 24 |
| Nº de camadas simultâneas | ≤ 6 |
| Contraste com o fundo | sempre ≥ 2 tons de diferença |

- Efeitos não podem esconder a hurtbox do alvo por mais de 3 frames.
- Em cenas com 30 personagens, VFX de auto-attack são reduzidos a 60% do tamanho.
- Deve existir opção de “VFX reduzido” (acessibilidade) — documentada na UI.

---

## 9. Especificações de arquivo

| Item | Valor |
|---|---|
| Canvas pequeno | 256 × 256 |
| Canvas médio | 512 × 512 |
| Canvas grande (ultimate) | 1024 × 1024 |
| Alpha | straight, PNG RGBA |
| Blend | declarado no manifest |
| Frame rate de autoria | 24 |
| Export | PNG sequence + spritesheet + GIF preview |
| Naming | `DB_VFX_<ELEMENT>_<KIND>_<NAME>_<FRAME>` |
| Metadata | `asset_id`, `element`, `blend`, `anchor`, `fps`, `loop`, `frames`, `screen_coverage` |

---

## 10. Integração

- VFX são ancorados a **sockets** de osso, não a coordenadas fixas.
- Em engines com skeletal, usar `bone attachment` + `flip` automático.
- Em engines com spritesheet, usar `socket offset` no JSON.
- O VFX nunca move o personagem; apenas o feedback (shake) move a câmera.
- Ordem de render: `aura_back` (20) → corpo → `attack_fx` (150) → `aura_front` (160) → UI.

---

## 11. Checklist de VFX

- [ ] Sem contorno.
- [ ] 3 camadas de energia (núcleo/meio/borda).
- [ ] Paleta do elemento correta.
- [ ] Blend declarado.
- [ ] ≤ 24 partículas.
- [ ] Não cobre a cabeça por > 3 frames.
- [ ] Componentizado (não monolítico).
- [ ] Anchor/socket correto.
- [ ] Preview GIF + APNG.
- [ ] Metadados válidos.
- [ ] Testado em cena com 10+ personagens.
