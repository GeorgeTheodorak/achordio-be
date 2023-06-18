from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy import func
from starlette import status

from auth.hash import auth_token
from auth.user_validate import validate_user
from base_models.requests.auth_request import validateToken
from base_models.requests.user import userUpdateThumbnail

from base_models.responses.base_response import BaseResponse
from exceptions.generic_exceptions import CustomException, USER_ALREADY_VERIFIED
from helpers.image_helper import downscale_image
from models import SessionLocal, get_db, Article, Artists

router = APIRouter(prefix="/v1/api")


@router.get("/user-profile", summary="Get user profile currently logged in")
async def user_profile(request: Request, db: SessionLocal = Depends(get_db), user=Depends(validate_user)):
    return BaseResponse(data=user.fixModelFields(is_light_mode=False))


@router.post("/user-profile")
async def user_profile(request: Request, db: SessionLocal = Depends(get_db), user=Depends(validate_user)):
    authorization_header = request.headers.get("Authorization")

    user = None
    if authorization_header and authorization_header.startswith("Bearer "):
        token = authorization_header.split(" ")[1]
        user = auth_token(token, db, True)  # Perform token validation if token is provided


@router.post("/user-profile/thumbnail")
async def user_profile(form_data: userUpdateThumbnail,
                       request: Request,
                       db: SessionLocal = Depends(get_db),
                       user=Depends(validate_user)):
    pass
    image_source = form_data.thumbnail

    image_source = downscale_image(image_source, (256, 256))
