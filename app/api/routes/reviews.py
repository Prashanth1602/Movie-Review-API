from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.models.auth import User
from app.schemas.reviews import ReviewCreate, ReviewOut, ReviewUpdate
from app.core.database import get_db
from app.api.deps import get_current_user
from app.services.reviews import ReviewService

router = APIRouter()
review_service = ReviewService()

@router.post("/movies/{movie_id}/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    movie_id: int,
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.create_review(db, movie_id, review_in, current_user.id)

@router.get("/movies/{movie_id}/reviews", response_model=List[ReviewOut])
def get_movie_reviews(
    movie_id: int, 
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 20
):
    return review_service.get_movie_reviews(db, movie_id, skip, limit)

@router.get("/reviews/{review_id}", response_model=ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    return review_service.get_review_by_id(db, review_id)

@router.put("/reviews/{review_id}", response_model=ReviewOut)
def update_review(
    review_id: int,
    review_in: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.update_review(db, review_id, review_in, current_user.id)

@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.delete_review(db, review_id, current_user.id)
