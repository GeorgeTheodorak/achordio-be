from typing import Any
from pydantic import BaseModel, EmailStr
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse


class articleResponse(BaseModel):
    id: int
    title: str
    content: str
    thumbnail: str
    article_date: str
    description: str
