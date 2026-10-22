# 12 — QUALITY GATES
**Projeto AURA · v1.0.0**
Define o que "pronto" significa, como se testa e quem pode aprovar.

---

## 1. Fluxo de status

```
PLANNED → GENERATED → PROCESSING → QA_PENDING → APPROVED
                                   │
                                   ├→ REWORK_REQUIRED → PROCESSING
                                   └→ BLOCKED → (decisão)
APPROVED → DEPRECATED (substituído)
```

- Nenhum asset pula etapa.
- `APPROVED` exige: validação automática PASS + checklist visual + rubric (se animado) + registro no manifesto.
- Quem aprova: o agente de produção (com evidência em arquivo). O usuário aprova o **gate**, não cada asset.

---

## 2. Gates do projeto

| Gate | Nome | Critério objetivo | Evidência |
|---|---|---|---|
| **G0** | Documentação | 19 docs + 10 standards existentes, consistentes, sem TODO | `docs/`, `standards/` |
| **G1** | Infra | `validate.py` roda sem erro; renderer de prova produz frame | `production/qa_reports/G1.json` |
| **G2** | Primeiro modelo | 18 slots de corpo + equipamento montados, 9 clipes, zero peça faltante | `characters/.../goku/base/` |
| **G3** | Validação GIF | 18 GIFs + métricas PASS + rubrica ≥ 24/30 | `exports/previews/...` |
| **G4** | Matriz congelada | hashes publicados + certificado assinado | `docs/matrix/FROZEN_MATRIX_v1.0.0.json` |
| **G5** | Pack completo | metas §5 + 18 critérios do master-prompt | `asset_manifest.json` |

---

## 3. Checklists por categoria

### 3.1 Personagem
- [ ] ID, versão, rig e altura declarados.
- [ ] 18–26 peças, todas presentes, com pivô.
- [ ] 8 máscaras quando aplicável.
- [ ] Ordem de camadas correta.
- [ ] Contorno 3,0 px @220.
- [ ] ≤ 8 cores + contorno.
- [ ] Silhueta legível a 48 px.
- [ ] Faces obrigatórias (10).
- [ ] Clipes mínimos (9 para G2; 30 para G5).
- [ ] GIFs validados.
- [ ] Retrato 256² e ícone 128².
- [ ] Metadados válidos e checksums.

### 3.2 Equipamento
- [ ] Slot e `covers[]` corretos.
- [ ] Pivôs coincidem com juntas.
- [ ] Overlap 2–3 px.
- [ ] Compatível com ≥ 2 rigs.
- [ ] Sem clipping em idle/run/attack_heavy/death.
- [ ] Máscaras exportadas.
- [ ] Ícone derivado.
- [ ] 3 variantes de cor (quando previsto).

### 3.3 Animação
- [ ] Duração e fases conforme matriz.
- [ ] Eventos no frame correto.
- [ ] F1–F6 do doc 05 atendidos.
- [ ] Rubrica ≥ 24/30.
- [ ] Loop fecha.
- [ ] Sem jitter > 3°/frame².
- [ ] Secundárias ativas.
- [ ] Silhueta nos 3 frames-chave.

### 3.4 VFX
- [ ] Sem contorno.
- [ ] 3 camadas de energia.
- [ ] Paleta do elemento.
- [ ] Blend declarado.
- [ ] ≤ 24 partículas.
- [ ] Cobertura dentro do limite.
- [ ] Socket correto.
- [ ] Preview GIF/APNG.

### 3.5 Cenário
- [ ] Camadas separadas.
- [ ] Parallax declarado.
- [ ] Chão sem costura (3×3).
- [ ] Personagem legível.
- [ ] `map.json` válido.
- [ ] Colisão, spawn, portal e oclusão.
- [ ] Preview com ator de referência.

### 3.6 UI
- [ ] Texto em chave, não em imagem.
- [ ] 9-slice com insets.
- [ ] 8 estados.
- [ ] Contraste e escala.
- [ ] Ícones a 64 px.
- [ ] Atlas e tema exportados.

---

## 4. Testes automatizados

`tools/validate.py` (estrutural) + `tools/validate_animation.py` (métricas).

| Teste | Falha se |
|---|---|
| JSON schema | qualquer campo obrigatório ausente/tipo errado |
| Arquivo ausente | referência sem arquivo |
| Órfão | arquivo sem registro |
| PNG inválido | não abre, não é RGBA, alpha vazio |
| Dimensão | diferente do declarado |
| Pivô | fora da imagem e não declarado |
| ID duplicado | dois assets com mesmo ID |
| ID inválido | não casa com regex |
| Camada | valor fora de `layer_order.json` |
| Nome | fora do padrão |
| Rig | `rig_compat` inexistente |
| Frame | keyframe > duração |
| Loop | `loop=true` sem frame de fechamento |
| Socket | osso inexistente |
| Atlas | coordenadas inconsistentes |
| Checksum | hash divergente |
| Texto em UI | imagem de UI com texto detectado (manual/visual) |
| Gap de junta | > 0 px |
| Foot slip | > 1 px |
| Loop seam | > 0,5° / 0,5 px |
| Jitter | > 3°/frame² |

Saída: `production/qa_reports/<asset>__<tipo>.json` + código de saída 0/1.

---

## 5. Severidade de defeitos

| Nível | Definição | Ação |
|---|---|---|
| **S1 — bloqueante** | asset inutilizável (pivô errado, peça faltando, alpha quebrado) | bloqueia gate |
| **S2 — maior** | quebra imersão ou regra visual (cor errada, fenda em pose comum) | corrige antes de aprovar |
| **S3 — menor** | detalhe estético (1 px de linha, sombra 2% fora) | corrige no próximo lote |
| **S4 — cosmético** | preferência | registra como backlog |

S1 e S2 nunca são aceitos "para depois".

---

## 6. Matriz de teste de compatibilidade

| Teste | Amostra |
|---|---|
| Rig × peças | todos os rigs × 3 sets |
| Pose × equipamento | idle, run, attack_heavy, death × 3 sets |
| Escala | 50%, 100%, 200% |
| Personagens simultâneos | 30 na cena de estresse |
| VFX × personagens | 10 atores + 5 efeitos |
| UI × resolução | 1280×720, 1920×1080, 2560×1440 |
| Idioma | textos longos (PT/EN) sem estourar |
| Acessibilidade | reduce_motion, daltonismo, escala 150% |

---

## 7. Regressão

- Todo asset aprovado tem checksum; qualquer mudança de arquivo sem bump de versão falha o build.
- O pacote de validação do G3 é re-renderizado sempre que o renderizador muda de versão.
- Comparação visual lado a lado (diff de silhueta) para detectar regressão de rig.
- Nenhum asset aprovado é regerado "por estética" sem ADR.

---

## 8. Relatório de QA

```json
{
  "asset_id": "DB_CHAR_HERO_GOKU_BASE",
  "version": "1.0.0",
  "date": "2026-10-22T00:00:00Z",
  "automated": {"status": "PASS", "failures": []},
  "visual": {"status": "PASS", "notes": []},
  "animation": {"rubric_total": 27, "per_clip": {"idle": 5, "walk": 4}},
  "defects": [{"id": "D-001", "severity": "S3", "clip": "run", "frame": 9, "desc": "leve overshoot no cotovelo"}],
  "decision": "APPROVED",
  "approver": "agent",
  "matrix_version": "1.0.0"
}
```

---

## 9. Relatório de sessão (obrigatório)

```
SESSION ID:
PHASE:
OBJECTIVE:

IMAGE GENERATIONS:
- Planned new:
- Executed new:
- Reserved corrections:
- Executed corrections:
- Total executed:

ASSETS CREATED:
ASSETS APPROVED:
ASSETS REJECTED:
ASSETS PENDING:

FILES EXPORTED:
METADATA UPDATED:

QUALITY ISSUES:
CORRECTIONS PERFORMED:

CURRENT PROJECT STATUS:
NEXT SESSION OBJECTIVE:
```

- Salvo em `production/session_reports/S<nn>_<tema>.md`.
- Deve refletir o que existe no disco, não intenção.
- Nenhuma sessão termina sem relatório e sem atualizar `continuity_state.json`.

---

## 10. Definição de pronto do pack (G5)

1. Metas de conteúdo do master-prompt §22 atingidas.
2. `validate.py` com 0 erros.
3. Todos os assets `APPROVED` com checksum.
4. Previews de todas as categorias.
5. Integração demonstrável em 3 engines.
6. Documentação sem TODO.
7. `continuity_state.json` final.
8. Licença e notas de IP atualizadas.
