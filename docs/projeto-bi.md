# Mapa do projeto Power BI

## Escopo observado

A inspeção estática do PBIP fornecido identificou 13 páginas (incluindo tooltips), 125 medidas, 38 relacionamentos, 47 tabelas e cinco papéis de segurança. Das tabelas, 24 são calendários automáticos. A contagem de papéis não comprova testes de autorização. Não foi executada atualização de fontes corporativas.

| Módulo de referência | Elementos identificados | O que avaliar numa entrevista |
|---|---|---|
| Analytics Operacional | Filtros, cartões, séries temporais, matriz e categorias de atividade | Contexto de filtro, jornada e interpretação das taxas |
| Analytics Comercial | Indicadores de custos, vendas e resultado, além de atividade | Granularidade, relacionamento entre fatos e comparabilidade |
| Mapeamento | Implantação, presença de equipamento, sucesso do mapeamento e recência de coleta | Cobertura da população e lacunas de observação |
| Visão Geral | Síntese de cobertura e atividade | Clareza executiva e navegação |
| Visão 360 Colaborador | Página dedicada ao recorte individual | Necessidade de acesso restrito e limites de uso |
| Documentação e tooltips | Página de documentação e páginas auxiliares | Explicação contextual dos indicadores |

## Relação com esta versão pública

O código público foi criado separadamente para demonstrar geração de dados, integridade, carga incremental e cálculo de indicadores. Não é uma exportação do backend empresarial. A galeria redesenha duas perguntas analíticas com os agregados sintéticos disponíveis; não representa capturas do relatório original.

Para uma futura versão PBIP pública, é necessário reconstruir fontes e medidas publicáveis, validar relacionamentos, substituir imagens e textos internos e testar o relatório no Power BI Desktop. Remover somente o cache ou renomear empresas não torna o restante do projeto automaticamente publicável.

[Voltar ao portfólio](../README.md)
