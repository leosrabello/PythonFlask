"""Endpoints REST de Autor — 6 rotas CRUD sob /autores.

Padrão de resposta combinado com o grupo:
  - sucesso  -> o próprio recurso (ou {"items": [...]} + metadados na lista)
  - erro     -> {"error": "mensagem"}  (validação também traz "detalhes")

Os status codes usados aqui: 200, 201, 204, 400, 404 e 422.
A Frente 4 pode migrar estes try/except para handlers globais em errors.py.
"""

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from ..schemas.autor_schema import autor_schema, autores_schema
from ..services import autor_service

bp = Blueprint("autores", __name__, url_prefix="/autores")


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _erro(mensagem, status, **extras):
    corpo = {"error": mensagem}
    corpo.update(extras)
    return jsonify(corpo), status


def _corpo_json():
    """Devolve (dados, None) ou (None, resposta_de_erro_400)."""
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return None, _erro("Corpo da requisicao deve ser um objeto JSON valido", 400)
    return dados, None


def _inteiro_da_query(nome, padrao, minimo=1):
    """Lê um inteiro da query string. Levanta ValueError se vier bobagem."""
    bruto = request.args.get(nome)
    if bruto is None or bruto == "":
        return padrao
    valor = int(bruto)  # ValueError sobe para quem chamou
    if valor < minimo:
        raise ValueError(f"{nome} deve ser maior ou igual a {minimo}")
    return valor


def _nao_encontrado(autor_id):
    return _erro(f"Autor {autor_id} nao encontrado", 404)


# --------------------------------------------------------------------------- #
# 1) GET /autores  -> lista com filtro e paginação
# --------------------------------------------------------------------------- #
@bp.get("", strict_slashes=False)
def listar_autores():
    try:
        page = _inteiro_da_query("page", 1)
        per_page = _inteiro_da_query("per_page", autor_service.PER_PAGE_PADRAO)
    except ValueError:
        return _erro("Parametros 'page' e 'per_page' devem ser inteiros positivos", 400)

    paginacao = autor_service.listar(
        nome=request.args.get("nome"),
        nacionalidade=request.args.get("nacionalidade"),
        page=page,
        per_page=per_page,
    )

    return jsonify(
        {
            "items": autores_schema.dump(paginacao.items),
            "page": paginacao.page,
            "per_page": paginacao.per_page,
            "total": paginacao.total,
            "pages": paginacao.pages,
        }
    ), 200


# --------------------------------------------------------------------------- #
# 2) GET /autores/<id>
# --------------------------------------------------------------------------- #
@bp.get("/<int:autor_id>")
def obter_autor(autor_id):
    autor = autor_service.obter(autor_id)
    if autor is None:
        return _nao_encontrado(autor_id)
    return jsonify(autor_schema.dump(autor)), 200


# --------------------------------------------------------------------------- #
# 3) POST /autores
# --------------------------------------------------------------------------- #
@bp.post("", strict_slashes=False)
def criar_autor():
    dados, erro = _corpo_json()
    if erro:
        return erro

    try:
        validado = autor_schema.load(dados)
    except ValidationError as exc:
        return _erro("Dados invalidos", 422, detalhes=exc.messages)

    autor = autor_service.criar(validado)
    corpo = autor_schema.dump(autor)
    return jsonify(corpo), 201, {"Location": f"/autores/{autor.id}"}


# --------------------------------------------------------------------------- #
# 4) PUT /autores/<id>  -> substitui o recurso inteiro
# --------------------------------------------------------------------------- #
@bp.put("/<int:autor_id>")
def substituir_autor(autor_id):
    autor = autor_service.obter(autor_id)
    if autor is None:
        return _nao_encontrado(autor_id)

    dados, erro = _corpo_json()
    if erro:
        return erro

    try:
        validado = autor_schema.load(dados)  # sem partial: 'nome' continua obrigatorio
    except ValidationError as exc:
        return _erro("Dados invalidos", 422, detalhes=exc.messages)

    autor = autor_service.atualizar(autor, validado, substituir=True)
    return jsonify(autor_schema.dump(autor)), 200


# --------------------------------------------------------------------------- #
# 5) PATCH /autores/<id>  -> atualiza só o que veio
# --------------------------------------------------------------------------- #
@bp.patch("/<int:autor_id>")
def atualizar_autor(autor_id):
    autor = autor_service.obter(autor_id)
    if autor is None:
        return _nao_encontrado(autor_id)

    dados, erro = _corpo_json()
    if erro:
        return erro
    if not dados:
        return _erro("Informe ao menos um campo para atualizar", 422)

    try:
        validado = autor_schema.load(dados, partial=True)
    except ValidationError as exc:
        return _erro("Dados invalidos", 422, detalhes=exc.messages)

    autor = autor_service.atualizar(autor, validado, substituir=False)
    return jsonify(autor_schema.dump(autor)), 200


# --------------------------------------------------------------------------- #
# 6) DELETE /autores/<id>
# --------------------------------------------------------------------------- #
@bp.delete("/<int:autor_id>")
def remover_autor(autor_id):
    autor = autor_service.obter(autor_id)
    if autor is None:
        return _nao_encontrado(autor_id)

    autor_service.remover(autor)
    return "", 204
