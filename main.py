import os
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from starlette import status
from auth.hash import get_hashed_password

app = FastAPI()

load_dotenv(".env")  # Load environment variables from .env file

@app.get("/greet")
async def root():
    return {"message": "All good","envFileTest":os.environ.get("postGresPassword")}




