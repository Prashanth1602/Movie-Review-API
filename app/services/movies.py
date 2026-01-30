from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.movies import Movie
from app.schemas.movies import MovieCreate


class MovieService:
    def get_movies(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Movie).offset(skip).limit(limit).all()

    def get_movie_by_id(self, db: Session, movie_id: int):
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie

    def create_movie(self, db: Session, movie: MovieCreate):
        new_movie = Movie(
            title=movie.title,
            description=movie.description,
            genre=movie.genre,
            release_year=movie.release_year
        )
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)
        return new_movie

    def update_movie(self, db: Session, movie_id: int, movie: MovieCreate):
        db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not db_movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        old_title = db_movie.title
        
        db_movie.title = movie.title
        db_movie.description = movie.description
        db_movie.genre = movie.genre
        db_movie.release_year = movie.release_year
        
        db.commit()
        db.refresh(db_movie)

        return db_movie

    def delete_movie(self, db: Session, movie_id: int):
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        movie_title = movie.title
        
        db.delete(movie)
        db.commit()
        

