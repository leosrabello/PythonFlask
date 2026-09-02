# Ponto central onde os models são importados para o Flask-Migrate
# conseguir "enxergar" as tabelas na hora de gerar as migrations.
#
from .autor import Autor
from .livro import Livro

__all__ = ["Autor", "Livro"]
