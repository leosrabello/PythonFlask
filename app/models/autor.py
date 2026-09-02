from datetime import datetime, timezone

from ..extensions import db


class Autor(db.Model):
    """Entidade A do trabalho: o autor de um ou mais livros (lado "1" do 1:N)."""

    __tablename__ = "autores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False, index=True)
    nacionalidade = db.Column(db.String(60), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Frente 3 (Livro) liga o outro lado do relacionamento 1:N descomentando a
    # linha abaixo, depois de criar app/models/livro.py com a FK autor_id:
    #
    # livros = db.relationship(
    #     "Livro", back_populates="autor", cascade="all, delete-orphan", lazy="selectin"
    # )

    def __repr__(self):
        return f"<Autor {self.id} - {self.nome}>"
