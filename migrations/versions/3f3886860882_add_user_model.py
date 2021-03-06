"""add User model

Revision ID: 3f3886860882
Revises: 
Create Date: 2022-06-26 15:23:01.671897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f3886860882'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cards_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=45), nullable=False),
    sa.Column('registered_on', sa.DateTime(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('public_id', sa.String(length=36), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('public_id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cards_user')
    # ### end Alembic commands ###
