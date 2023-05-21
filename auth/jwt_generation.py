import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

import secrets

# Generate a random string with 64 bytes (512 bits) of entropy
JWT_SECRET_KEY = secrets.token_urlsafe(64)

# Generate a random string with 32 bytes (256 bits) of entropy
JWT_REFRESH_SECRET_KEY = secrets.token_urlsafe(32)

ACCESS_TOKEN_EXPIRE_MINUTES = 3600000
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"


def return_auth(subject: Union[str, Any], expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    return return_auth(subject, expires_delta)

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    return return_auth(subject, expires_delta)

