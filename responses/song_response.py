from typing import Any
from pydantic import BaseModel, EmailStr
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse


#singleton
class song_response(BaseModel):
    unique_identifier: str
    id: int
    name: str

#multiple
class songs_response(BaseModel):
    songs: song_response
    

