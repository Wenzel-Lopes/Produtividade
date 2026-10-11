# Reprodução visual a partir do PBIP

`layout.json` contém somente nomes de páginas, tipos de visuais, posições, dimensões e títulos revisados. Consultas, medidas, parâmetros, filtros, conexões, IDs internos e imagens empresariais não foram exportados. A cor azul foi identificada nas propriedades das formas laterais.

`amostra.json` registra os principais valores ilustrativos, gerados com seed 77. Outros valores esquemáticos estão explícitos no renderizador. As empresas A–D possuem 30 pessoas cada; a cobertura visual aproxima 27, 26, 28 e 27 pessoas mapeadas. A amostra tem 92 máquinas corporativas, oito próprias, oito pessoas sem máquina e 12 sem mapeamento; entre 100 usuários com máquina, 94 coletaram. Destes, 82 estão no grupo recente, oito em atenção e quatro no grupo crítico. Essas regras existem apenas para compor a prévia.

Os índices operacionais e distribuições temporais são ilustrativos independentes, sem cálculo pelas medidas DAX do relatório. Não são evidência de performance individual ou de resultados do projeto.

## Gerar as imagens

```powershell
python -m pip install Pillow
python scripts/gerar_previa_bi.py
```

O comando lê somente o layout público revisado. Não precisa acessar o PBIP original. Gera recortes para o README e duas páginas completas em `docs/imagens/`. O arquivo `amostra.json` também é recriado de forma determinística.

## Limite da fidelidade

O renderizador preserva a composição do canvas, não implementa o motor Power BI. Gráficos compostos, categorias, formatação condicional, tooltips, interações e controles não têm equivalência completa. A fidelidade visual final só pode ser confirmada por comparação com uma renderização do Power BI Desktop.
