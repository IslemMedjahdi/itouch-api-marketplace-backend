"""empty message

Revision ID: 9b338f045bf4
Revises: 3a84eb47b87a
Create Date: 2024-03-25 19:46:47.173353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b338f045bf4'
down_revision = '3a84eb47b87a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bio', sa.String(length=1024), nullable=True))
        batch_op.add_column(sa.Column('phone_number', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('phone_number')
        batch_op.drop_column('bio')

    # ### end Alembic commands ###