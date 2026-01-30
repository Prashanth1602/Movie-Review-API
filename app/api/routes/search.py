from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.search import MovieSearchResponse
from app.core.database import get_db
from app.services.search import SearchService

router = APIRouter()
search_service = SearchService()

@router.get("/", response_model=List[MovieSearchResponse])
def search_movies(db: Session = Depends(get_db), q: str = Query(..., min_length=1)):
    return search_service.search_movies(db, q)