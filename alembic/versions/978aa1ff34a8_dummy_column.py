"""Initial schema

Revision ID: 978aa1ff34a8
Revises: 
Create Date: 2025-09-12 14:48:56.562979

Creates users, movies, reviews tables with indexes and FKs.
Includes a temporary movies.alembic_check column removed in next migration.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '978aa1ff34a8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_user_username', 'users', ['username'], unique=False)
    op.create_index('idx_user_email', 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Movies table (includes temporary 'alembic_check' column)
    op.create_table(
        'movies',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('genre', sa.String(), nullable=True),
        sa.Column('release_year', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('alembic_check', sa.Integer(), nullable=True),
    )
    op.create_index('idx_movie_title', 'movies', ['title'], unique=False)
    op.create_index('idx_movie_genre', 'movies', ['genre'], unique=False)
    op.create_index('idx_movie_year', 'movies', ['release_year'], unique=False)
    op.create_index(op.f('ix_movies_title'), 'movies', ['title'], unique=False)
    op.create_index(op.f('ix_movies_genre'), 'movies', ['genre'], unique=False)
    op.create_index(op.f('ix_movies_release_year'), 'movies', ['release_year'], unique=False)

    # Reviews table
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('movie_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_review_user', 'reviews', ['user_id'], unique=False)
    op.create_index('idx_review_movie', 'reviews', ['movie_id'], unique=False)
    op.create_index('idx_review_movie_user', 'reviews', ['movie_id', 'user_id'], unique=False)
    op.create_index('idx_review_rating', 'reviews', ['rating'], unique=False)
    op.create_index('idx_review_created', 'reviews', ['created_at'], unique=False)
    op.create_index(op.f('ix_reviews_user_id'), 'reviews', ['user_id'], unique=False)
    op.create_index(op.f('ix_reviews_movie_id'), 'reviews', ['movie_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_reviews_movie_id'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_user_id'), table_name='reviews')
    op.drop_index('idx_review_created', table_name='reviews')
    op.drop_index('idx_review_rating', table_name='reviews')
    op.drop_index('idx_review_movie_user', table_name='reviews')
    op.drop_index('idx_review_movie', table_name='reviews')
    op.drop_index('idx_review_user', table_name='reviews')
    op.drop_table('reviews')

    op.drop_index(op.f('ix_movies_release_year'), table_name='movies')
    op.drop_index(op.f('ix_movies_genre'), table_name='movies')
    op.drop_index(op.f('ix_movies_title'), table_name='movies')
    op.drop_index('idx_movie_year', table_name='movies')
    op.drop_index('idx_movie_genre', table_name='movies')
    op.drop_index('idx_movie_title', table_name='movies')
    op.drop_table('movies')

    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index('idx_user_email', table_name='users')
    op.drop_index('idx_user_username', table_name='users')
    op.drop_table('users')
