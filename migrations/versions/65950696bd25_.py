"""empty message

Revision ID: 65950696bd25
Revises: 
Create Date: 2021-06-19 22:01:10.391741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65950696bd25'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Drug',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(length=120), nullable=True),
    sa.Column('side_effects', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('price', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Pharmacy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('location_link', sa.String(length=500), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Drug_Availability',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('drug_id', sa.Integer(), nullable=False),
    sa.Column('pharmcy_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['drug_id'], ['Drug.id'], ),
    sa.ForeignKeyConstraint(['pharmcy_id'], ['Pharmacy.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Drug_Availability')
    op.drop_table('Pharmacy')
    op.drop_table('Drug')
    # ### end Alembic commands ###
