# Executar o case Produtividade

[Voltar ao portfólio](../README.md)

## Comece aqui (sem banco externo)

Requisito: Python 3.10 ou superior. Abra o terminal na pasta deste README.

```powershell
python -m produtividade demo
python -m unittest discover -s tests -v
python -m http.server 8000 --directory site
```

Abra `http://localhost:8000` no navegador. Encerre o servidor com Ctrl+C. Também é possível abrir `site/index.html` diretamente. No Windows, se `python` não existir mas o Python estiver instalado com o launcher, substitua `python` por `py`.

O modo local usa apenas a biblioteca padrão. O comando `demo` gera os lotes, carrega SQLite e exporta os agregados. Executá-lo novamente não duplica registros. `data/warehouse.sqlite` guarda o banco local. `data/raw/` contém os lotes gerados; esses caminhos são ignorados pelo Git.

## Demonstre a carga em etapas

Use um banco separado para observar a evolução desde o início:

```powershell
python -m produtividade generate
python -m produtividade load --db data/etapas.sqlite --batch data/raw/001_base.json
python -m produtividade load --db data/etapas.sqlite --batch data/raw/001_base.json
python -m produtividade load --db data/etapas.sqlite --batch data/raw/002_incremental.json
python -m produtividade export --db data/etapas.sqlite
```

Na segunda carga aparece `already_loaded`. O lote incremental adiciona junho e corrige um fato de março em R$ 150. A versão antiga não sobrescreve a nova. Os testes verificam falha de lote inteiro quando há conflito ou chave órfã.

## PostgreSQL com Docker

Pré-requisitos adicionais: Docker com Compose e acesso para instalar `psycopg`. Use um banco demonstrativo, separado de qualquer ambiente empresarial.

1. Copie `.env.example` para `.env` e substitua a senha de exemplo por uma senha local exclusiva. O Compose lê esse arquivo automaticamente.
2. Suba o banco e instale o driver em um ambiente Python de sua escolha:

```powershell
docker compose up -d --wait
python -m pip install -r requirements-postgres.txt
```

3. Configure `DATABASE_URL` no terminal, usando a mesma senha do `.env`. Se a senha contiver caracteres reservados de URL, aplique percent-encoding. Exemplo de estrutura no PowerShell (substitua o marcador):

```powershell
$env:DATABASE_URL = 'postgresql://produtividade:SUA_SENHA@localhost:5432/produtividade'
python -m produtividade demo --postgres
```

No macOS/Linux, use `export DATABASE_URL='postgresql://produtividade:SUA_SENHA@localhost:5432/produtividade'`.

4. Crie as views e confira a reconciliação com o teste de integração:

```powershell
$env:PRODUTIVIDADE_TEST_POSTGRES = '1'
python -m unittest discover -s tests -v
```

O teste cria a view `vw_kpis_monthly` a partir de `sql/002_kpis_postgresql.sql` e compara os resultados com Python. Alternativamente, execute esse SQL no cliente PostgreSQL de sua preferência, depois da carga.

5. Para encerrar o banco mantendo os dados: `docker compose down`. O volume é persistente. A porta está limitada a localhost. O `.env` e a URL de conexão não devem ser versionados.

## Estrutura

```text
produtividade/             Gerador, conexão, ETL, agregação e interface de comando
sql/                   DDL e view analítica PostgreSQL
tests/                 Testes de integridade, reprocessamento e reconciliação
docs/                  Contratos, arquitetura, Power BI e roteiro da entrevista
reports/               JSON e CSV de indicadores sintéticos
site/                  Portfólio estático com filtros e materiais para download
.github/workflows/     Testes automáticos com SQLite e PostgreSQL
compose.yaml           PostgreSQL local
```

## Baixar o projeto

Repositório público: [Wenzel-Lopes/Produtividade](https://github.com/Wenzel-Lopes/Produtividade).

1. Baixe o código pelo botão **Code → Download ZIP**, ou clone com Git:

```powershell
git clone https://github.com/Wenzel-Lopes/Produtividade.git
cd Produtividade
python -m produtividade demo
python -m unittest discover -s tests -v
```

2. Consulte a aba **Actions** para acompanhar os testes automáticos de SQLite e PostgreSQL.
3. Use o README e a apresentação executiva para apresentar o case. Não é necessário ativar GitHub Pages. A pasta `site/` contém uma demonstração local opcional.
4. Leia `docs/entrevista.md` e descreva sua contribuição real nos projetos profissionais separadamente. Não inclua arquivos de ambientes empresariais.

## Leitura e limitações

- [Métricas e dicionário](metricas.md)
- [Arquitetura e escolhas](arquitetura.md)
- [Montagem no Power BI](power-bi.md)
- [Roteiro de entrevista](entrevista.md)
- [Resultados e validação](resultados.md)

O site já contém a amostra agregada para abrir imediatamente. Depois de mudanças no gerador/ETL, execute `demo`/`export` e atualize a apresentação e os arquivos de download antes de publicar. A apresentação é um retrato da versão entregue, não uma conexão ao vivo com o banco.

O projeto não inclui um PBIX pronto, agendamento de produção, CDC real ou regras completas de folha. A implementação é uma demonstração pequena e inspecionável, com suas limitações declaradas.
