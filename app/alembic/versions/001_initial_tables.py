"""Create initial tables

Revision ID: 001_initial_tables
Revises: 
Create Date: 2025-07-25 15:40:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Apply migration."""
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    
    # Create clothing_items table
    op.create_table(
        'clothing_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('brand', sa.String(length=100), nullable=True),
        sa.Column('color', sa.String(length=50), nullable=True),
        sa.Column('size', sa.String(length=20), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('ai_tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('user_tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_favorite', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clothing_items_category'), 'clothing_items', ['category'], unique=False)
    op.create_index(op.f('ix_clothing_items_color'), 'clothing_items', ['color'], unique=False)
    op.create_index(op.f('ix_clothing_items_user_id'), 'clothing_items', ['user_id'], unique=False)
    
    # Create style_dna table
    op.create_table(
        'style_dna',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('quiz_responses', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('style_profile', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('preferred_styles', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('preferred_colors', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('lifestyle_factors', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('version', sa.String(length=10), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_style_dna_user_id'), 'style_dna', ['user_id'], unique=False)
    
    # Create outfits table
    op.create_table(
        'outfits',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('occasion', sa.String(length=100), nullable=True),
        sa.Column('season', sa.String(length=50), nullable=True),
        sa.Column('clothing_item_ids', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('styling_tips', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('user_rating', sa.Integer(), nullable=True),
        sa.Column('is_favorite', sa.Boolean(), nullable=False),
        sa.Column('is_ai_generated', sa.Boolean(), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_outfits_occasion'), 'outfits', ['occasion'], unique=False)
    op.create_index(op.f('ix_outfits_user_id'), 'outfits', ['user_id'], unique=False)


def downgrade() -> None:
    """Rollback migration."""
    op.drop_index(op.f('ix_outfits_user_id'), table_name='outfits')
    op.drop_index(op.f('ix_outfits_occasion'), table_name='outfits')
    op.drop_table('outfits')
    
    op.drop_index(op.f('ix_style_dna_user_id'), table_name='style_dna')
    op.drop_table('style_dna')
    
    op.drop_index(op.f('ix_clothing_items_user_id'), table_name='clothing_items')
    op.drop_index(op.f('ix_clothing_items_color'), table_name='clothing_items')
    op.drop_index(op.f('ix_clothing_items_category'), table_name='clothing_items')
    op.drop_table('clothing_items')
    
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
