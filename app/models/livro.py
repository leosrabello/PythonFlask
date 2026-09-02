from ..extensions import db


class Livro(db.Model):
    """Livro pertencente a um autor."""

    __tablename__ = "livros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False, index=True)
    ano = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(80), nullable=False, index=True)
    autor_id = db.Column(
        db.Integer,
        db.ForeignKey("autores.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    autor = db.relationship("Autor", back_populates="livros")

    def __repr__(self):
        return f"<Livro {self.id} - {self.titulo}>"
