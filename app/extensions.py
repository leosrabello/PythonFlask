import sqlite3

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine

# Instâncias criadas "soltas" aqui e ligadas ao app dentro da factory (__init__.py).
# Isso evita import circular: models importam 'db' daqui, não do __init__.
db = SQLAlchemy()
migrate = Migrate()


@event.listens_for(Engine, "connect")
def _ativar_foreign_keys_sqlite(dbapi_connection, connection_record):
    """O SQLite ignora foreign keys por padrão; liga a checagem em cada conexão.

    Sem isto, o ON DELETE RESTRICT declarado no model não é respeitado e o banco
    deixa apagar um autor mesmo que ele tenha livros. O isinstance garante que
    isto só roda no SQLite — em MySQL não faz nada.
    """
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
