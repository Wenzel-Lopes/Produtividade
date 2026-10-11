# Recriação no Power BI Desktop

O pacote entrega dados, contratos, consultas e medidas de referência. Não contém um `.pbix` pronto e não modifica os relatórios empresariais.

1. Execute `python -m produtividade demo` para conhecer os resultados.
2. Para explorar os agregados, importe `reports/metrics.csv`. Defina `month` como data; contagens como inteiros; valores monetários e razões como decimais, usando localidade compatível com ponto decimal do CSV.
3. Para um modelo detalhado PostgreSQL, siga o README e importe `departments`, `employees` e `monthly_facts` do banco demonstrativo. Defina datas e timestamps nos tipos correspondentes.
4. Crie relações unidirecionais 1:N de `departments[department_id]` para `employees[department_id]` e de `employees[employee_id]` para `monthly_facts[employee_id]`. Crie `DimMes` com uma linha por mês e relacione-a à coluna `monthly_facts[month]`. Evite uma tabela com datas diárias para esse relacionamento sem documentar o grão mensal.
5. Crie as medidas abaixo no modelo detalhado. Exiba percentuais com uma casa e folha em reais. O turnover deve vir da view `vw_kpis_monthly`, com a fórmula agregada do contrato; não faça média simples das taxas.
6. Monte páginas “Resumo”, “Pessoas e custos” e “Cobertura”. Use seletor de mês e área, tendências mensais e uma tabela com métricas e denominadores. Inclua “DADOS 100% SINTÉTICOS” em todas as páginas.
7. Para demonstrar a carga incremental, carregue a base primeiro e atualize o modelo; depois carregue o lote incremental e atualize. Junho aparece e março recebe o ajuste de R$ 150. A carga incremental do Python é distinta do recurso de atualização incremental do Power BI, que não está configurado aqui.

```dax
Folha Demonstrativa = DIVIDE(SUM(monthly_facts[payroll_cents]), 100)
Cobertura Mapeamento = DIVIDE(SUM(monthly_facts[mapped]), COUNTROWS(monthly_facts))
Cobertura Coleta = DIVIDE(SUM(monthly_facts[captured_minutes]), SUM(monthly_facts[scheduled_minutes]))
Atividade Observada = DIVIDE(SUM(monthly_facts[productive_minutes]), SUM(monthly_facts[captured_minutes]))
```

As medidas são novas para este cenário, não foram copiadas dos relatórios da empresa. Não use a atividade observada como ranking de pessoas. Não publique o relatório empresarial para demonstrar este case.
