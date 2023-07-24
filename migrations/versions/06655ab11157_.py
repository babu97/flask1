"""empty message

Revision ID: 06655ab11157
Revises: 54871f3604bf
Create Date: 2023-07-24 11:06:43.825851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06655ab11157'
down_revision = '54871f3604bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_posts_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_hash', sa.String(length=32), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('avatar_hash')

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_posts_timestamp'))

    op.drop_table('posts')
    # ### end Alembic commands ###
