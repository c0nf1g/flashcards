"""removed unique for value in sentence

Revision ID: 953e8d8ec149
Revises: 7daf39ed5036
Create Date: 2023-02-04 16:14:05.710130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '953e8d8ec149'
down_revision = '7daf39ed5036'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('sentence_value_key', 'sentence', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('sentence_value_key', 'sentence', ['value'])
    # ### end Alembic commands ###
