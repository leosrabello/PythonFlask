# Biblioteca API

API RESTful em Flask — tema **Biblioteca**. Entidades: **Autor** (1:N) **Livro**.

## Stack
Flask · Flask-SQLAlchemy · Flask-Migrate · Marshmallow · python-dotenv

## Como rodar

```bash
# 1. criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. instalar dependências
pip install -r requirements.txt

# 3. configurar variáveis de ambiente
cp .env.example .env            # ajuste SECRET_KEY e DATABASE_URL se quiser

# 4. subir o banco (depois que os models existirem)
flask db migrate -m "cria tabelas autor e livro"
flask db upgrade

# 5. rodar
python run.py                   # http://127.0.0.1:5000
```

Teste rápido: `GET http://127.0.0.1:5000/health` → `{"status": "ok"}`

## Estrutura

```
biblioteca-api/
├── run.py                  # ponto de entrada
├── requirements.txt
├── .env.example
├── migrations/             # controle de versão do banco (Flask-Migrate)
└── app/
    ├── __init__.py         # app factory
    ├── config.py           # configuração via .env
    ├── extensions.py       # instâncias db e migrate
    ├── errors.py           # handlers globais de erro (Frente 4)
    ├── models/             # entidades / ORM
    │   └── autor.py        # Frente 2
    ├── schemas/            # validação de payload
    │   └── autor_schema.py # Frente 2
    ├── services/           # regras de negócio
    │   └── autor_service.py# Frente 2
    └── routes/             # endpoints (blueprints)
        └── autor_routes.py # Frente 2
```

## Endpoints

### Autor — `/autores` (Frente 2)

| Método | Rota             | O que faz                                   | Sucesso | Erros            |
|--------|------------------|---------------------------------------------|---------|------------------|
| GET    | `/autores`       | Lista com filtro e paginação                | 200     | 400              |
| GET    | `/autores/<id>`  | Busca um autor                              | 200     | 404              |
| POST   | `/autores`       | Cria (devolve header `Location`)            | 201     | 400, 422         |
| PUT    | `/autores/<id>`  | Substitui o recurso inteiro                 | 200     | 400, 404, 422    |
| PATCH  | `/autores/<id>`  | Atualiza só os campos enviados              | 200     | 400, 404, 422    |
| DELETE | `/autores/<id>`  | Remove (sem corpo na resposta)              | 204     | 404              |

**Campos:** `nome` (obrigatório, 2–120 caracteres), `nacionalidade` (opcional, até 60),
`data_nascimento` (opcional, ISO `AAAA-MM-DD`). `id` e `criado_em` são gerados pelo servidor.

**Filtros da listagem:** `?nome=` e `?nacionalidade=` (busca parcial, ignora maiúsculas),
`?page=` (padrão 1) e `?per_page=` (padrão 10, máximo 100).

```bash
curl -X POST http://127.0.0.1:5000/autores -H "Content-Type: application/json" -d "{\"nome\": \"Machado de Assis\", \"nacionalidade\": \"Brasileira\", \"data_nascimento\": \"1839-06-21\"}"
```

```bash
curl "http://127.0.0.1:5000/autores?nome=machado&page=1&per_page=10"
```

Resposta da lista:

```json
{ "items": [ { "id": 1, "nome": "Machado de Assis", "nacionalidade": "Brasileira",
               "data_nascimento": "1839-06-21", "criado_em": "2026-09-02T12:57:59" } ],
  "page": 1, "per_page": 10, "total": 1, "pages": 1 }
```

Erro de validação (422) — campo desconhecido também é recusado:

```json
{ "error": "Dados invalidos", "detalhes": { "nome": ["Missing data for required field."] } }
```

### Livro — `/livros` (Frente 3)

A definir pela Frente 3, seguindo exatamente o mesmo padrão de rota e de resposta.

## Divisão do trabalho

- **Frente 1 — Fundação/Infra:** este esqueleto (feito). App factory, config, extensões, migrate, health check.
- **Frente 2 — Autor:** `models/autor.py`, `schemas/autor_schema.py`, `services/autor_service.py`, `routes/autor_routes.py` — CRUD em `/autores` (feito).
- **Frente 3 — Livro:** `models/livro.py` (FK `autor_id`), migration do relacionamento, CRUD em `/livros`.
- **Frente 4 — Erros/entrega:** completar `errors.py`, status codes, coleção Postman/Insomnia, revisão final.

Onde cada frente pluga o código está marcado com comentários nos `__init__.py` de `models/` e `routes/`.
