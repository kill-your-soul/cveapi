"""add hash_sum to models

Revision ID: 59a69392477f
Revises: 3fe71999c7f9
Create Date: 2024-04-04 22:18:38.483140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = '59a69392477f'
down_revision: Union[str, None] = '3fe71999c7f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bdus', sa.Column('hash_sum', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.create_index(op.f('ix_bdus_hash_sum'), 'bdus', ['hash_sum'], unique=True)
    op.add_column('cwes', sa.Column('hash_sum', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.create_index(op.f('ix_cwes_hash_sum'), 'cwes', ['hash_sum'], unique=True)
    op.add_column('nvds', sa.Column('hash_sum', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.drop_index('ix_cves_created_at', table_name='nvds')
    op.create_index(op.f('ix_nvds_created_at'), 'nvds', ['created_at'], unique=False)
    op.create_index(op.f('ix_nvds_hash_sum'), 'nvds', ['hash_sum'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_nvds_hash_sum'), table_name='nvds')
    op.drop_index(op.f('ix_nvds_created_at'), table_name='nvds')
    op.create_index('ix_cves_created_at', 'nvds', ['created_at'], unique=False)
    op.drop_column('nvds', 'hash_sum')
    op.drop_index(op.f('ix_cwes_hash_sum'), table_name='cwes')
    op.drop_column('cwes', 'hash_sum')
    op.drop_index(op.f('ix_bdus_hash_sum'), table_name='bdus')
    op.drop_column('bdus', 'hash_sum')
    # ### end Alembic commands ###
