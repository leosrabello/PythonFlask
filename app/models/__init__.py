# Ponto central onde os models são importados para o Flask-Migrate
# conseguir "enxergar" as tabelas na hora de gerar as migrations.
#
# Frente 3  ->  from .livro import Livro
from .autor import Autor

__all__ = ["Autor"]
