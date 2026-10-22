# FREEZE CHECKLIST — MATRIZ v1.0.0
Preencher apenas quando o Gate G3 estiver aprovado. Este documento é o ritual de congelamento.

---

## 1. Pré-requisitos (G3)

- [ ] 18 GIFs de validação existem em `exports/previews/DB_CHAR_HERO_GOKU_BASE/`.
- [ ] Cada GIF tem `manifest.json` com hash do rig e do clipe.
- [ ] Relatório automático `production/qa_reports/DB_CHAR_HERO_GOKU_BASE__anim.json` = PASS.
- [ ] Rubrica ≥ 24/30 por clipe, nenhum critério < 3.
- [ ] Revisão visual do usuário registrada em `S07_validation.md`.
- [ ] Nenhum S1/S2 aberto.

## 2. Itens a congelar

| Item | Arquivo | SHA-256 |
|---|---|---|
| Esqueleto | `standards/skeleton_humanoid.json` | |
| Escala/canvas | `standards/canvas_and_scale.json` | |
| Camadas | `standards/layer_order.json` | |
| Paleta | `standards/palette_master.json` | |
| Matriz de clipes | `standards/clip_matrix.json` | |
| Easing | `standards/easing_library.json` | |
| Naming | `standards/naming.json` | |
| Schema de rig | `standards/rig.schema.json` | |
| Schema de animação | `standards/animation.schema.json` | |
| Schema de manifesto | `standards/asset_manifest.schema.json` | |
| Visual Bible | `docs/01_VISUAL_BIBLE.md` | |

## 3. Valores congelados (preencher)

```
character_height_px: 220
head_height_px: 36
canvas: 512 x 512
ground_y: 448
center_x: 256
outer_stroke_px: 3.0
inner_stroke_px: 1.8
back_shade: 0.82
fps_base: 24
fps_sample: 60
gif_fps: 25
first_model_clips: 9
validation_gifs: 18
rig_version: 1.0.0
```

## 4. Certificado

```json
{
  "matrix_version": "1.0.0",
  "frozen_at": "<ISO-8601>",
  "frozen_by": "<agente/humano>",
  "gate": "G3",
  "hashes": {},
  "validation": {"gifs": 18, "rubric_min": 0, "rubric_avg": 0, "auto": "PASS"},
  "statement": "A Matriz v1.0.0 está congelada. Todo asset a partir desta data deve conformar-se a ela ou apresentar ADR de exceção com plano de migração.",
  "approved_by_user": false
}
```

## 5. Comunicação

- Atualizar `VERSION.md` (pack → 1.0.0).
- Atualizar `production/continuity_state.json` (`matrix_frozen: true`).
- Atualizar `asset_manifest.json` com o primeiro asset.
- Registrar no `generation_ledger.json`.
- Anunciar no README o novo estado.

## 6. Pós-congelamento

- Toda mudança em item congelado: ADR + impacto + migração.
- Regenerar previews afetados.
- Bump de `matrix_version` (MINOR para adição compatível, MAJOR para breaking).
- Nunca editar hash no certificado; emitir novo certificado.
