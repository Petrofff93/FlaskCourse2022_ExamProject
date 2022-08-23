"""restoring db

Revision ID: 7bf3307bffcc
Revises: 9d0b8a77a95f
Create Date: 2022-08-23 13:52:44.067429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7bf3307bffcc"
down_revision = "9d0b8a77a95f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "administrator",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=30), nullable=False),
        sa.Column("last_name", sa.String(length=30), nullable=False),
        sa.Column("email", sa.String(length=80), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=20), nullable=False),
        sa.Column(
            "role", sa.Enum("admin", "base_user", name="usertype"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone_number"),
    )
    op.create_table(
        "suggester",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=30), nullable=False),
        sa.Column("last_name", sa.String(length=30), nullable=False),
        sa.Column("email", sa.String(length=80), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=20), nullable=False),
        sa.Column(
            "role", sa.Enum("admin", "base_user", name="usertype"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone_number"),
    )
    op.create_table(
        "suggestion",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("assessment_rate", sa.Integer(), nullable=False),
        sa.Column(
            "created_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "status",
            sa.Enum("pending", "accepted", "rejected", name="state"),
            nullable=False,
        ),
        sa.Column("course_certificate_url", sa.String(length=255), nullable=False),
        sa.Column("suggester_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["suggester_id"],
            ["suggester.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("suggestion")
    op.drop_table("suggester")
    op.drop_table("administrator")
    # ### end Alembic commands ###