
from functools import wraps

from fastapi import Request

from auth.hash import auth_token


def validate_token(func):
    @wraps(func)
    async def wrapper(request: Request, db,user = None):
        authorization_header = request.headers.get("Authorization")

        if authorization_header and authorization_header.startswith("Bearer "):
            token = authorization_header.split(" ")[1]
            user = auth_token(token, db, False)  # Perform token validation if token is provided
        return await func(request, db, user=user) 
    
    return wrapper