"""added assessment rate option to models

Revision ID: 9d0b8a77a95f
Revises: 4ece555d506d
Create Date: 2022-08-21 11:05:43.587862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9d0b8a77a95f"
down_revision = "4ece555d506d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "suggestion", sa.Column("assessment_rate", sa.Integer(), nullable=False)
    )
    op.drop_column("suggestion", "importance_rate")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "suggestion",
        sa.Column("importance_rate", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_column("suggestion", "assessment_rate")
    # ### end Alembic commands ###
