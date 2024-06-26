"""change state lentgh

Revision ID: 19b727c50e65
Revises: 46c0999e44c6
Create Date: 2024-03-11 13:34:03.116441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19b727c50e65'
down_revision = '46c0999e44c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lead', schema=None) as batch_op:
        batch_op.alter_column('state',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=20),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lead', schema=None) as batch_op:
        batch_op.alter_column('state',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=10),
               existing_nullable=True)

    # ### end Alembic commands ###
