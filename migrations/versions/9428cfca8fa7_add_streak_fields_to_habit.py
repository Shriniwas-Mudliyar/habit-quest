"""add streak fields to habit

Revision ID: 9428cfca8fa7
Revises: e1209c035aa2
Create Date: 2026-02-03 05:25:45.632876
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9428cfca8fa7'
down_revision = 'e1209c035aa2'
branch_labels = None
depends_on = None


def upgrade():
    # 1️⃣ Add columns as nullable first
    with op.batch_alter_table('habit', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('current_streak', sa.Integer(), nullable=True)
        )
        batch_op.add_column(
            sa.Column('longest_streak', sa.Integer(), nullable=True)
        )
        batch_op.add_column(
            sa.Column('last_completed_date', sa.Date(), nullable=True)
        )

    # 2️⃣ Backfill existing rows
    op.execute("UPDATE habit SET current_streak = 0")
    op.execute("UPDATE habit SET longest_streak = 0")

    # 3️⃣ Enforce NOT NULL after backfill
    with op.batch_alter_table('habit', schema=None) as batch_op:
        batch_op.alter_column('current_streak', nullable=False)
        batch_op.alter_column('longest_streak', nullable=False)


def downgrade():
    with op.batch_alter_table('habit', schema=None) as batch_op:
        batch_op.drop_column('last_completed_date')
        batch_op.drop_column('longest_streak')
        batch_op.drop_column('current_streak')

