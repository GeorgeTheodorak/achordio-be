from datetime import timedelta
from functools import wraps
import random

from fastapi import APIRouter, Depends, status
from fastapi import Request
from fastapi.security import HTTPBearer

from auth.hash import auth_token
from auth.hash import get_hashed_password
from auth.hash import verify_password, generate_jwt_data_from_user_model
from auth.jwt_generation import create_access_token
from auth.user_validate import validate_user
from exceptions.generic_exceptions import USER_EXISTS_EXCEPTION_CODE, CustomException, \
    USER_DOES_NOT_EXISTS_EXCEPTION_CODE, \
    USER_WRONG_CREDENTIALS_EXCEPTION_CODE, USER_EXPIRED_TOKEN, USER_ALREADY_VERIFIED
from models import SessionLocal
from models import User
from models import get_db
from base_models.responses.auth_response import authResponse
from base_models.requests.auth_request import authRequest, validateToken

router = APIRouter(prefix="/v1/api")
security = HTTPBearer()

TOKEN_MINUTES = 360000


@router.get("/protected")
async def protected_route(request: Request, db: SessionLocal = Depends(get_db), User=None):
    user = validate_user(request, db, None, False)
    route_token = True
    if User is None:
        route_token = False

    return {
        "routeToken": route_token,
        "status": "good"
    }


@router.post('/user-register', summary="Create new user", response_model=authResponse)
async def register(form_data: authRequest, db: SessionLocal = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == form_data.email).first()

    if existing_user is not None:
        raise CustomException(
            USER_EXISTS_EXCEPTION_CODE,
            "User already exists",
            status.HTTP_403_FORBIDDEN
        )

    user_name_to_save = form_data.email.split("@")[0]
    tries = 0
    while tries < 10:
        tries += 1

        existing_user = db.query(User).filter(User.user_name == user_name_to_save).first()
        if existing_user is not None:
            user_name_to_save = f"{user_name_to_save}{random.randint(0, 9)}"
            continue

    # Create a new User instance
    user = User(
        email=form_data.email,
        user_name=user_name_to_save,
        password=get_hashed_password(form_data.password),
        user_visibility=1,
    )

    # Add the user to the session
    db.add(user)

    # Commit the session to save the changes to the database
    db.commit()

    # Generate the access token
    access_token_expires = timedelta(minutes=TOKEN_MINUTES)

    access_token = create_access_token(
        data=generate_jwt_data_from_user_model(user), expires_delta=access_token_expires
    )

    # Return the created user data
    return {
        "token": access_token
    }


@router.post('/login', summary="Create access and refresh tokens for models.py",
             response_model=authResponse)
async def login(form_data: authRequest, db: SessionLocal = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == form_data.email).first()

    if existing_user is None:
        raise CustomException(
            USER_DOES_NOT_EXISTS_EXCEPTION_CODE,
            "User not found",
            status.HTTP_403_FORBIDDEN
        )

    if not verify_password(form_data.password, existing_user.password):
        raise CustomException(
            USER_WRONG_CREDENTIALS_EXCEPTION_CODE,
            "What password is this brother?",
            status.HTTP_403_FORBIDDEN
        )

    # Generate the access token
    access_token_expires = timedelta(minutes=TOKEN_MINUTES)

    access_token = create_access_token(
        data=generate_jwt_data_from_user_model(existing_user), expires_delta=access_token_expires
    )

    return {"token": access_token}


@router.post("/verify_code")
async def verify_code(form_data: validateToken, request: Request, db: SessionLocal = Depends(get_db),
                      user=Depends(validate_user)):
    if not user:
        raise CustomException(
            USER_EXPIRED_TOKEN,
            "INVALID TOKEN",
            status.HTTP_403_FORBIDDEN
        )
    if user.is_verified:
        raise CustomException(
            USER_ALREADY_VERIFIED,
            "ALREADY VERIFIED",
            status.HTTP_403_FORBIDDEN
        )

    verificationTokenException = CustomException(
        USER_EXPIRED_TOKEN,
        "INVALID TOKEN",
        status.HTTP_403_FORBIDDEN
    )

    token = form_data.token

    if not token:
        raise verificationTokenException

    if user.verification_token != token:
        raise verificationTokenException

    user.is_verified = True

    db.add(user)
    db.commit()

    return {'status': "good"}
