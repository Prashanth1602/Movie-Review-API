from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func
from app.models.movies import Movie
from app.schemas.search import MovieSearchResponse


class SearchService:
    def search_movies(self, db: Session, q: str):
        ts_query = func.plainto_tsquery(q)

        results = db.query(
            Movie,
            func.coalesce(
                func.ts_rank_cd(Movie.search_vector, ts_query),
                func.similarity(Movie.title, q)
            ).label("score")
        ).filter(
            (Movie.search_vector.op('@@')(ts_query)) |
            (Movie.title.ilike(f"%{q}%")) |
            (func.similarity(Movie.title, q) > 0.2)
        ).order_by(
            func.coalesce(
                func.ts_rank_cd(Movie.search_vector, ts_query),
                func.similarity(Movie.title, q)
            ).desc()
        ).all()

        if not results:
            raise HTTPException(status_code=404, detail="No movies found matching")

        movies =  [r[0] for r in results]

        return movies
