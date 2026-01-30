from sqlalchemy import Column, Integer, String, DateTime, Index, FetchedValue
from sqlalchemy.dialects.postgresql import TSVECTOR
from datetime import datetime
from .base import Base

class Movie(Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    genre = Column(String, nullable=True, index=True)
    release_year = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    search_vector = Column(TSVECTOR, server_default=FetchedValue())

    __table_args__ = (
        Index('idx_movie_title', 'title'),
        Index('idx_movie_genre', 'genre'),
        Index('idx_movie_year', 'release_year'),
    )
