"""empty message

Revision ID: 06a4f25f835e
Revises: 47c8f9fccf79
Create Date: 2022-12-03 16:51:02.012883

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '06a4f25f835e'
down_revision = '47c8f9fccf79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('idUsuario', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombreUsuario', sa.String(length=250), nullable=True),
    sa.Column('correo', sa.String(length=250), nullable=False),
    sa.Column('contraseña', sa.String(length=250), nullable=False),
    sa.Column('edad', sa.Integer(), nullable=True),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('idUsuario'),
    sa.UniqueConstraint('correo')
    )
    op.drop_table('usuarios')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuarios',
    sa.Column('idUsuario', sa.INTEGER(), server_default=sa.text('nextval(\'"usuarios_idUsuario_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('nombreUsuario', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('correo', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('contraseña', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('edad', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('registered_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('admin', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('idUsuario', name='usuarios_pkey'),
    sa.UniqueConstraint('correo', name='usuarios_correo_key')
    )
    op.drop_table('usuario')
    # ### end Alembic commands ###
