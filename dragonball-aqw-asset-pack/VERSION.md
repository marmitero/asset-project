# VERSION

## Pack

| Campo | Valor |
|---|---|
| Versão do pack | **0.1.0** |
| Versão da Matriz | **0.0.0 (não congelada)** |
| Versão da Visual Bible | 1.0.0 |
| Versão da spec técnica | 1.0.0 |
| Versão do renderizador | 0.1.0 (`tools/aura/`) |
| Data | 2026-10-22 |
| Fase | 2 — Primeiro modelo renderizado (G2 ✅ · G3 em revisão) |

## Histórico

| Versão | Data | Mudança |
|---|---|---|
| 0.1.0 | 2026-10-22 | Documentação completa (21 docs, 10 standards), infraestrutura de produção, schemas, catálogo e blueprint. |
| 0.1.0+rig | 2026-10-22 | Renderizador `tools/aura/` (10 módulos), rig de 29 ossos, 28 peças procedurais, 23 clipes, 18 GIFs V01–V18, validador de 11 métricas (0 falhas), `exports/` com manifesto SHA-256. |

## Próxima versão planejada

| Versão | Gatilho |
|---|---|
| 0.2.0 | Goku base montado e 9 clipes (G2) |
| 0.3.0 | 18 GIFs aprovados por rubrica humana (G3) |
| **1.0.0** | **Matriz congelada (G4)** — bump MAJOR do pack |
| 1.x | Expansão de personagens/equipamentos/VFX/mapas/UI |
| 2.0.0 | Revisão de rig/escala (breaking) |

## Regra

`matrix_version` só muda no congelamento. Assets declaram a Matriz de origem. Mudança de pivô, altura ou ordem de camada é `MAJOR`.
