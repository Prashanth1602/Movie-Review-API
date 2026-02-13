from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps_external import verify_api_key
from app.services.movies import MovieService
from app.services.search import SearchService
from app.schemas.movies import MovieResponse
from app.schemas.search import MovieSearchResponse

router = APIRouter()
movie_service = MovieService()
search_service = SearchService()

@router.get("/movies", response_model=List[MovieResponse], dependencies=[Depends(verify_api_key)])
def get_movies_external(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return movie_service.get_movies(db, skip, limit)

@router.get("/search", response_model=List[MovieSearchResponse], dependencies=[Depends(verify_api_key)])
def search_movies_external(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    return search_service.search_movies(db, q)
