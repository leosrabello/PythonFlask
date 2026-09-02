# Biblioteca API

API RESTful em Flask para cadastro de autores e livros. Relacionamento: um
autor possui muitos livros.

## Stack

Flask, Flask-SQLAlchemy, Flask-Migrate, Marshmallow, python-dotenv e PyMySQL.

## Como rodar

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
flask db upgrade
python run.py
```

A API sobe em `http://127.0.0.1:5000`.

Teste rapido:

```bash
curl http://127.0.0.1:5000/health
```

Resposta:

```json
{ "status": "ok" }
```

## Configuracao

As variaveis ficam no arquivo `.env`.

```env
SECRET_KEY=troque-esta-chave
DATABASE_URL=sqlite:///biblioteca.db
```

Para MySQL, use uma URL no formato:

```env
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/biblioteca
```

## Estrutura

```text
.
|-- run.py
|-- requirements.txt
|-- Biblioteca_API.postman_collection.json
|-- migrations/
`-- app/
    |-- __init__.py
    |-- config.py
    |-- errors.py
    |-- extensions.py
    |-- models/
    |-- routes/
    |-- schemas/
    `-- services/
```

## Padrao de respostas

Respostas de sucesso devolvem o recurso solicitado ou uma lista paginada.
Respostas de erro sao sempre JSON e possuem ao menos a chave `error`.

```json
{ "error": "Mensagem do erro" }
```

Erros de validacao podem incluir `detalhes` com as mensagens do Marshmallow:

```json
{
  "error": "Dados invalidos",
  "detalhes": {
    "nome": ["Missing data for required field."]
  }
}
```

## Status codes

| Status | Uso |
| --- | --- |
| 200 | Consulta, listagem ou atualizacao feita com sucesso |
| 201 | Recurso criado com sucesso, com header `Location` |
| 204 | Recurso removido com sucesso, sem corpo na resposta |
| 400 | Requisicao malformada, corpo JSON invalido ou query string invalida |
| 404 | Rota ou recurso inexistente |
| 422 | JSON valido, mas com dados semanticamente invalidos |
| 500 | Erro interno inesperado, sem expor detalhes do servidor |

## Endpoints

### Health

| Metodo | Rota | Sucesso |
| --- | --- | --- |
| GET | `/health` | 200 |

### Autores

| Metodo | Rota | O que faz | Sucesso | Erros |
| --- | --- | --- | --- | --- |
| GET | `/autores` | Lista autores com filtros e paginacao | 200 | 400 |
| GET | `/autores/<id>` | Busca um autor por id | 200 | 404 |
| POST | `/autores` | Cria um autor | 201 | 400, 422 |
| PUT | `/autores/<id>` | Substitui um autor inteiro | 200 | 400, 404, 422 |
| PATCH | `/autores/<id>` | Atualiza campos enviados | 200 | 400, 404, 422 |
| DELETE | `/autores/<id>` | Remove um autor | 204 | 404 |

Campos de autor:

| Campo | Obrigatorio | Regra |
| --- | --- | --- |
| `nome` | Sim | Texto entre 2 e 120 caracteres |
| `nacionalidade` | Nao | Texto com ate 60 caracteres |
| `data_nascimento` | Nao | Data ISO `AAAA-MM-DD` |

Filtros de autores: `nome`, `nacionalidade`, `page` e `per_page`.

Exemplo:

```bash
curl -X POST http://127.0.0.1:5000/autores ^
  -H "Content-Type: application/json" ^
  -d "{\"nome\":\"Machado de Assis\",\"nacionalidade\":\"Brasileira\",\"data_nascimento\":\"1839-06-21\"}"
```

### Livros

| Metodo | Rota | O que faz | Sucesso | Erros |
| --- | --- | --- | --- | --- |
| GET | `/livros` | Lista livros com filtros e paginacao | 200 | 400 |
| GET | `/livros/<id>` | Busca um livro por id | 200 | 404 |
| POST | `/livros` | Cria um livro | 201 | 400, 422 |
| PUT | `/livros/<id>` | Substitui um livro inteiro | 200 | 400, 404, 422 |
| PATCH | `/livros/<id>` | Atualiza campos enviados | 200 | 400, 404, 422 |
| DELETE | `/livros/<id>` | Remove um livro | 204 | 404 |

Campos de livro:

| Campo | Obrigatorio | Regra |
| --- | --- | --- |
| `titulo` | Sim | Texto entre 1 e 200 caracteres |
| `ano` | Sim | Inteiro entre 1 e 9999 |
| `genero` | Sim | Texto entre 1 e 80 caracteres |
| `autor_id` | Sim | Inteiro positivo de um autor existente |

Filtros de livros: `genero`, `autor_id`, `page` e `per_page`.

Exemplo:

```bash
curl -X POST http://127.0.0.1:5000/livros ^
  -H "Content-Type: application/json" ^
  -d "{\"titulo\":\"Dom Casmurro\",\"ano\":1899,\"genero\":\"Romance\",\"autor_id\":1}"
```

## Colecao Postman

Arquivo: `Biblioteca_API.postman_collection.json`.

Como usar:

1. Importe o arquivo no Postman.
2. Confirme a variavel `base_url` como `http://127.0.0.1:5000`.
3. Rode a colecao em ordem.

A colecao cobre:

- `GET /health`
- CRUD completo de `/autores`
- CRUD completo de `/livros`
- 400 para query string/corpo invalido
- 404 para recurso e rota inexistentes
- 422 para validacao de payload e `autor_id` inexistente
- 204 sem corpo em deletes

## Conferencia final

Antes da entrega:

1. Instalar dependencias com `pip install -r requirements.txt`.
2. Rodar `flask db upgrade`.
3. Rodar `python run.py`.
4. Executar a colecao `Biblioteca_API.postman_collection.json`.
5. Conferir que todas as respostas de erro retornam JSON com a chave `error`.
