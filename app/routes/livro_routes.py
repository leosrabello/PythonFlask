"""Endpoints REST de Livro: CRUD sob /livros."""

from flask import Blueprint, jsonify, request

from ..errors import abortar, corpo_json_obrigatorio, inteiro_positivo_query
from ..schemas.livro_schema import livro_schema, livros_schema
from ..services import autor_service, livro_service

bp = Blueprint("livros", __name__, url_prefix="/livros")


def _nao_encontrado(livro_id):
    abortar(f"Livro {livro_id} nao encontrado", 404)


def _validar_autor(autor_id):
    if autor_service.obter(autor_id) is None:
        abortar(f"Autor {autor_id} nao encontrado", 422)


@bp.get("", strict_slashes=False)
def listar_livros():
    page = inteiro_positivo_query("page", 1)
    per_page = inteiro_positivo_query("per_page", livro_service.PER_PAGE_PADRAO)
    autor_id = inteiro_positivo_query("autor_id", None)

    paginacao = livro_service.listar(
        genero=request.args.get("genero"),
        autor_id=autor_id,
        page=page,
        per_page=per_page,
    )
    return jsonify(
        {
            "items": livros_schema.dump(paginacao.items),
            "page": paginacao.page,
            "per_page": paginacao.per_page,
            "total": paginacao.total,
            "pages": paginacao.pages,
        }
    ), 200


@bp.get("/<int:livro_id>")
def obter_livro(livro_id):
    livro = livro_service.obter(livro_id)
    if livro is None:
        _nao_encontrado(livro_id)
    return jsonify(livro_schema.dump(livro)), 200


@bp.post("", strict_slashes=False)
def criar_livro():
    dados = corpo_json_obrigatorio()
    validado = livro_schema.load(dados)
    _validar_autor(validado["autor_id"])

    livro = livro_service.criar(validado)
    return jsonify(livro_schema.dump(livro)), 201, {"Location": f"/livros/{livro.id}"}


@bp.put("/<int:livro_id>")
def substituir_livro(livro_id):
    livro = livro_service.obter(livro_id)
    if livro is None:
        _nao_encontrado(livro_id)

    dados = corpo_json_obrigatorio()
    validado = livro_schema.load(dados)
    _validar_autor(validado["autor_id"])

    livro = livro_service.atualizar(livro, validado, substituir=True)
    return jsonify(livro_schema.dump(livro)), 200


@bp.patch("/<int:livro_id>")
def atualizar_livro(livro_id):
    livro = livro_service.obter(livro_id)
    if livro is None:
        _nao_encontrado(livro_id)

    dados = corpo_json_obrigatorio()
    if not dados:
        abortar("Informe ao menos um campo para atualizar", 422)

    validado = livro_schema.load(dados, partial=True)
    if "autor_id" in validado:
        _validar_autor(validado["autor_id"])

    livro = livro_service.atualizar(livro, validado, substituir=False)
    return jsonify(livro_schema.dump(livro)), 200


@bp.delete("/<int:livro_id>")
def remover_livro(livro_id):
    livro = livro_service.obter(livro_id)
    if livro is None:
        _nao_encontrado(livro_id)

    livro_service.remover(livro)
    return "", 204
