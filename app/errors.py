from flask import jsonify


def register_error_handlers(app):
    """Handlers globais de erro em JSON.

    Scaffold mínimo montado pela Frente 1. A Frente 4 expande aqui:
    tratar 400, 422 (validação), erros do Marshmallow/Pydantic, etc.,
    sempre no formato {"error": "mensagem descritiva"}.
    """

    @app.errorhandler(404)
    def nao_encontrado(e):
        return jsonify({"error": "Recurso nao encontrado"}), 404

    @app.errorhandler(500)
    def erro_interno(e):
        return jsonify({"error": "Erro interno do servidor"}), 500
