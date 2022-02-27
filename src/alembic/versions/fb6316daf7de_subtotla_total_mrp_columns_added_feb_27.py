"""subtotla, total, mrp - columns added (Feb 27)


Revision ID: fb6316daf7de
Revises: 7f6985709bc5
Create Date: 2022-02-27 16:00:38.731796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb6316daf7de'
down_revision = '7f6985709bc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoice_order_lines', sa.Column('mrp', sa.Float(), nullable=False))
    op.add_column('invoice_orders', sa.Column('sub_total', sa.Float(), nullable=False))
    op.add_column('invoice_orders', sa.Column('total_mrp', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('invoice_orders', 'total_mrp')
    op.drop_column('invoice_orders', 'sub_total')
    op.drop_column('invoice_order_lines', 'mrp')
    # ### end Alembic commands ###