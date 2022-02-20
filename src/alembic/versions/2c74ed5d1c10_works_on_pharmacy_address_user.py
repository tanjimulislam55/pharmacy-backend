"""works on Pharmacy, Address, User

Revision ID: 2c74ed5d1c10
Revises: a4b0cd0c4763
Create Date: 2022-02-19 15:58:54.702262

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2c74ed5d1c10'
down_revision = 'a4b0cd0c4763'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pharmacies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('trade_license', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('addresses', sa.Column('district', sa.String(length=50), nullable=True))
    op.add_column('addresses', sa.Column('sub_district', sa.String(length=50), nullable=True))
    op.drop_column('addresses', 'city')
    op.drop_column('addresses', 'flat')
    op.drop_column('addresses', 'house')
    op.drop_column('addresses', 'postal_code')
    op.drop_column('addresses', 'country')
    op.drop_column('addresses', 'road')
    op.drop_column('addresses', 'block')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('addresses', sa.Column('block', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('addresses', sa.Column('road', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('addresses', sa.Column('country', mysql.VARCHAR(length=30), nullable=True))
    op.add_column('addresses', sa.Column('postal_code', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('addresses', sa.Column('house', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('addresses', sa.Column('flat', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('addresses', sa.Column('city', mysql.VARCHAR(length=20), nullable=True))
    op.drop_column('addresses', 'sub_district')
    op.drop_column('addresses', 'district')
    op.drop_table('pharmacies')
    # ### end Alembic commands ###
