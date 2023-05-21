import datetime
import time
from exceptions.generic_exceptions import USER_WRONG_CREDENTIALS_EXCEPTION_CODE,CustomException,USER_EXPIRED_TOKEN
from fastapi import status
from sqlalchemy import and_
from models import User
from models import get_db
from auth import jwt_generation
from auth.jwt_generation import SECRET_KEY
from passlib.context import CryptContext
import jwt


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def auth_token(token,db)->bool:    
    
    
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    user_name = decoded_token.get("sub")
    password = decoded_token.get("pw")
    mail = decoded_token.get("mail")
    expire_date_token = decoded_token.get("exp")

    current_time = datetime.datetime.utcnow()
    expire_date = datetime.datetime.fromtimestamp(expire_date_token)

    if current_time > expire_date:
           # expired token.
           raise CustomException(
            USER_EXPIRED_TOKEN,
            "EXPIRED TOKEN",
            status.HTTP_403_FORBIDDEN
        )

    user = db.query(User).filter(and_(User.email == mail, User.user_name == user_name)).first()

    if user is None:
        #invalid token
        raise CustomException(
            USER_WRONG_CREDENTIALS_EXCEPTION_CODE,
            "Invalid Token",
            status.HTTP_403_FORBIDDEN
        )
    else:
        return True
    

def generate_jwt_data_from_user_model(User : User)->dict:
    return {
        "sub": User.user_name,
        "pw": User.password,
        "mail": User.email
    }


def decodeString(string :str):
    return jwt_generation.decode(string, SECRET_KEY, algorithms=["HS256"])