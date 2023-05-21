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
from auth.jwt_generation import create_access_token, create_refresh_token
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
    
    # Return the created user data
    return {
        "token": create_access_token( form_data.email + form_data.user_name )
    }


@router.post('/login', summary="Create access and refresh tokens for models.py", response_model=auth_response.authResponse)
async def login(form_data: auth_response.authRequest, db: SessionLocal = Depends(get_db)):
    existing_user = db.query(User).filter(and_(User.email == form_data.email, User.user_name == form_data.user_name)).first()

    if existing_user == None :
        raise CustomException(
                    USER_DOSNT_EXISTS_EXCEPTION_CODE,
                    "User not found",
                    status.HTTP_403_FORBIDDEN
                )

    if verify_password() == False:
               
        raise CustomException(
            USER_WRONG_CREDENTIALS_EXCEPTION_CODE,
            "User not found",
            status.HTTP_403_FORBIDDEN
        )


    return {
        "token": create_access_token( User.email + User.user_name )
    }
# .
# ├── achordio-be
# │   ├── __init__.py
# │   ├── main.py
# │   ├── test.py
# │   └── routers
# │   │   ├── __init__.py
# │   │   ├── authentication.py
# │   │   └── global_data.py
# │   └── auth
# │       ├── __init__.py
# │       ├── jwt_generation.py
# │       └── hash.py
