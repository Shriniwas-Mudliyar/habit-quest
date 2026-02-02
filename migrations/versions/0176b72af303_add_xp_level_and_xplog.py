"""Add XPLog table (xp and level already exist)

Revision ID: 0176b72af303
Revises: 89a1c65fab6a
Create Date: 2026-02-02
"""

from alembic import op
import sqlalchemy as sa


revision = '0176b72af303'
down_revision = '89a1c65fab6a'
branch_labels = None
depends_on = None


def upgrade():
    # Create xp_log table only (xp/level already exist)
    op.create_table(
        'xp_log',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('habit_id', sa.Integer(), nullable=True),
        sa.Column('xp_amount', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.ForeignKeyConstraint(['habit_id'], ['habit.id']),
    )


def downgrade():
    op.drop_table('xp_log')

