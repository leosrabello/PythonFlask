from sqlalchemy import select

from ..extensions import db
from ..models.livro import Livro

CAMPOS_EDITAVEIS = ("titulo", "ano", "genero", "autor_id")
PER_PAGE_PADRAO = 10
PER_PAGE_MAXIMO = 100


def listar(genero=None, autor_id=None, page=1, per_page=PER_PAGE_PADRAO):
    stmt = select(Livro)

    if genero:
        stmt = stmt.where(Livro.genero.ilike(f"%{genero}%"))
    if autor_id is not None:
        stmt = stmt.where(Livro.autor_id == autor_id)

    stmt = stmt.order_by(Livro.titulo, Livro.id)
    return db.paginate(
        stmt,
        page=page,
        per_page=per_page,
        max_per_page=PER_PAGE_MAXIMO,
        error_out=False,
    )


def obter(livro_id):
    return db.session.get(Livro, livro_id)


def criar(dados):
    livro = Livro(**{campo: dados[campo] for campo in CAMPOS_EDITAVEIS})
    db.session.add(livro)
    db.session.commit()
    return livro


def atualizar(livro, dados, substituir=False):
    for campo in CAMPOS_EDITAVEIS:
        if campo in dados:
            setattr(livro, campo, dados[campo])
    db.session.commit()
    return livro


def remover(livro):
    db.session.delete(livro)
    db.session.commit()
