from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.models.auth import User
from app.schemas.movies import MovieCreate, MovieResponse
from app.core.database import get_db
from app.api.deps import require_role
from app.services.movies import MovieService

router = APIRouter()
movie_service = MovieService()

@router.post("/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie: MovieCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_role("admin"))
):
    return movie_service.create_movie(db, movie)

@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int, 
    movie: MovieCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    return movie_service.update_movie(db, movie_id, movie)

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    movie_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    return movie_service.delete_movie(db, movie_id)
