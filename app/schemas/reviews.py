from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    rating: float
    comment: Optional[str] = None

class ReviewOut(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: float
    comment: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ReviewUpdate(BaseModel):
    rating: Optional[float] = None
    comment: Optional[str] = None
