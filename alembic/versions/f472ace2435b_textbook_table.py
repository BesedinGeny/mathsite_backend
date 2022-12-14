"""textbook table

Revision ID: f472ace2435b
Revises: af224591f223
Create Date: 2022-09-01 17:10:32.121006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f472ace2435b'
down_revision = 'af224591f223'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('textbook',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('school_class', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('slug', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='data',
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('textbook', schema='data')
    # ### end Alembic commands ###
