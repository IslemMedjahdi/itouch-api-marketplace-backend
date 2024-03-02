"""empty message

Revision ID: 58826e8222ed
Revises: cda1af43fae5
Create Date: 2024-03-02 20:19:43.047609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58826e8222ed'
down_revision = 'cda1af43fae5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_plan',
    sa.Column('api_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('max_requests', sa.Integer(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['api_id'], ['api.id'], ),
    sa.PrimaryKeyConstraint('api_id', 'name')
    )
    op.drop_table('api_version_plan')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_version_plan',
    sa.Column('api_id', sa.INTEGER(), nullable=False),
    sa.Column('api_version', sa.VARCHAR(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), nullable=False),
    sa.Column('price', sa.INTEGER(), nullable=True),
    sa.Column('max_requests', sa.INTEGER(), nullable=True),
    sa.Column('duration', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['api_id'], ['api_version.api_id'], ),
    sa.ForeignKeyConstraint(['api_version'], ['api_version.version'], ),
    sa.PrimaryKeyConstraint('api_id', 'api_version', 'name')
    )
    op.drop_table('api_plan')
    # ### end Alembic commands ###