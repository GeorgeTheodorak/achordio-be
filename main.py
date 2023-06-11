import os
from exceptions.generic_exceptions import CustomError
from exceptions.generic_exceptions import CustomException
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from routers.global_data import router as global_data_router
from routers.authentication import router as authentication_data_router
from routers.songs.song import song_router
from routers.articles import router as article_router
from routers.artists import router as artists_router
from routers.users import router as user_router
from helpers import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# This runs the fast api application.

app = FastAPI()

# add routers to the app
app.include_router(global_data_router)
app.include_router(authentication_data_router)
app.include_router(song_router)
app.include_router(article_router)
app.include_router(artists_router)
app.include_router(user_router)


# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # Assuming your React app runs on this port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    error_response = CustomError(
        error_code=exc.error_code,
        error_message=exc.error_message
    )

    error_response = {
        "data": {},
        "error": error_response.dict()
    }
    return JSONResponse(status_code=exc.response_code, content=error_response)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_messages = []
    for error in exc.errors():
        error_messages.append({
            "data": {},
            "error": {
                "error_message": error.get("msg"),
                "code": None
            }
        })

    return JSONResponse(status_code=400, content=error_messages[0])


@app.get("/greet")
async def root():
    return {"message": "Whats up brother?"}


@app.get("/error-test")
async def root():
    raise CustomException(1, "This is my custom error", 404)

# .
# ├── achordio-be
# │   ├── __init__.py
# │   ├── main.py
# │   ├── test.py
# │   └── routers
# │   │   ├── __init__.py
# │   │   ├── authentication.py
# │   │   └── global_data.py
# │   └── auth_request.py
# │       ├── __init__.py
# │       ├── jwt_generation.py
# │       └── hash.py
