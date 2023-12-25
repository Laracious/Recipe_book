"""empty message

Revision ID: cc71f4acd794
Revises: 3c819b337479
Create Date: 2023-12-24 10:47:10.973657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc71f4acd794'
down_revision = '3c819b337479'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('video', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('user_rating', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('image', sa.String(length=255), nullable=True))
        batch_op.alter_column('ingredients',
               existing_type=sa.TEXT(),
               type_=sa.JSON(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.alter_column('ingredients',
               existing_type=sa.JSON(),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.drop_column('image')
        batch_op.drop_column('user_rating')
        batch_op.drop_column('video')

    # ### end Alembic commands ###