from datetime import timedelta
import time
from auth.jwt_generation import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import APIRouter, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy import and_
from starlette import status
from uuid import uuid4
from models import User
from models import sessionmaker
from models import get_db
from models import SessionLocal
from starlette.responses import JSONResponse
from auth.hash import get_hashed_password
from auth.jwt_generation import create_access_token
from responses import auth_response
from exceptions.generic_exceptions import USER_EXISTS_EXCEPTION_CODE,CustomException,USER_DOSNT_EXISTS_EXCEPTION_CODE,USER_WRONG_CREDENTIALS_EXCEPTION_CODE
from auth.hash import verify_password

router = APIRouter(prefix="/v1/api")


@router.post('/user-register', summary="Create new user", response_model=auth_response.authResponse)
async def register(form_data: auth_response.authRequest, db: SessionLocal = Depends(get_db)):
    
    existing_user = db.query(User).filter(and_(User.email == form_data.email, User.user_name == form_data.user_name)).first()

    if existing_user is not None:
        
        raise CustomException(
            USER_EXISTS_EXCEPTION_CODE,
            "User already exist",
            status.HTTP_403_FORBIDDEN
        )
    
    # Create a new User instance
    user = User(
        email=form_data.email,
        user_name=form_data.user_name,
        password=get_hashed_password(form_data.password),
    )
    
    # Add the user to the session
    db.add(user)
    
    # Commit the session to save the changes to the database
    db.commit()
    

    # Generate the access token
    access_token_expires = timedelta(minutes=30)

    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )

    # Return the created user data
    return {
        "token": access_token
    }

@router.post('/login', summary="Create access and refresh tokens for models.py", response_model=auth_response.authResponse)
async def login(form_data: auth_response.authRequest, db: SessionLocal = Depends(get_db)):

    existing_user = db.query(User).filter(and_(User.email == form_data.email, User.user_name == form_data.user_name)).first()

    if existing_user is None:
        raise CustomException(
            USER_DOSNT_EXISTS_EXCEPTION_CODE,
            "User not found",
            status.HTTP_403_FORBIDDEN
        )

    print(f"pass: {form_data.password} : hashed pass: {existing_user.password}")

    if not verify_password(form_data.password, existing_user.password):
        raise CustomException(
            USER_WRONG_CREDENTIALS_EXCEPTION_CODE,
            "What password is this brother?",
            status.HTTP_403_FORBIDDEN
        )

    # Generate the access token
    access_token_expires = timedelta(minutes=30)

    access_token = create_access_token(
        data={"sub": existing_user.user_name}, expires_delta=access_token_expires
    )

    return {"token": access_token}
