"""add memo

Revision ID: 33e5a24fc918
Revises: 837dd88358dc
Create Date: 2025-01-20 21:27:45.650333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33e5a24fc918'
down_revision: Union[str, None] = '837dd88358dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('memo', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('User', 'memo')
    # ### end Alembic commands ###
