from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.movies import Movie
from app.models.reviews import Review
from app.models.auth import User
from app.schemas.reviews import ReviewCreate, ReviewUpdate

class ReviewService:
    def create_review(self, db: Session, movie_id: int, review_in: ReviewCreate, current_user_id: int):
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        existing_review = db.query(Review).filter(
            Review.movie_id == movie_id, 
            Review.user_id == current_user_id
        ).first()
        if existing_review:
            raise HTTPException(
                status_code=400, 
                detail="You have already reviewed this movie. Update your existing review instead."
            )

        if review_in.rating < 0 or review_in.rating > 10:
            raise HTTPException(
                status_code=400, 
                detail="Rating must be between 0 and 10"
            )

        new_review = Review(
            user_id=current_user_id,
            movie_id=movie_id,
            rating=review_in.rating,
            comment=review_in.comment,
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review

    def get_movie_reviews(self, db: Session, movie_id: int, skip: int = 0, limit: int = 20):
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        return (
            db.query(Review)
            .filter(Review.movie_id == movie_id)
            .order_by(Review.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_review_by_id(self, db: Session, review_id: int):
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return review

    def update_review(self, db: Session, review_id: int, review_in: ReviewUpdate, current_user_id: int):
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        if review.user_id != current_user_id:
            raise HTTPException(
                status_code=403, 
                detail="You can only update your own reviews"
            )

        if review_in.rating is not None:
            if review_in.rating < 0 or review_in.rating > 10:
                raise HTTPException(
                    status_code=400, 
                    detail="Rating must be between 0 and 10"
                )
            review.rating = review_in.rating
        
        if review_in.comment is not None:
            review.comment = review_in.comment

        db.commit()
        db.refresh(review)
        return review

    def delete_review(self, db: Session, review_id: int, current_user_id: int):
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        if review.user_id != current_user_id:
            raise HTTPException(
                status_code=403, 
                detail="You can only delete your own reviews"
            )

        db.delete(review)
        db.commit()
