from fastapi import FastAPI
from app.api.routes import auth, movies, reviews, search, admin
from app.api.external import routes as external_routes

from app.core.database import SessionLocal
from app.core.init_db import init_db
import logging

app = FastAPI()

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    init_db(db)
    db.close()

app.include_router(auth.router, prefix="/auth")
app.include_router(movies.router, prefix="/movies")
app.include_router(reviews.router)
app.include_router(search.router, prefix="/search")
app.include_router(admin.router, prefix="/movies")
app.include_router(external_routes.router, prefix="/api/external")

@app.get("/")
def hello():
    return {"message": "Hello, World....This is Prashanth Surapaneni!"}




