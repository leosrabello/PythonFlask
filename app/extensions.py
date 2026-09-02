from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instâncias criadas "soltas" aqui e ligadas ao app dentro da factory (__init__.py).
# Isso evita import circular: models importam 'db' daqui, não do __init__.
db = SQLAlchemy()
migrate = Migrate()
