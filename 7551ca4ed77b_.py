"""empty message

Revision ID: 7551ca4ed77b
Revises: 
Create Date: 2020-12-02 22:14:27.199539

"""
from alembic import op
import sqlalchemy as sa
import sys
sys.path.insert(1, 'C:/Users/iryna/PycharmProjects/flproj/models.py')
import models


# revision identifiers, used by Alembic.
revision = '7551ca4ed77b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Car',
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('carId', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('carId')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Text(), nullable=True),
    sa.Column('firstName', sa.Text(), nullable=True),
    sa.Column('lastName', sa.Text(), nullable=True),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('password', sa.Text(), nullable=True),
    sa.Column('phone', sa.Text(), nullable=True),
    sa.Column('accessLevel', sa.Enum('admin', 'passenger', name='User_access'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('carId', sa.Integer(), nullable=True),
    sa.Column('shipDate', sa.Date(), nullable=True),
    sa.Column('returnDate', sa.Date(), nullable=True),
    sa.Column('usedId', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('placed', 'approved', 'delivered', name='Order_status'), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['carId'], ['Car.carId'], ),
    sa.ForeignKeyConstraint(['usedId'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Order')
    op.drop_table('User')
    op.drop_table('Car')
    # ### end Alembic commands ###
