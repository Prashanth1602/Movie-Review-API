from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.movies import MovieResponse
from app.core.database import get_db
from app.services.movies import MovieService

router = APIRouter()
movie_service = MovieService()

@router.get("/", response_model=List[MovieResponse])
def get_movies(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return movie_service.get_movies(db, skip, limit)

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    return movie_service.get_movie_by_id(db, movie_id)
