"""empty message

Revision ID: 86f65a33b37a
Revises: 099a686e6130
Create Date: 2020-06-12 19:43:53.901950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86f65a33b37a'
down_revision = '099a686e6130'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('sector', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('emissions', sa.Float(), nullable=True),
    sa.Column('reference', sa.String(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_emission_category'), 'emission', ['category'], unique=False)
    op.create_index(op.f('ix_emission_description'), 'emission', ['description'], unique=False)
    op.create_index(op.f('ix_emission_emissions'), 'emission', ['emissions'], unique=False)
    op.create_index(op.f('ix_emission_name'), 'emission', ['name'], unique=True)
    op.create_index(op.f('ix_emission_reference'), 'emission', ['reference'], unique=False)
    op.create_index(op.f('ix_emission_sector'), 'emission', ['sector'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_emission_sector'), table_name='emission')
    op.drop_index(op.f('ix_emission_reference'), table_name='emission')
    op.drop_index(op.f('ix_emission_name'), table_name='emission')
    op.drop_index(op.f('ix_emission_emissions'), table_name='emission')
    op.drop_index(op.f('ix_emission_description'), table_name='emission')
    op.drop_index(op.f('ix_emission_category'), table_name='emission')
    op.drop_table('emission')
    # ### end Alembic commands ###