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

    livros = db.relationship(
        "Livro", back_populates="autor", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self):
        return f"<Autor {self.id} - {self.nome}>"
