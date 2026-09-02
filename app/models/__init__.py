# Ponto central onde os models são importados para o Flask-Migrate
# conseguir "enxergar" as tabelas na hora de gerar as migrations.
#
# Frente 2  ->  from .autor import Autor
# Frente 3  ->  from .livro import Livro
#
# Enquanto ninguém adicionou model, o app sobe normal (só sem tabelas).
