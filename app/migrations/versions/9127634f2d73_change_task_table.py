"""change task table

Revision ID: 9127634f2d73
Revises: 
Create Date: 2023-08-12 15:17:04.620733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9127634f2d73'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_get_content',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('statistic', sa.Boolean(), nullable=True),
    sa.Column('description', sa.Boolean(), nullable=True),
    sa.Column('comments', sa.Boolean(), nullable=True),
    sa.Column('tags', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('app_task_handler_explore',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('crawler_id', sa.Integer(), nullable=True),
    sa.Column('last_status', sa.String(), nullable=True),
    sa.Column('is_done', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('app_task_handler_tag',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('crawler_id', sa.Integer(), nullable=True),
    sa.Column('last_status', sa.String(), nullable=True),
    sa.Column('is_done', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('app_task_handler_username',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('crawler_id', sa.Integer(), nullable=True),
    sa.Column('last_status', sa.String(), nullable=True),
    sa.Column('is_done', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('app_requests_model_explore',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('task_handler_id', sa.Integer(), nullable=True),
    sa.Column('content_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['content_id'], ['app_get_content.id'], ),
    sa.ForeignKeyConstraint(['task_handler_id'], ['app_task_handler_explore.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('app_requests_model_search_tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('task_handler_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('content_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['content_id'], ['app_get_content.id'], ),
    sa.ForeignKeyConstraint(['task_handler_id'], ['app_task_handler_tag.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('app_requests_model_search_username',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('task_handler_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('content_id', sa.Integer(), autoincrement=True, nullable=True),
    sa.ForeignKeyConstraint(['content_id'], ['app_get_content.id'], ),
    sa.ForeignKeyConstraint(['task_handler_id'], ['app_task_handler_username.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('app_requests_model_search_username')
    op.drop_table('app_requests_model_search_tag')
    op.drop_table('app_requests_model_explore')
    op.drop_table('app_task_handler_username')
    op.drop_table('app_task_handler_tag')
    op.drop_table('app_task_handler_explore')
    op.drop_table('app_get_content')
    # ### end Alembic commands ###
