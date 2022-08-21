"""phone_number field updated in order to prevent multiple registrations with one phonenum

Revision ID: 4ece555d506d
Revises: f5aaa2ba68e4
Create Date: 2022-08-19 10:19:39.271150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ece555d506d'
down_revision = 'f5aaa2ba68e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'administrator', ['phone_number'])
    op.create_unique_constraint(None, 'suggester', ['phone_number'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'suggester', type_='unique')
    op.drop_constraint(None, 'administrator', type_='unique')
    # ### end Alembic commands ###