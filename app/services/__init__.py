# Camada de servico: regras de negocio e acesso ao banco.
# As rotas chamam os services; os services falam com os models.
#
# Frente 3  ->  livro_service.py
from . import autor_service

__all__ = ["autor_service"]
