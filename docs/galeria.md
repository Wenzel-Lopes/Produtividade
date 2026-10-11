# O visual do projeto Produtividade

Estas prévias utilizam a **geometria real das páginas do PBIP fornecido**: posição e tamanho dos visuais, sequência das seções, títulos e barra lateral azul `#2A6484`. Os dados foram substituídos por uma amostra fictícia. A renderização é aproximada, feita fora do Power BI; não executa DAX.

## Analytics Operacional

![Primeira parte da página Analytics](imagens/analytics.png)

[**Abrir Analytics completo, em alta resolução**](imagens/analytics-completo.png)

A página original tem 1.980 × 3.500 unidades de canvas. A prévia mantém cartões no topo, visão diária, distribuição por horário, diretoria, centro de custo, tabela de colaboradores e detalhamento de atividades. Os filtros e menus representados na imagem são estáticos.

## Mapeamento

![Primeira parte da página Mapeamento](imagens/mapeamento.png)

[**Abrir Mapeamento completo, em alta resolução**](imagens/mapeamento-completo.png)

A página original tem 2.100 × 2.400 unidades de canvas. A organização passa por visão geral, mapeamento dos usuários, centro de custo, implantação, coleta de atividades e lista detalhada. Essa estrutura é a do projeto de referência, com empresas e pessoas fictícias na prévia.

## O que foi preservado e o que foi substituído

| Preservado do layout | Substituído ou aproximado |
|---|---|
| Posições e dimensões dos blocos | Números e séries ilustrativos |
| Ordem e títulos das seções | Nomes de empresas, pessoas e áreas |
| Barra lateral azul | Logos e imagens empresariais omitidos |
| Categorias de visual | Aparência dos gráficos renderizada fora do Power BI |
| Composição vertical | Fontes, espaçamentos internos e interações aproximados |

O gráfico denominado “Heatmap - Horário” no original é do tipo área no PBIP; a prévia mantém esse tipo e esse título. Os gráficos de detalhamento são esquemáticos, sem reproduzir classificações, pesos ou regras corporativas. Os índices nos cartões são exemplos visuais, não avaliações reais de pessoas.

## Duas amostras com propósitos diferentes

- **Prévia do layout:** cenário fictício independente, seed 77, 120 pessoas, documentado em [visual-bi](visual-bi/README.md). Sem vínculo com as medidas originais.
- **Backend reproduzível:** seed 42, gerador Python e indicadores em `reports/metrics.json`. A demonstração HTML existente usa esse pipeline e possui outro layout.

Para ver o relatório com a renderização exata e filtros nativos, ainda é necessário preparar e validar uma cópia sintética no Power BI Desktop. O PBIP empresarial e seu cache permanecem fora deste repositório.

[Voltar ao portfólio](../README.md)
