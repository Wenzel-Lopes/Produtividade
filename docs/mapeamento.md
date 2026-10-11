# Controle de mapeamento

A pergunta central é: **a base observada representa a população que queremos analisar?**

O BI de referência distingue implantação, equipamento, mapeamento e recência da coleta. A versão sintética publicada demonstra a primeira parte desse raciocínio com um sinal mensal de mapeamento e tempos previstos/capturados; não implementa alertas de recência nem inventário de máquinas.

## Junho de 2025 — exemplo sintético

| Indicador | Valor | População |
|---|---:|---|
| Elegíveis no mês | 209 | Vínculo em parte do mês |
| Mapeados | 196 | Elegíveis com sinal mapped = 1 |
| Não mapeados | 13 | Elegíveis menos mapeados |
| Cobertura | 93,8% | 196 / 209 |
| Headcount final | 204 | Pessoas ativas no último dia |

## Como o backend protege a interpretação

- Uma pessoa possui no máximo um fato por mês: chave composta `(employee_id, month)`.
- `mapped` só aceita 0 ou 1.
- Sem mapeamento, os minutos capturados devem ser zero.
- Tempo produtivo não pode exceder o capturado, e o capturado não pode exceder o previsto.
- Taxas totais são recalculadas pelos totais dos numeradores e denominadores.

[Ver restrições SQL](../sql/001_schema.sql) · [Ver prévia](imagens/mapeamento.png)

## Próximo nível, ainda não implementado

Uma operação com alertas precisa definir a data da última coleta, calendário de dias úteis, limiares acordados, exceções e responsáveis. O PBIP mostra indicadores relacionados, mas não comprova qual serviço executa a automação fora do Power BI.
