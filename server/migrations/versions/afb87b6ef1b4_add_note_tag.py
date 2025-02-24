"""add Note, Tag

Revision ID: afb87b6ef1b4
Revises: 6b7d6c185a27
Create Date: 2025-01-22 14:40:14.305722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afb87b6ef1b4'
down_revision: Union[str, None] = '6b7d6c185a27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Note',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('content', sa.String(length=8), nullable=False),
    sa.Column('memo_date', sa.String(length=8), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Note_title'), 'Note', ['title'], unique=False)
    op.create_index(op.f('ix_Note_user_id'), 'Note', ['user_id'], unique=False)
    op.create_table('Tag',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Note_Tag',
    sa.Column('note_id', sa.String(length=36), nullable=True),
    sa.Column('tag_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['note_id'], ['Note.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['Tag.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Note_Tag')
    op.drop_table('Tag')
    op.drop_index(op.f('ix_Note_user_id'), table_name='Note')
    op.drop_index(op.f('ix_Note_title'), table_name='Note')
    op.drop_table('Note')
    # ### end Alembic commands ###
