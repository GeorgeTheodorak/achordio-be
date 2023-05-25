from typing import Any
from pydantic import BaseModel, EmailStr
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse


class authRequest(BaseModel):
    email: EmailStr
    password: str
