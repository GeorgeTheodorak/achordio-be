from functools import wraps

from fastapi import Request, Depends
from starlette import status

from auth.hash import auth_token
from exceptions.generic_exceptions import CustomException, USER_INVALID_TOKEN_TYPE, \
    USER_WRONG_CREDENTIALS_EXCEPTION_CODE
from models import SessionLocal, get_db


def validate_user(request: Request, db: SessionLocal = Depends(get_db), crashIfNotExists=True):
    authorization_header = request.headers.get("Authorization")

    if authorization_header and authorization_header.startswith("Bearer "):
        token = authorization_header.split(" ")[1]
        user = auth_token(token, db, True)  # Perform token validation if token is provided

        if user is None and crashIfNotExists:
            raise CustomException(
                USER_WRONG_CREDENTIALS_EXCEPTION_CODE,
                "INVALID USER TOKEN",
                status.HTTP_403_FORBIDDEN
            )

        return user

    return None
