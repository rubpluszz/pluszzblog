"""add selectod post in post


Revision ID: 11e1b6543f0e
Revises: 9e3bb0b14b1f
Create Date: 2021-02-20 15:27:54.082855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11e1b6543f0e'
down_revision = '9e3bb0b14b1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('selected_posts', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'selected_posts')
    # ### end Alembic commands ###
