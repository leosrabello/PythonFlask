from flask import Flask, jsonify

from .config import Config
from .extensions import db, migrate


def create_app(config_class=Config):
    """App factory: monta a aplicação e devolve pronta para rodar."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1) Liga as extensões ao app
    db.init_app(app)
    migrate.init_app(app, db)

    # 2) Importa os models para o Flask-Migrate enxergar as tabelas.
    #    (as Frentes 2 e 3 registram Autor e Livro dentro de app/models/__init__.py)
    from . import models  # noqa: F401

    # 3) Registra as rotas (blueprints). Cada frente pluga a sua aqui dentro.
    from .routes import register_blueprints
    register_blueprints(app)

    # 4) Handlers globais de erro (a Frente 4 completa este arquivo)
    from .errors import register_error_handlers
    register_error_handlers(app)

    # 5) Rota de saúde: confirma que o esqueleto está de pé
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app
