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
from exceptions.generic_exceptions import USER_EXISTS_EXCEPTION_CODE,CustomException


router = APIRouter(prefix="/v1/api")


@router.post('/user-register', summary="Create new user", response_model=auth_response.authResponse)
async def register(form_data: auth_response.authRequest, db: SessionLocal = Depends(get_db)):
    
    existing_user = db.query(User).filter(and_(User.email == form_data.email, User.name == form_data.user_name)).first()

    if existing_user is not None:
        
        raise CustomException(
            USER_EXISTS_EXCEPTION_CODE,
            "User already exist",
            status.HTTP_403_FORBIDDEN
        )
    
    # Create a new User instance
    user = User(
        email=form_data.email,
        user_name=get_hashed_password(form_data.password)
    )
    
    # Add the user to the session
    db.add(user)
    
    # Commit the session to save the changes to the database
    db.commit()
    
    # Return the created user data
    return {
        "token": get_hashed_password(form_data.password)
    }


@router.post('/login', summary="Create access and refresh tokens for models.py", response_model=auth_response.authResponse)
async def login(form_data: auth_response.authRequest, db: SessionLocal = Depends(get_db)):
    # models.py = models.py.mial

    # if form_data.e !=  mail

    # user = db.get(form_data.username, None)
    # if models.py is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Incorrect email or password"
    #     )

    # hashed_pass = models.py['password']
    # if not verify_password(form_data.password, hashed_pass):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Incorrect email or password"
    #     )

    return {
        "access_token": create_access_token(form_data['email']),
        "refresh_token": create_refresh_token(form_data['email']),
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
