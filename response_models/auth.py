from typing import Any
from pydantic import BaseModel, EmailStr

class authResponse(BaseModel):
    token: str


class authRequest(BaseModel):
    email: EmailStr
    password: str