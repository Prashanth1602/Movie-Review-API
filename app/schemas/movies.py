from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None

class MovieResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
