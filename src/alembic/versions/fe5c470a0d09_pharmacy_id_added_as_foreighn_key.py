"""pharmacy_id added as foreighn key

Revision ID: fe5c470a0d09
Revises: 03f469dd3206
Create Date: 2022-02-22 16:41:33.220363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe5c470a0d09'
down_revision = '03f469dd3206'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('pharmacy_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'customers', 'pharmacies', ['pharmacy_id'], ['id'], ondelete='CASCADE')
    op.add_column('grns', sa.Column('pharmacy_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'grns', 'pharmacies', ['pharmacy_id'], ['id'], ondelete='CASCADE')
    op.add_column('invoice_orders', sa.Column('pharmacy_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'invoice_orders', 'pharmacies', ['pharmacy_id'], ['id'], ondelete='CASCADE')
    op.add_column('purchase_orders', sa.Column('pharmacy_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'purchase_orders', 'pharmacies', ['pharmacy_id'], ['id'], ondelete='CASCADE')
    op.add_column('stocks', sa.Column('pharmacy_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'stocks', 'pharmacies', ['pharmacy_id'], ['id'], ondelete='CASCADE')
    op.add_column('trade_histories', sa.Column('pharmacy_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'trade_histories', 'pharmacies', ['pharmacy_id'], ['id'], ondelete='CASCADE')
    op.add_column('trades', sa.Column('pharmacy_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'trades', 'pharmacies', ['pharmacy_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'trades', type_='foreignkey')
    op.drop_column('trades', 'pharmacy_id')
    op.drop_constraint(None, 'trade_histories', type_='foreignkey')
    op.drop_column('trade_histories', 'pharmacy_id')
    op.drop_constraint(None, 'stocks', type_='foreignkey')
    op.drop_column('stocks', 'pharmacy_id')
    op.drop_constraint(None, 'purchase_orders', type_='foreignkey')
    op.drop_column('purchase_orders', 'pharmacy_id')
    op.drop_constraint(None, 'invoice_orders', type_='foreignkey')
    op.drop_column('invoice_orders', 'pharmacy_id')
    op.drop_constraint(None, 'grns', type_='foreignkey')
    op.drop_column('grns', 'pharmacy_id')
    op.drop_constraint(None, 'customers', type_='foreignkey')
    op.drop_column('customers', 'pharmacy_id')
    # ### end Alembic commands ###
