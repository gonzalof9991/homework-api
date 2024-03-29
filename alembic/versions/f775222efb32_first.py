"""First

Revision ID: f775222efb32
Revises: 
Create Date: 2024-03-04 17:13:47.766424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f775222efb32'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('type', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('history_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_tasks_type'), 'tasks', ['type'], unique=False)
    op.drop_constraint('tasks_owner_id_fkey', 'tasks', type_='foreignkey')
    op.create_foreign_key(None, 'tasks', 'histories', ['history_id'], ['id'])
    op.drop_column('tasks', 'owner_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.create_foreign_key('tasks_owner_id_fkey', 'tasks', 'users', ['owner_id'], ['id'])
    op.drop_index(op.f('ix_tasks_type'), table_name='tasks')
    op.drop_column('tasks', 'history_id')
    op.drop_column('tasks', 'type')
    # ### end Alembic commands ###
