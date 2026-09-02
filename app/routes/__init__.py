def register_blueprints(app):
    """Registra as rotas de cada entidade. Cada frente pluga o seu blueprint aqui.

    """
    from .autor_routes import bp as autor_bp
    from .livro_routes import bp as livro_bp

    app.register_blueprint(autor_bp)
    app.register_blueprint(livro_bp)
