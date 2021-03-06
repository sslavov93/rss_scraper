"""empty message

Revision ID: 86fa213c8c6d
Revises: ff8ab16dc11a
Create Date: 2020-09-13 23:49:03.409314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86fa213c8c6d'
down_revision = 'ff8ab16dc11a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.VARCHAR(length=254), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
