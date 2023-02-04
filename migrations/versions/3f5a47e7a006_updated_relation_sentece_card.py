"""updated relation sentece card

Revision ID: 3f5a47e7a006
Revises: 23f1129e7a67
Create Date: 2023-02-04 13:07:44.159072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f5a47e7a006'
down_revision = '23f1129e7a67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('sentence_card_id_fkey', 'sentence', type_='foreignkey')
    op.create_foreign_key(None, 'sentence', 'card', ['card_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sentence', type_='foreignkey')
    op.create_foreign_key('sentence_card_id_fkey', 'sentence', 'card', ['card_id'], ['id'])
    # ### end Alembic commands ###
