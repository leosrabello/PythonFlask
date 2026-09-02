import os
from dotenv import load_dotenv

# Carrega o arquivo .env para dentro das variáveis de ambiente
load_dotenv()


class Config:
    """Configurações da aplicação, lidas do ambiente (.env)."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-inseguro-troque")

    # Conexão do banco. Padrão SQLite (arquivo local); troque no .env para MySQL:
    # mysql+pymysql://usuario:senha@localhost:3306/biblioteca
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///biblioteca.db")

    # Desliga um recurso pesado do SQLAlchemy que não usamos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
