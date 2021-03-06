"""add delete

Revision ID: 31028fd4d1fd
Revises: 4d57c044ac6b
Create Date: 2018-01-13 11:24:07.685839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31028fd4d1fd'
down_revision = '4d57c044ac6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('isdeleted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'isdeleted')
    # ### end Alembic commands ###
