def register_blueprints(app):
    """Registra as rotas de cada entidade. Cada frente pluga o seu blueprint aqui.

    Frente 2 (Autor):
        from .autor_routes import bp as autor_bp
        app.register_blueprint(autor_bp)

    Frente 3 (Livro):
        from .livro_routes import bp as livro_bp
        app.register_blueprint(livro_bp)
    """
    pass
