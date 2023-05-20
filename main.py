import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from psycopg2 import OperationalError
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from starlette import status
from starlette.responses import JSONResponse
from routers.global_data import router as global_data_router
from routers.authentication import router as authentication_data_router
from fastapi import Depends
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from db import check_postgres_ready

load_dotenv(".env")
postgresUrl = os.environ.get("POSTGRES_URL")
Base = declarative_base()

# This is an infinite loop. 
engine = check_postgres_ready(postgresUrl)

# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_name = Column(String, nullable=False)
#     email = Column(String, nullable=False)
#     created_at = Column(DateTime, nullable=False, default=func.now())
#     updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
#
# # Load environment variables from .env file
#
# engine = create_engine(os.environ.get("POSTGRES_URL"))
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
# Base.metadata.create_all(bind=engine)
#

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


app = FastAPI()
app.include_router(global_data_router)
app.include_router(authentication_data_router)


class CustomError(BaseModel):
    error_code: int
    error_message: str


class CustomException(Exception):
    def __init__(self, error_code: int, error_message: str, response_code: int):
        self.error_code = error_code
        self.error_message = error_message
        self.response_code = response_code


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
    return {"message": "All good", "envFileTest": os.environ.get("POSTGRES_URL")}

@app.get("/error-test")
async def root():
    raise CustomException(1,"custopmErr-r",404)
    return {"message": "All good", "envFileTest": os.environ.get("POSTGRES_URL")}
