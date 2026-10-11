# Apresentação do case em 7 minutos

## 0:00–1:00 — Contexto

“Este é um case demonstrativo que integra análise de pessoas, custos e cobertura operacional. Todos os dados são sintéticos. A pergunta central é como acompanhar o quadro e os custos sem confundir ausência de coleta com ausência de atividade.”

## 1:00–2:00 — Modelagem e métricas

Explique o grão pessoa/mês e por que headcount no fim do mês difere de pessoas elegíveis em qualquer dia. Explique o desligamento como primeiro dia inativo, o uso de centavos e as exclusões da folha simulada.

## 2:00–3:00 — Integração

Demonstre a carga da base, a repetição do lote e a carga incremental. Junho entra e março muda. Explique por que selecionar somente datas de fato posteriores ao último mês perderia correções antigas.

## 3:00–4:00 — Qualidade

Mostre a equação do headcount, a reconciliação da folha, a chave composta e o rollback por erro. Diferencie cobertura de mapeamento de cobertura de coleta. Não afirme que todos os controles de produção estão implementados.

## 4:00–5:30 — Leitura executiva

Mostre os filtros do site. A melhora programada de cobertura torna mais dados observáveis. O percentual de atividade utiliza apenas o tempo capturado; não mede valor de negócio nem desempenho individual. Uma decisão simulada é priorizar a qualidade da coleta antes de comparar áreas.

## 5:30–7:00 — Limites e evolução

Explique a ausência de encargos, feriados e histórico de transferências. Proponha evolução para staging, dimensão histórica, orquestração e alertas. Não prometa ganho financeiro baseado na simulação.

## Contribuição profissional: preencher antes de usar

Para cada projeto empresarial, escreva: problema, período, papel pessoal, partes implementadas, partes de terceiros, evidência permitida e resultado verificável. Separe observações do workspace de afirmações de autoria. Não declare que implementou sozinho o que ainda não confirmou.

Estude e execute este código antes de apresentá-lo. Se perguntarem sobre ferramentas de apoio, explique como utilizou assistência na implementação e quais escolhas consegue justificar pessoalmente.
