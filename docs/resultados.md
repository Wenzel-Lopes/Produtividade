# Leitura da simulação e validação

Fonte única: gerador original `produtividade/generate.py`, seed 42, contrato v1.0. Dados de janeiro a junho de 2025, com correção processada em julho. Os valores abaixo não vêm do Power BI empresarial.

## Achados demonstrativos

- Headcount final: 209 em janeiro e 204 em junho. A abertura de janeiro é 210; no semestre há 30 admissões e 36 saídas.
- Cobertura de mapeamento: 152/215 (70,7%) em janeiro e 196/209 (93,8%) em junho, aumento de 23,1 pontos percentuais.
- Cobertura de coleta: 61,2% em janeiro e 82,2% em junho. O crescimento foi intencionalmente parametrizado no cenário.
- Atividade observada: 69,6% do tempo capturado em janeiro e 68,3% em junho. Esse indicador não deve ser confundido com produtividade econômica.
- Folha demonstrativa: R$ 1.388.241,94 em janeiro e R$ 1.354.430,01 em junho. Não representa uma economia obtida por um projeto real.

## Decisão demonstrativa

Priorizar cobertura e estabilidade da coleta antes de comparações de atividade entre áreas. Em um cenário real, investigar ausência de mapeamento, adequação das fontes e diferenças de função, além de validar definições com os responsáveis. O case não estabelece causalidade nem uma meta empresarial.

## Verificações executadas

O modo SQLite foi executado e oito testes passaram: determinismo, repetição de lote, correção retroativa/versão antiga, alteração de arquivo carregado, conflito de versão com rollback, chave órfã com rollback, chave duplicada e reconciliação de métricas.

O teste de integração PostgreSQL passou no GitHub Actions com PostgreSQL 16 e Python 3.12. A execução confirmou os nove testes e o comando de demonstração. [Consultar evidência da validação](https://github.com/Wenzel-Lopes/Produtividade/actions/runs/38105245050). No ambiente local, apenas os oito testes SQLite foram executados; a apresentação registra essa validação local.

## Como conferir os números

Execute `python -m produtividade demo` e veja `reports/metrics.json`. A linha `department_id=0` é o total. O CSV também contém linhas por área; não somar o total às partes. As taxas totais usam os denominadores totais.
