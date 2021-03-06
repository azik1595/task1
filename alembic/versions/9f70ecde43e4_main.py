"""main

Revision ID: 9f70ecde43e4
Revises: 
Create Date: 2022-02-14 04:30:16.035155

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9f70ecde43e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Event',
    sa.Column('id', mysql.INTEGER(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.Column('price', mysql.DOUBLE(precision=18, scale=2, asdecimal=True), nullable=False),
    sa.Column('date', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Persons',
    sa.Column('id', mysql.INTEGER(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('surname', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.Column('token', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Coupon',
    sa.Column('id', mysql.INTEGER(), nullable=False),
    sa.Column('event_id', mysql.INTEGER(), nullable=False),
    sa.Column('user_id', mysql.INTEGER(), nullable=False),
    sa.Column('hash', sa.String(length=250), nullable=False),
    sa.Column('comments', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['Event.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Persons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('servicelogs',
    sa.Column('id', mysql.INTEGER(), nullable=False),
    sa.Column('user_id', mysql.INTEGER(), nullable=True),
    sa.Column('ip_address', sa.Unicode(length=15), nullable=False),
    sa.Column('request_time', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Persons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('servicelogs')
    op.drop_table('Coupon')
    op.drop_table('Persons')
    op.drop_table('Event')
    # ### end Alembic commands ###
