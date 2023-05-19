import os
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from starlette import status
from auth.hash import get_hashed_password
from response_models import auth

app = FastAPI()

load_dotenv(".env")  # Load environment variables from .env file

@app.get("/greet")
async def root():
    return {"message": "All good","envFileTest":os.environ.get("postGresPassword")}

@app.post('/user-register', summary="Create new user", response_model=auth.authRequest)
async def create_user(form_data: auth.authRequest):
    # querying database to check if user already exist
    
    user = None
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    
    user = {
        'email': form_data.email,
        'password': get_hashed_password(form_data.password),
        'id': str(uuid4())
    }

    return user


@app.post('/login', summary="Create access and refresh tokens for user", response_model=auth.authResponse)
async def login(form_data: auth.authRequest):

    # user = user.mial

    # if form_data.e !=  mail

    # user = db.get(form_data.username, None)
    # if user is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Incorrect email or password"
    #     )

    # hashed_pass = user['password']
    # if not verify_password(form_data.password, hashed_pass):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Incorrect email or password"
    #     )
    
    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }
    