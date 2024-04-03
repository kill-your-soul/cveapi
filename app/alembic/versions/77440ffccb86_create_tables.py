"""Create tables

Revision ID: 77440ffccb86
Revises: 
Create Date: 2024-04-03 18:43:37.675854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = '77440ffccb86'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bdus',
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('bdu_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'bdu_id')
    )
    op.create_index(op.f('ix_bdus_created_at'), 'bdus', ['created_at'], unique=False)
    op.create_table('cwes',
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('cwe_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cwes_created_at'), 'cwes', ['created_at'], unique=False)
    op.create_index(op.f('ix_cwes_cwe_id'), 'cwes', ['cwe_id'], unique=False)
    op.create_table('cves',
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('cve_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('json', sa.JSON(), nullable=True),
    sa.Column('vendors', sa.JSON(), nullable=True),
    sa.Column('cwes', sa.JSON(), nullable=True),
    sa.Column('summary', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('cvss2', sa.Float(), nullable=True),
    sa.Column('cvss3', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cves_created_at'), 'cves', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cves_created_at'), table_name='cves')
    op.drop_table('cves')
    op.drop_index(op.f('ix_cwes_cwe_id'), table_name='cwes')
    op.drop_index(op.f('ix_cwes_created_at'), table_name='cwes')
    op.drop_table('cwes')
    op.drop_index(op.f('ix_bdus_created_at'), table_name='bdus')
    op.drop_table('bdus')
    # ### end Alembic commands ###
