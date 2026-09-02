"""cria tabela livros com relacionamento com autores

Revision ID: 8c4f1a2b7d90
Revises: 35b85d7e93dc
Create Date: 2026-09-02
"""
from alembic import op
import sqlalchemy as sa


revision = "8c4f1a2b7d90"
down_revision = "35b85d7e93dc"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "livros",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("titulo", sa.String(length=200), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("genero", sa.String(length=80), nullable=False),
        sa.Column("autor_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["autor_id"], ["autores.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("livros", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_livros_titulo"), ["titulo"], unique=False)
        batch_op.create_index(batch_op.f("ix_livros_genero"), ["genero"], unique=False)
        batch_op.create_index(batch_op.f("ix_livros_autor_id"), ["autor_id"], unique=False)


def downgrade():
    with op.batch_alter_table("livros", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_livros_autor_id"))
        batch_op.drop_index(batch_op.f("ix_livros_genero"))
        batch_op.drop_index(batch_op.f("ix_livros_titulo"))
    op.drop_table("livros")
