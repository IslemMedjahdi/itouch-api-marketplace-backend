"""empty message

Revision ID: 86f6805f55d1
Revises: 9b338f045bf4
Create Date: 2024-03-26 20:25:44.633250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86f6805f55d1'
down_revision = '9b338f045bf4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('api_subscription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('api_subscription', schema=None) as batch_op:
        batch_op.drop_column('price')

    # ### end Alembic commands ###