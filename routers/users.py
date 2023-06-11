from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy import func
from auth.hash import auth_token

from base_models.responses.base_response import BaseResponse
from models import SessionLocal, get_db, Article, Artists

router = APIRouter(prefix="/v1/api")

@router.get("/user-profile",summary="Get user profile currently logged in")
async def user_profile(request: Request, db: SessionLocal = Depends(get_db)):
    authorization_header = request.headers.get("Authorization")

    user = None
    if authorization_header and authorization_header.startswith("Bearer "):
        token = authorization_header.split(" ")[1]
        user = auth_token(token, db, True)  # Perform token validation if token is provided


    if user is None:
        return {"error": "No token provided"}

    return BaseResponse(data=user.fixModelFields(False))

@router.post("/user-profile")
async def user_profile(request: Request, db: SessionLocal = Depends(get_db)):
    authorization_header = request.headers.get("Authorization")

    user = None
    if authorization_header and authorization_header.startswith("Bearer "):
        token = authorization_header.split(" ")[1]
        user = auth_token(token, db, True)  # Perform token validation if token is provided
