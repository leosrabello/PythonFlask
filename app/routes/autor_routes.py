"""Endpoints REST de Autor: CRUD sob /autores."""

from flask import Blueprint, jsonify, request

from ..errors import abortar, corpo_json_obrigatorio, inteiro_positivo_query
from ..schemas.autor_schema import autor_schema, autores_schema
from ..services import autor_service

bp = Blueprint("autores", __name__, url_prefix="/autores")


def _nao_encontrado(autor_id):
    abortar(f"Autor {autor_id} nao encontrado", 404)


@bp.get("", strict_slashes=False)
def listar_autores():
    page = inteiro_positivo_query("page", 1)
    per_page = inteiro_positivo_query("per_page", autor_service.PER_PAGE_PADRAO)

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


@bp.get("/<int:autor_id>")
def obter_autor(autor_id):
    autor = autor_service.obter(autor_id)
    if autor is None:
        _nao_encontrado(autor_id)
    return jsonify(autor_schema.dump(autor)), 200


@bp.post("", strict_slashes=False)
def criar_autor():
    dados = corpo_json_obrigatorio()
    validado = autor_schema.load(dados)

    autor = autor_service.criar(validado)
    return jsonify(autor_schema.dump(autor)), 201, {"Location": f"/autores/{autor.id}"}


@bp.put("/<int:autor_id>")
def substituir_autor(autor_id):
    autor = autor_service.obter(autor_id)
    if autor is None:
        _nao_encontrado(autor_id)

    dados = corpo_json_obrigatorio()
    validado = autor_schema.load(dados)

    autor = autor_service.atualizar(autor, validado, substituir=True)
    return jsonify(autor_schema.dump(autor)), 200


@bp.patch("/<int:autor_id>")
def atualizar_autor(autor_id):
    autor = autor_service.obter(autor_id)
    if autor is None:
        _nao_encontrado(autor_id)

    dados = corpo_json_obrigatorio()
    if not dados:
        abortar("Informe ao menos um campo para atualizar", 422)

    validado = autor_schema.load(dados, partial=True)

    autor = autor_service.atualizar(autor, validado, substituir=False)
    return jsonify(autor_schema.dump(autor)), 200


@bp.delete("/<int:autor_id>")
def remover_autor(autor_id):
    autor = autor_service.obter(autor_id)
    if autor is None:
        _nao_encontrado(autor_id)

    autor_service.remover(autor)
    return "", 204
