"""Camada de serviço de Autor: regras de negócio e acesso ao banco.

As rotas não falam com o SQLAlchemy diretamente — elas chamam estas funções.
Nada aqui sabe o que é HTTP: quem não existe volta ``None`` e quem chamou
decide qual status code usar.
"""

from sqlalchemy import select

from ..extensions import db
from ..models.autor import Autor

# Campos que o cliente pode gravar (id e criado_em são do servidor).
CAMPOS_EDITAVEIS = ("nome", "nacionalidade", "data_nascimento")

PER_PAGE_PADRAO = 10
PER_PAGE_MAXIMO = 100


def listar(nome=None, nacionalidade=None, page=1, per_page=PER_PAGE_PADRAO):
    """Lista autores com filtro simples por nome/nacionalidade e paginação.

    Devolve o objeto de paginação do Flask-SQLAlchemy (tem .items, .total, .pages).
    """
    stmt = select(Autor)

    if nome:
        stmt = stmt.where(Autor.nome.ilike(f"%{nome}%"))
    if nacionalidade:
        stmt = stmt.where(Autor.nacionalidade.ilike(f"%{nacionalidade}%"))

    stmt = stmt.order_by(Autor.nome)

    return db.paginate(
        stmt,
        page=page,
        per_page=per_page,
        max_per_page=PER_PAGE_MAXIMO,
        error_out=False,  # página fora do intervalo volta lista vazia, não 404
    )


def obter(autor_id):
    """Busca um autor pelo id. Devolve None se não existir."""
    return db.session.get(Autor, autor_id)


def criar(dados):
    """Cria um autor a partir do dicionário já validado pelo schema."""
    autor = Autor(**{campo: dados.get(campo) for campo in CAMPOS_EDITAVEIS})
    db.session.add(autor)
    db.session.commit()
    return autor


def atualizar(autor, dados, substituir=False):
    """Atualiza um autor já existente.

    ``substituir=True`` é o PUT: os campos opcionais que não vieram no corpo
    são zerados, porque o PUT troca o recurso inteiro.
    ``substituir=False`` é o PATCH: só mexe no que foi enviado.
    """
    for campo in CAMPOS_EDITAVEIS:
        if campo in dados:
            setattr(autor, campo, dados[campo])
        elif substituir:
            setattr(autor, campo, None)

    db.session.commit()
    return autor


def remover(autor):
    """Apaga o autor.

    Frente 3: quando Livro existir, decidir aqui o que fazer com os livros do
    autor (apagar junto via cascade, ou barrar a exclusão se houver livros).
    """
    db.session.delete(autor)
    db.session.commit()
