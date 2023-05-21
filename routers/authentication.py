from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import and_
from starlette import status
from models import User
from models import get_db
from models import SessionLocal
from auth.hash import get_hashed_password
from auth.jwt_generation import create_access_token
from responses import auth_response
from exceptions.generic_exceptions import USER_EXISTS_EXCEPTION_CODE,CustomException,USER_DOSNT_EXISTS_EXCEPTION_CODE,USER_WRONG_CREDENTIALS_EXCEPTION_CODE
from auth.hash import verify_password,generate_jwt_data_from_user_model
from fastapi import APIRouter, Depends, HTTPException, status
from auth.hash import auth_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/v1/api")
security = HTTPBearer()

TOKEN_MINUTES = 360000

@router.get("/protected")
async def protected_route(request :Request, db: SessionLocal = Depends(get_db)):
    authorization_header = request.headers.get("Authorization")
    
    if authorization_header and authorization_header.startswith("Bearer "):
        token = authorization_header.split(" ")[1]
        auth_token(token, db)  # Perform token validation if token is provided
        route_token = True
    else:
        token = None
        route_token = False

    return {
        "routeToken": route_token,
        "status": "good"
    }




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
    access_token_expires = timedelta(minutes=TOKEN_MINUTES)

    access_token = create_access_token(
        data=generate_jwt_data_from_user_model(user), expires_delta=access_token_expires
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
