# Projeto de Solicitações de Processos Jurídicos

## Descrição

Este projeto consiste em um sistema de gerenciamento de solicitações de processos jurídicos, permitindo o cadastro e consulta dos dados do processo.
A API permite o cadastro e a busca dos dados de um processo em todos os graus dos Tribunais de Justiça de Alagoas (TJAL) e do Ceará (TJCE), os dados são coletados através de um crawler.

### Tecnologias Usadas
- Python
- Flask
- SQLAlchemy
- MySQL Workbench
- Scrapy
- Schedule

## Instalação

1. Clone o repositório: `git clone https://github.com/keilaviana/TJ-Processos`
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure a conexão com o banco de dados em `app\__init__.py`

## Uso
1. Execute o script: : `python create_db.py`, para criação do schema *db_solicitacoes* e da tabela *solicitacoes*;
2. Execute o Schedule: `python app.py`, ele que irá orquestrar a execução o aplicativo Flask e a solicitação do JOB;
    - Aplicativo Flask: O aplicativo Flask fornece duas rotas para interagir com solicitações de processos judiciais. Uma rota é responsável por cadastrar novos números de processo, enquanto a outra rota lê informações dos processos cadastrados.
    - JOB: É um script Python (`processamento.py`) que executa um job e processa solicitações judiciais pendentes. Ele interage com um banco de dados, consulta solicitações marcadas como 'SOLICITADA' e executa web scraping com base no número do processo e no estado a que pertence. Os resultados são armazenados no banco de dados.
3. Acesse `http://127.0.0.1:5000` no navegador para interagir com as rotas.

## Rotas
Rotas da API:
| Método | ROTA | Descrição |
|---|---|---|
| `GET` | `/ler-processo/<numero>`| Retorna informações da solicitação. |
| `POST` | `/cadastrar-numero-processo` | Utilizado para criar uma nova solicitação. |

## Estrutura do Projeto


```dir
app/
┣ models/
┃ ┗ solicitacoes.py
┣ utils
┃ ┗ tj_crawler/
┃ ┃ ┗ tj_crawler/
┃ ┃ ┃ ┗ spiders
┃ ┃ ┃ ┃ ┣ tjal_scrapper_2.py
┃ ┃ ┃ ┃ ┣ tjal_scrapper.py
┃ ┃ ┃ ┃ ┣ tjce_scrapper_2.py
┃ ┃ ┃ ┃ ┗ tjce_scrapper.py
┃ ┣ __init__.py
┗ api.py
jobs/
┗ processamento.py
.gitignore
app.py
create_db.py
README.md
requirements.txt
```
## Autor

- Nome: [Keila Viana]
- GitHub: [https://github.com/keilaviana]
