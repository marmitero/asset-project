# Sonda de estilo — por que o sprite parece "feio" e o que muda isso

Documento de apoio para a decisão de direção de arte (ADR-0007, ainda não escrito).
Nada aqui altera o pipeline canônico em `exports/`; é medição, não produção.

- `out/compare_style.png` — mesmo frame em três clipes, coluna esquerda = estilo atual,
  coluna direita = variante barata (fundo claro + rampa de cor + outline quente).
- `out/reference_ai_style.jpg` — referência de *teto* gerada por IA. Não é asset do
  pacote, não é animável, serve só para calibrar expectativa.

Reproduzir: `python3 experiments/style_probe/probe.py` (≈17 s).

## Diagnóstico — o que está feio de fato

O render v1 não é feio por ser vetorial. Ele é feio por sete defeitos concretos, e
só dois deles são limitação de técnica:

| # | Defeito | Onde | Custo de corrigir |
|---|---|---|---|
| 1 | Fundo escuro + outline quase preto = contorno invisível, personagem parece adesivo | `scene.make_background` | baixo |
| 2 | Sem contorno interno: onde a peça sobrepõe a peça não há linha, então o corpo lê "chapado" | `core.build_part` | baixo |
| 3 | Sombra de duas bandas com ~4 px: a rampa existe mas não lê | `shapes.limb` | baixo |
| 4 | Silhueta de manequim: braço-tubo sem deltoide/bíceps, perna-tubo, mão pequena | `parts_goku` | médio |
| 5 | Sem dobras de tecido — gi laranja é uma mancha laranja | `parts_goku` | médio |
| 6 | Rosto: olhos altos e afastados, pupila minúscula, cabelo sem mecha | `parts_goku._face/_hair_front` | médio |
| 7 | Enquadramento: 220 px de personagem num canvas de 512 | `ShowConfig.zoom` | trivial |

A coluna "v2" do comparativo já corrige 1, 3 e parte de 7 sem tocar em geometria.
O ganho é grande e custa ~40 linhas — isso mostra que a maior parte do problema
**não** é o método de desenho, é acabamento.

## As três rotas

**A. Acabamento vetorial (paint pass v2)** — corrige 1–7 no renderizador atual.
Mantém 100% do que o validador já aprova (contato de pé, loop, jitter, IK).
Teto estético: "Flash game limpo", próximo do AQW real, que também é chapado.
Risco: baixo. Custo: ~1 dia. Nada de licença de terceiros.

**B. Atlas de peças pintado por IA** — IA gera cada peça (cabeça, tronco, braços,
pernas) na pose de repouso; o rig continua animando. Teto estético: alto, nível
ilustração. Riscos reais: (i) emenda nas juntas racha quando o membro dobra,
(ii) coerência de luz entre peças geradas separadamente, (iii) fundo transparente
não sai pronto — precisa de recorte por máscara. Custo: dias, com iteração.

**C. Frame a frame por IA** — descartado. Flicker entre frames, sem contato de pé
garantido, sem loop fechado, sem controle de frame de impacto. Destrói exatamente
o critério de aceitação do G3 (fluidez). Não é uma opção.

## Recomendação

Fazer **A** agora (é o 80/20 e não põe em risco a matriz validada) e usar IA onde
não existe restrição temporal: retratos, ícones de item, telas de UI, fundos de
mapa e arte promocional — que são metade do pacote e onde IA é imbatível.
Avaliar **B** depois, como "skin premium" de um único personagem, com o pipeline
já congelado: se a emenda rachar, o pacote base continua íntegro.
