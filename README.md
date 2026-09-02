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
    ├── schemas/            # validação de payload
    ├── services/           # regras de negócio
    └── routes/             # endpoints (blueprints)
```

## Divisão do trabalho

- **Frente 1 — Fundação/Infra:** este esqueleto (feito). App factory, config, extensões, migrate, health check.
- **Frente 2 — Autor:** `models/autor.py`, `schemas/`, `services/`, `routes/autor_routes.py` — CRUD em `/autores`.
- **Frente 3 — Livro:** `models/livro.py` (FK `autor_id`), migration do relacionamento, CRUD em `/livros`.
- **Frente 4 — Erros/entrega:** completar `errors.py`, status codes, coleção Postman/Insomnia, revisão final.

Onde cada frente pluga o código está marcado com comentários nos `__init__.py` de `models/` e `routes/`.
