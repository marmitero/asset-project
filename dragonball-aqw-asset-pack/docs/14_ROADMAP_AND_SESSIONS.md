# 14 — ROADMAP E SESSÕES
**Projeto AURA · v1.0.0**
Plano de execução detalhado: fases, sessões, entregáveis, critérios de saída, backlog e prioridades.

---

## 1. Visão geral

```
FASE 0  Auditoria ──────────────── S00            ✅
FASE 1  Documentação ───────────── S01            ✅
FASE 2  Primeiro modelo ────────── S02–S06        ← próximo
FASE 3  Validação GIF ──────────── S07            gate G3
FASE 4  Matriz congelada ───────── S08            gate G4
FASE 5  Heróis ─────────────────── S09–S14
FASE 6  Transformações ─────────── S15–S18
FASE 7  Equipamentos ───────────── S19–S24
FASE 8  Inimigos ───────────────── S25–S31
FASE 9  Pets ───────────────────── S32–S34
FASE 10 VFX ────────────────────── S35–S40
FASE 11 Cenários ───────────────── S41–S48
FASE 12 UI ─────────────────────── S49–S54
FASE 13 Integração e QA ────────── S55–S60       gate G5
```

---

## 2. Fase 2 — Primeiro modelo (detalhada)

**Objetivo:** Goku base completo, montável, animável, com 9 clipes e zero dívida de rig.
**Rig:** `DB_RIG_HUMANOID_MALE_A` · **Altura:** 220 px · **Canvas:** 512²

| Sessão | Objetivo | Entregáveis | Saída |
|---|---|---|---|
| **S02** | Núcleo do renderizador e do rig | `tools/rig/*`, `tools/render/*`, CLI `build`; render de um manequim de teste | manequim montado, frame PNG, teste de determinismo |
| **S03** | Corpo base (pele) | 18 peças do corpo, 8 máscaras, pivôs, `skeleton.json` | montagem A-pose sem fenda |
| **S04** | Figurino Goku | gi (torso, pelvis, braços, pernas), luvas, botas, faixa, cinto; cabelo frente/trás; face neutra | personagem completo em repouso |
| **S05** | Rosto e cabelo | 10 faces, blink, 3 penteados (base, SSJ placeholder, danificado) | expressões legíveis a 100% e 50% |
| **S06** | Clipes mínimos | idle, idle_combat, walk, run, attack_light_1, attack_whiff, hurt_light, hurt_crit, death | 9 clipes reproduzíveis |

**Critério de saída (G2):**
- 18 slots de corpo + equipamento montados; 18–26 peças.
- Zero peça faltante; zero fenda em 4 poses de teste.
- 9 clipes com eventos.
- `validate.py` sem erro estrutural.
- Nenhum TODO visível.

### 2.1 Tarefas técnicas da S02 (ordem)
1. `transform.py`: matriz 2D, composição, inversa.
2. `skeleton.py`: carregar `skeleton_humanoid.json`, validar pais.
3. `shapes.py`: Bézier → polígono, preenchimento, máscara.
4. `stroke.py`: contorno por dilatação.
5. `shading.py`: recorte de sombra e brilho.
6. `composer.py`: ordem de camadas + downsample.
7. `timeline.py`: sampling com easing.
8. Teste: manequim 220 px, 24 peças geométricas, 1 frame; hash estável em 3 execuções.

---

## 3. Fase 3 — Validação (detalhada)

| Sessão | Objetivo | Entregáveis |
|---|---|---|
| **S07a** | Render dos 18 GIFs | `exports/previews/DB_CHAR_HERO_GOKU_BASE/` + manifest |
| **S07b** | Métricas automáticas | relatório `qa_reports/...__anim.json`, corrigir falhas |
| **S07c** | Revisão visual + rubrica | ficha preenchida, defeitos priorizados |
| **S07d** | Correções e re-render | v0.1.x; máximo 3 ciclos por clipe |
| **S07e** | Aprovação | `S07_validation.md`, rubrica ≥ 24/30 |

**Critério de saída (G3):** doc 05 §11.

---

## 4. Fase 4 — Congelamento

| Sessão | Objetivo | Entregáveis |
|---|---|---|
| **S08** | Publicar Matriz v1.0.0 | `FROZEN_MATRIX_v1.0.0.json` com hashes, certificado, `VERSION.md`, `continuity_state.json`, `asset_manifest.json` com 1 personagem |

**Regra:** a partir daqui, mudanças exigem ADR.

---

## 5. Fase 5 — Heróis

| Sessão | Personagem | Reuso | Especificidade |
|---|---|---|---|
| S09 | Vegeta base | rig + 18 peças | armadura, ombreiras, cabelo |
| S10 | Gohan (adulto) | rig | cabelo, gi roxo, rosto |
| S11 | Piccolo | rig namekian adaptado | antenas, capa, turbante, 4 dedos |
| S12 | Trunks (futuro) | rig | jaqueta, espada, cabelo |
| S13 | Kuririn | rig | careca, gi laranja, estatura |
| S14 | Bulma | rig female | cabelo, roupa, sem combate pesado |

Cada um: peças, máscaras, faces, 9 clipes, GIFs, retrato, ícone, metadata.

---

## 6. Fase 6 — Transformações

| Sessão | Conteúdo |
|---|---|
| S15 | SSJ1, SSJ2, SSJ3 (cabelo + aura + clipes de transformação) |
| S16 | SSG, SSB, SSB Evolution |
| S17 | Ultra Instinct Sign/UI, Ultra Ego |
| S18 | Golden Frieza, Beast, Orange Piccolo, fusões |

Cada transformação: swap de cabelo/olhos/sobrancelha, aura, `transform_in/out`, ícone, retrato, metadata `form`.

---

## 7. Fase 7 — Equipamentos

| Sessão | Entrega |
|---|---|
| S19 | 4 sets T0 (Goku, Vegeta, Turtle, Piccolo) |
| S20 | 4 sets T0 (Saiyaman, Freeza soldier, Red Ribbon, Galactic Patrol) |
| S21 | 4 sets T1 (Fusion, King Kai, Cell saga, Namek warrior) |
| S22 | 25 armas (espadas, adagas, cajados) |
| S23 | 25 armas (lanças, machados, marretas, manoplas, bastões) |
| S24 | 20 helms + 20 capas + 20 acessórios + ícones |

Metas: 20 sets · 50 armas · 30 helms/capas · 50 acessórios.

---

## 8. Fase 8 — Inimigos e bosses

| Sessão | Entrega |
|---|---|
| S25 | 10 comuns (Saibaman, Freeza soldier, RR soldier, Cell Jr...) |
| S26 | 10 comuns (Bandit, Wolf, Dino, Namek creature...) |
| S27 | 6 elites (Raditz, Nappa, Zarbon, Dodoria, Android 19, Dabura) |
| S28 | 4 bosses T1 (Vegeta Saiyan, Frieza, Cell, Majin Buu) |
| S29 | 3 bosses T2 (Beerus, Goku Black, Jiren) |
| S30 | 3 bosses T2 (Broly, Janemba, Omega Shenron) |
| S31 | retratos, ícones de alvo, VFX assinatura, QA |

---

## 9. Fase 9–12

| Fase | Sessões | Entrega |
|---|---|---|
| Pets | S32–S34 | 20–50 pets, rigs 4–8 ossos, idle/follow/attack |
| VFX | S35–S40 | 40+ técnicas componentizadas, 20 ícones |
| Cenários | S41–S48 | 8 mapas completos (camadas, tiles, props, colisão) |
| UI | S49–S54 | 12 telas, HUD, 100+ ícones, tema, atlas |

---

## 10. Fase 13 — Integração e QA

| Sessão | Entrega |
|---|---|
| S55 | Exportadores finais, atlas, checksums |
| S56 | Exemplo Godot 4 jogável (arena + 3 inimigos) |
| S57 | Exemplo Unity 2D |
| S58 | Exemplo web (canvas) |
| S59 | QA completo (`validate.py` 0 erros), estresse 30 atores |
| S60 | Pacote final, README de consumo, manifesto, release |

---

## 11. Backlog

`production/production_backlog.json`:

```json
{
  "items": [
    {
      "id": "BL-0001",
      "asset_id": "DB_CHAR_HERO_GOKU_BASE",
      "title": "Goku base completo",
      "phase": 2,
      "priority": "T0",
      "depends_on": ["BL-0000"],
      "estimate": "5 sessions",
      "status": "PLANNED",
      "acceptance": ["9 clips", "18 GIFs", "rubric >= 24"]
    }
  ]
}
```

### 11.1 Prioridades
| Tier | Critério |
|---|---|
| **T0** | bloqueia gate ou outro asset (rig, Goku, 8 sets, VFX base, HUD, mapa Paozu) |
| **T1** | primeiro conteúdo jogável (heróis, inimigos comuns, mapa Kame House) |
| **T2** | variedade (vilões, bosses, pets, transformações) |
| **T3** | polimento e extras (emotes, seasonais, casas) |

### 11.2 Regras de backlog
- Todo item tem ID, fase, prioridade, dependência e critério de aceite.
- Não se inicia item com dependência aberta.
- Item bloqueado recebe motivo e data de revisão.
- Backlog é reordenado ao fim de cada fase.

---

## 12. Marcos

| Marco | Definição | Gate |
|---|---|---|
| **M1 — Fundação** | docs + infra + standards | G0/G1 |
| **M2 — Prova de fluidez** | Goku completo + 18 GIFs aprovados | G2/G3 |
| **M3 — Molde** | Matriz v1.0.0 congelada | G4 |
| **M4 — Jogo jogável** | 7 heróis + 20 inimigos + 8 mapas + HUD + VFX | — |
| **M5 — Pack completo** | metas de conteúdo + 3 integrações | G5 |

---

## 13. Metas de conteúdo (master-prompt §22)

| Categoria | Meta | Fase |
|---|---|---|
| Corpos/rigs | 10+ | 2, 5, 8 |
| Personagens | 30+ | 5, 6, 8 |
| Transformações | 30+ | 6 |
| Sets de armadura | 20+ | 7 |
| Armas | 50+ | 7 |
| Helms/cabelos/acessórios | 30+ | 7 |
| Pets | 20–50 | 9 |
| Inimigos comuns | 20+ | 8 |
| Bosses | 10+ | 8 |
| Mapas | 5–10 | 11 |
| NPCs | 10+ | 5, 12 |
| Habilidades/VFX | 40+ | 10 |
| Ícones | 100+ | 7, 10, 12 |
| UI | 12 telas | 12 |

---

## 14. Template de sessão

```markdown
# S<nn> — <título>

**Fase:** <n> · **Data:** <data> · **Duração:** <tempo>
**Objetivo:** <uma frase>

## Escopo
- [ ] item 1
- [ ] item 2

## Orçamento
- Gerações de imagem: planejadas __ / reservadas __ / executadas __
- Sessões de engenharia: __

## Execução
<o que foi feito, com caminhos de arquivo>

## Validação
<comandos, resultados, métricas>

## Problemas
<defeitos, decisões, bloqueios>

## Estado
- Assets criados:
- Assets aprovados:
- Próxima sessão:

## Anexos
<links para previews e relatórios>
```

---

## 15. Regras do roadmap

- Nenhuma fase começa sem o gate anterior aprovado.
- Estimativas são ordens de grandeza, não promessas.
- Se um gate falhar duas vezes, revisar o padrão (Matriz), não só o asset.
- O escopo só cresce com corte correspondente em outra parte (ou novo ciclo).
- O roadmap é revisitado ao fim de cada fase e versionado.
