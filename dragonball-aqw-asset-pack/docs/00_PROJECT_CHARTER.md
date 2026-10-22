# 00 — PROJECT CHARTER
**Projeto:** `dragonball-aqw-asset-pack` · codinome **AURA**
**Versão:** 1.0.0 · **Data:** 2026-10-22 · **Fase:** 1 (Documentação)
**Autoridade:** este documento + `docs/master-prompt.md`. Em conflito, vale o master-prompt; em lacuna, valem as decisões registradas aqui.

---

## 1. Visão

> Criar o **asset pack 2D mais completo e tecnicamente utilizável** para construir um MMORPG de ação em tempo real com a linguagem visual e de movimento de *AdventureQuest Worlds*, aplicada à identidade canônica de *Dragon Ball* — com qualidade de produção, modularidade real e documentação suficiente para que **uma IA** monte o jogo sem intervenção de um artista.

## 2. Problema que o projeto resolve

Asset packs comuns falham em um de três pontos:

1. **Não são modulares de verdade** — são ilustrações bonitas sem peças, pivôs ou hierarquia.
2. **Não são animáveis** — não há timeline, curva, evento ou hit frame; o dev precisa redesenhar.
3. **Não são consistentes** — cada item parece de um jogo diferente, e nada encaixa.

O AURA ataca os três com: **rig determinístico**, **timeline em dados** e **Matriz congelada** (padrões com hash).

## 3. Público-alvo

| Público | O que precisa encontrar no pack |
|---|---|
| **Agente de IA** (principal) | JSONs válidos por schema, IDs estáveis, padrões explícitos, exemplos de composição, handbook de consumo. |
| Desenvolvedor solo / small studio | Peças PNG, spritesheets, rig pronto, integração Godot/Unity/web. |
| Artista 2D | Visual Bible, pranchas de proporção, regras de shading, templates de peças. |
| Designer de jogo | Blueprint de mecânicas, matriz de animação, economia, classes, progressão. |

## 4. Escopo

### Dentro
- Personagens paper-doll (heróis, vilões, NPCs) com peças, rig, clipes e metadados.
- Transformações como *swaps* de peças + VFX + clipes especiais.
- Equipamentos modulares (armaduras, armas, helms, capas, luvas, botas, acessórios).
- Inimigos (comuns, elites, bosses) com rigs próprios quando a anatomia exigir.
- Pets e invocações.
- VFX componentizados (cast, acúmulo, projétil, impacto, explosão, aura, buff).
- Cenários 2.5D em camadas, tiles, props, colisão, oclusão, portais.
- UI kit completo de MMO (HUD, inventário, equipamento, skills, quests, loja, chat, diálogos, criação de personagem, ícones).
- Metadados, schemas, validador, exemplos de integração e documentação.
- Blueprint de jogo (classes, combate, progressão, quests, economia) como inspiração AQW.

### Fora
- Código de um jogo completo e jogável (entregamos cenas/exemplos de integração, não um MMO).
- Servidor, netcode, banco de dados, autenticação.
- Áudio (apenas *sugestões* de SFX e música; nenhum arquivo de áudio é obrigatório).
- Animações 3D, modelos 3D, rigs de engine proprietários como única entrega.
- Reprodução de qualquer arquivo oficial da Artix Entertainment ou de Dragon Ball.
- Localização de textos embutidos em imagens.

## 5. Pilares

1. **Fluidez primeiro.** Nenhum asset é aprovado sem validação em movimento (§ ver doc 05).
2. **Modularidade real.** Se não desmonta, não serve.
3. **Determinismo.** O mesmo input de rig produz o mesmo frame, sempre.
4. **Legibilidade.** Silhueta e leitura de combate acima de detalhe.
5. **Documentação como produto.** O pack é consumível por humanos e por máquinas.
6. **Continuidade.** Estado persistido; nunca reiniciar do zero.
7. **Honestidade técnica.** Nada é declarado pronto sem evidência em arquivo.

## 6. ADR-0001 — Pipeline vector-first e uso restrito de IA generativa

**Contexto.** O master-prompt sugere gerar sprites por IA. A experiência mostra que 21 peças geradas separadamente não compartilham proporção, pivô, espessura de linha nem paleta; recortá-las e realinhá-las consome mais tempo do que desenhar, e o resultado nunca fecha em costura.

**Decisão.**
- A arte de personagem, equipamento, UI e VFX é **autorada em formas vetoriais determinísticas** e renderizada por um rasterizador próprio (Python + Pillow + NumPy, supersampling 4×, contorno por dilatação de alpha, cel-shading por recorte de máscara).
- O rig, a animação e os metadados são **dados** (JSON), não pixels.
- IA generativa é usada **somente** para: concept/referência visual, cenários pintados de fundo (backdrops) e texturas orgânicas — nunca para peças modulares de personagem.

**Consequências.**
- (+) Pivôs exatos, peças reutilizáveis, interpolação verdadeira, reprodutibilidade bit-a-bit.
- (+) Custo marginal de novo personagem cai (mesmo rig, nova paleta e silhueta).
- (−) Exige construir o renderizador e a biblioteca de formas antes do primeiro personagem.
- (−) O estilo depende da qualidade da modelagem vetorial; iterações são no código, não no prompt.

**Status:** aceito.

## 7. ADR-0007 — Identidade e nomenclatura

- Nome técnico da pasta: `dragonball-aqw-asset-pack` (fixado pelo master-prompt §4).
- Codinome público: **AURA** (evita sugerir produto oficial).
- Prefixo de ID: `DB_` (fixado pelo master-prompt §5).
- A obra é **inspirada** em Dragon Ball e em AQW; não é oficial, licenciada ou endossada.

## 8. Governança de assets

Estados permitidos (master-prompt §23): `PLANNED`, `GENERATED`, `PROCESSING`, `QA_PENDING`, `APPROVED`, `REWORK_REQUIRED`, `BLOCKED`, `DEPRECATED`.

Regras:
- Só `APPROVED` entra em `asset_manifest.json`.
- Todo asset tem ID imutável, versão semântica e sessão de origem.
- Mudança de padrão visual = ADR + nova versão da Matriz + plano de migração.
- Asset rejeitado vai para `production/rejected/` com motivo e nunca é apagado sem registro.

## 9. Métricas de sucesso do projeto

| Métrica | Alvo |
|---|---|
| Personagens montáveis com rig documentado | ≥ 30 |
| Clipes animados aprovados | ≥ 500 (somando personagens/inimigos/pets) |
| Rubrica de fluidez média nos clipes de personagem | ≥ 26/30 |
| Cobertura de categorias do master-prompt §22 | 100% das metas |
| Validador (`validate.py`) | 0 erros no pacote final |
| Documentos com exemplos executáveis | ≥ 10 |
| Integração demonstrável | 3 engines (Godot, Unity, web/canvas) |

## 10. Restrições e premissas

- **Ambiente:** sem GPU, sem Adobe, sem Spine. Python 3.11 + Pillow + NumPy + ImageMagick. Render é CPU-bound.
- **Sem ffmpeg:** previews em GIF (25 fps) e APNG (60 fps); MP4 é opcional/documentado.
- **Sem fontes licenciadas de fantasia:** UI usa DejaVu como placeholder e documenta substituição.
- **Tempo:** projeto de longo prazo; cada sessão deve terminar com estado persistido e progresso verificável.

## 11. Propriedade intelectual

Ver `LICENSE_NOTES.md`. Resumo: Dragon Ball pertence a seus titulares; AQW pertence à Artix Entertainment; o pack é derivado/inspiracional, sem assets oficiais, sem declaração de licença, e a distribuição comercial exige autorização dos titulares.

## 12. Documentos relacionados

`PLAN.md` (plano executivo) · `docs/01_VISUAL_BIBLE.md` · `docs/02_TECHNICAL_SPECIFICATION.md` · `docs/04_ANIMATION_STANDARD.md` · `docs/05_FLUIDITY_AND_GIF_VALIDATION.md` · `docs/14_ROADMAP_AND_SESSIONS.md` · `docs/17_AI_AGENT_HANDBOOK.md`
