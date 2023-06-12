from pydantic import BaseModel, EmailStr
class authRequest(BaseModel):
    email: EmailStr
    password: str


class validateToken(BaseModel):
    token: str
