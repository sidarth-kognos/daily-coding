"""02_salary_column_creation

Revision ID: bd9094356799
Revises: 295cc1a00619
Create Date: 2025-07-23 13:07:10.026643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd9094356799'
down_revision: Union[str, None] = '295cc1a00619'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('salary', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'salary')
    # ### end Alembic commands ###
