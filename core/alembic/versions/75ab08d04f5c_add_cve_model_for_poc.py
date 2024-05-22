"""add cve model for poc

Revision ID: 75ab08d04f5c
Revises: 59a69392477f
Create Date: 2024-05-22 08:50:01.023789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
import sqlalchemy_utils.types.url


# revision identifiers, used by Alembic.
revision: str = '75ab08d04f5c'
down_revision: Union[str, None] = '59a69392477f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cves',
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('hash_sum', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('cve_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('pocs', sa.ARRAY(sqlalchemy_utils.types.url.URLType()), nullable=True),
    sa.Column('references', sa.ARRAY(sqlalchemy_utils.types.url.URLType()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cves_created_at'), 'cves', ['created_at'], unique=False)
    op.create_index(op.f('ix_cves_hash_sum'), 'cves', ['hash_sum'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cves_hash_sum'), table_name='cves')
    op.drop_index(op.f('ix_cves_created_at'), table_name='cves')
    op.drop_table('cves')
    # ### end Alembic commands ###
