"""ok

Revision ID: cd17245eb798
Revises: e1d458c25296
Create Date: 2023-06-09 22:46:25.488557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd17245eb798'
down_revision = 'e1d458c25296'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###
