"""Endpoints REST de Livro: seis rotas CRUD sob /livros."""

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from ..schemas.livro_schema import livro_schema, livros_schema
from ..services import livro_service

bp = Blueprint("livros", __name__, url_prefix="/livros")


def _erro(mensagem, status, **extras):
    corpo = {"error": mensagem}
    corpo.update(extras)
    return jsonify(corpo), status


def _corpo_json():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return None, _erro("Corpo da requisicao deve ser um objeto JSON valido", 400)
    return dados, None


def _inteiro_da_query(nome, padrao, minimo=1):
    bruto = request.args.get(nome)
    if bruto is None or bruto == "":
        return padrao
    valor = int(bruto)
    if valor < minimo:
        raise ValueError
    return valor


def _nao_encontrado(livro_id):
    return _erro(f"Livro {livro_id} nao encontrado", 404)


def _autor_invalido(autor_id):
    return _erro(f"Autor {autor_id} nao encontrado", 422)


def _validar_autor(validado):
    from ..services import autor_service
    return autor_service.obter(validado["autor_id"]) is not None


@bp.get("", strict_slashes=False)
def listar_livros():
    try:
        page = _inteiro_da_query("page", 1)
        per_page = _inteiro_da_query("per_page", livro_service.PER_PAGE_PADRAO)
        autor_id = _inteiro_da_query("autor_id", None)
    except (TypeError, ValueError):
        return _erro("Parametros 'page', 'per_page' e 'autor_id' devem ser inteiros positivos", 400)

    paginacao = livro_service.listar(
        genero=request.args.get("genero"), autor_id=autor_id, page=page, per_page=per_page
    )
    return jsonify({
        "items": livros_schema.dump(paginacao.items),
        "page": paginacao.page,
        "per_page": paginacao.per_page,
        "total": paginacao.total,
        "pages": paginacao.pages,
    }), 200


@bp.get("/<int:livro_id>")
def obter_livro(livro_id):
    livro = livro_service.obter(livro_id)
    if livro is None:
        return _nao_encontrado(livro_id)
    return jsonify(livro_schema.dump(livro)), 200


@bp.post("", strict_slashes=False)
def criar_livro():
    dados, erro = _corpo_json()
    if erro:
        return erro
    try:
        validado = livro_schema.load(dados)
    except ValidationError as exc:
        return _erro("Dados invalidos", 422, detalhes=exc.messages)
    if not _validar_autor(validado):
        return _autor_invalido(validado["autor_id"])

    livro = livro_service.criar(validado)
    return jsonify(livro_schema.dump(livro)), 201, {"Location": f"/livros/{livro.id}"}


@bp.put("/<int:livro_id>")
def substituir_livro(livro_id):
    livro = livro_service.obter(livro_id)
    if livro is None:
        return _nao_encontrado(livro_id)
    dados, erro = _corpo_json()
    if erro:
        return erro
    try:
        validado = livro_schema.load(dados)
    except ValidationError as exc:
        return _erro("Dados invalidos", 422, detalhes=exc.messages)
    if not _validar_autor(validado):
        return _autor_invalido(validado["autor_id"])

    return jsonify(livro_schema.dump(livro_service.atualizar(livro, validado, substituir=True))), 200


@bp.patch("/<int:livro_id>")
def atualizar_livro(livro_id):
    livro = livro_service.obter(livro_id)
    if livro is None:
        return _nao_encontrado(livro_id)
    dados, erro = _corpo_json()
    if erro:
        return erro
    if not dados:
        return _erro("Informe ao menos um campo para atualizar", 422)
    try:
        validado = livro_schema.load(dados, partial=True)
    except ValidationError as exc:
        return _erro("Dados invalidos", 422, detalhes=exc.messages)
    if "autor_id" in validado and not _validar_autor(validado):
        return _autor_invalido(validado["autor_id"])

    return jsonify(livro_schema.dump(livro_service.atualizar(livro, validado))), 200


@bp.delete("/<int:livro_id>")
def remover_livro(livro_id):
    livro = livro_service.obter(livro_id)
    if livro is None:
        return _nao_encontrado(livro_id)
    livro_service.remover(livro)
    return "", 204
