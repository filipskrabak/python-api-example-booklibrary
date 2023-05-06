"""init

Revision ID: 7977543618c7
Revises:
Create Date: 2023-04-22 20:16:59.202779

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '7977543618c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('identification_num', sa.String(10), nullable=False, unique=True),
        sa.Column('email', sa.String(254), nullable=True, unique=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('surname', sa.Text(), nullable=False),
        sa.Column('birth_date', sa.Date, nullable=False),
        sa.Column('parent_id', sa.String(36), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_table(
        'cards',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('magstripe', sa.String(20), nullable=False),
        sa.Column('status', sa.Enum('active', 'inactive', 'expired', name='cardstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_table(
        'publications',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_table(
        'instances',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('type', sa.Enum('physical', 'ebook', 'audiobook', name='type'), nullable=False),
        sa.Column('publisher', sa.Text(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('available', 'reserved', name='status'), nullable=False),
        sa.Column('publication_id', UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_table(
        'authors',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('surname', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_table(
        'categories',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.Text(), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_table(
        'rentals',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('instance_id', UUID(as_uuid=True), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('active', 'overdue', 'returned', name='rentalstatus'), nullable=False),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_table(
        'reservations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('publication_id', UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )

    # Foreign keys
    op.create_foreign_key('fk_cards_user_id', 'cards', 'users', ['user_id'], ['id'])
    op.create_foreign_key('fk_instances_publication_id', 'instances', 'publications', ['publication_id'], ['id'])
    op.create_foreign_key('fk_rentals_user_id', 'rentals', 'users', ['user_id'], ['id'])
    op.create_foreign_key('fk_rentals_instance_id', 'rentals', 'instances', ['instance_id'], ['id'])
    op.create_foreign_key('fk_reservations_user_id', 'reservations', 'users', ['user_id'], ['id'])
    op.create_foreign_key('fk_reservations_publication_id', 'reservations', 'publications', ['publication_id'], ['id'])



def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('cards')
    op.drop_table('publications')
    op.drop_table('authors')
