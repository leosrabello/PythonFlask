# Schemas de validação de payload (Marshmallow).
#
# Frente 3  ->  livro_schema.py  (valida entrada/saida de Livro)
from .autor_schema import AutorSchema, autor_schema, autores_schema

__all__ = ["AutorSchema", "autor_schema", "autores_schema"]
