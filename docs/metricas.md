# Contrato de métricas v1.0

Todos os dados são sintéticos. Janeiro a junho de 2025, datas civis sem conversão de fuso. `updated_at` usa UTC. Período de vínculo: admissão inclusiva e desligamento exclusivo (primeiro dia inativo). Uma pessoa pertence a uma área estável durante todo o cenário.

| Métrica | Regra | Limitação |
|---|---|---|
| Headcount final | Pessoas ativas no último dia do mês | Não somar headcount de meses diferentes |
| Headcount inicial | Pessoas ativas no dia anterior ao início do mês | HC final = inicial + admissões − desligamentos |
| Admissões e desligamentos | Eventos cuja data está no mês | Não há recontratações no cenário |
| Turnover de saída | Desligamentos / média do headcount inicial e final | Não é a fórmula de movimentação que inclui admissões |
| Folha demonstrativa | Soma do salário-base proporcional aos dias corridos de vínculo no mês, em centavos | Exclui encargos, benefícios, férias e regras de folha reais. Inclui ajuste tardio de R$ 150 em março |
| Cobertura de mapeamento | Pessoas mapeadas / pessoas com vínculo em parte do mês | Todas as pessoas são elegíveis no cenário. Não usa headcount final como denominador |
| Cobertura de coleta | Minutos capturados / minutos previstos | Dias úteis de segunda a sexta, 8h/dia, sem feriados. Valores de coleta são simulados |
| Atividade observada | Minutos classificados como produtivos / minutos capturados | Proxy pedagógica. Não mede valor entregue nem fundamenta ranking ou decisão sobre indivíduos |

Divisão por zero resulta em nulo (exibido como “Sem base”), não zero. Taxas do total são recalculadas com os numeradores e denominadores totais, nunca médias simples das taxas das áreas. No CSV de métricas, `department_id=0` é o total: não somar essa linha às áreas.

## Granularidade e dicionário

`departments`: uma linha por área fictícia. `department_id` é a chave e `name` é o rótulo.

`employees`: uma linha por vínculo fictício; chave `employee_id`; chave estrangeira `department_id`; `hired_on`/`ended_on` definem elegibilidade; `salary_cents` informa salário-base simulado. Não há nomes, CPF, e-mail, nascimento ou atributos sensíveis.

`monthly_facts`: uma linha por pessoa/mês com vínculo em algum dia. Chave composta (`employee_id`,`month`). `month` é sempre o primeiro dia. `payroll_cents` é a parcela demonstrativa do mês. `scheduled_minutes`, `captured_minutes` e `productive_minutes` são inteiros com produtivos ≤ capturados ≤ previstos. `mapped` é 0/1, e não mapeados têm coleta zero.

`etl_batches`: uma linha por lote, com nome, SHA-256, horário de commit e quantidade de linhas inseridas/alteradas. Não é uma contagem apenas de fatos.

Todas as entidades têm `updated_at`, timestamp canônico em UTC que ordena as versões. A versão v1 usa datas em texto ISO para compartilhar o mesmo DDL entre SQLite e PostgreSQL. As views PostgreSQL convertem essas colunas para tipos temporais nas consultas. Em produção, preferir tipos nativos e contratos na origem.
