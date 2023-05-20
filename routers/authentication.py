from fastapi import APIRouter, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette import status
from uuid import uuid4

from starlette.responses import JSONResponse

from auth.hash import get_hashed_password
from auth.jwt_generation import create_access_token, create_refresh_token
from responses import auth_response

router = APIRouter(prefix="/v1/api")


@router.post('/user-register', summary="Create new models.py", response_model=auth_response.authRequest)
async def create_user(form_data: auth_response.authRequest):
    # querying database to check if models.py already exist

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


@router.post('/login', summary="Create access and refresh tokens for models.py", response_model=auth_response.authResponse)
async def login(form_data: auth_response.authRequest):
    # models.py = models.py.mial

    # if form_data.e !=  mail

    # models.py = db.get(form_data.username, None)
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
