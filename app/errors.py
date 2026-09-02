from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest, HTTPException


class APIError(Exception):
    """Erro esperado da API, sempre devolvido em JSON."""

    def __init__(self, mensagem, status_code=400, detalhes=None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status_code = status_code
        self.detalhes = detalhes


def resposta_erro(mensagem, status_code, detalhes=None):
    corpo = {"error": mensagem}
    if detalhes is not None:
        corpo["detalhes"] = detalhes
    return jsonify(corpo), status_code


def abortar(mensagem, status_code=400, detalhes=None):
    raise APIError(mensagem, status_code, detalhes)


def corpo_json_obrigatorio():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        abortar("Corpo da requisicao deve ser um objeto JSON valido", 400)
    return dados


def inteiro_positivo_query(nome, padrao, minimo=1):
    bruto = request.args.get(nome)
    if bruto is None or bruto == "":
        return padrao

    try:
        valor = int(bruto)
    except (TypeError, ValueError):
        abortar(f"Parametro '{nome}' deve ser um inteiro positivo", 400)

    if valor < minimo:
        abortar(f"Parametro '{nome}' deve ser um inteiro positivo", 400)
    return valor


def register_error_handlers(app):
    """Registra handlers globais que nunca devolvem pagina HTML do Flask."""

    @app.errorhandler(APIError)
    def erro_api(e):
        return resposta_erro(e.mensagem, e.status_code, e.detalhes)

    @app.errorhandler(ValidationError)
    def erro_validacao(e):
        return resposta_erro("Dados invalidos", 422, e.messages)

    @app.errorhandler(BadRequest)
    def erro_requisicao_invalida(e):
        return resposta_erro("Requisicao invalida", 400)

    @app.errorhandler(404)
    def nao_encontrado(e):
        return resposta_erro("Recurso nao encontrado", 404)

    @app.errorhandler(HTTPException)
    def erro_http(e):
        return resposta_erro(e.description or "Erro HTTP", e.code or 500)

    @app.errorhandler(SQLAlchemyError)
    def erro_banco(e):
        from .extensions import db

        db.session.rollback()
        app.logger.exception("Erro de banco de dados")
        return resposta_erro("Erro interno do servidor", 500)

    @app.errorhandler(Exception)
    def erro_interno(e):
        app.logger.exception("Erro inesperado")
        return resposta_erro("Erro interno do servidor", 500)
