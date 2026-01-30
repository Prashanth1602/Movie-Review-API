from pydantic import BaseModel, ConfigDict

class MovieSearchResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    genre : str | None = None
    release_year: int | None = None

    model_config = ConfigDict(from_attributes=True)