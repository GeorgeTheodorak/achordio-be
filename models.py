import os
import time
from db import check_postgres_ready
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

load_dotenv(".env")
postgresUrl = os.environ.get("POSTGRES_URL")
Base = declarative_base()

# This is an infinite loop. 
engine = check_postgres_ready(postgresUrl)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db()->sessionmaker:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
        # Add the following line to define metadata for the User model
    metadata = Base.metadata

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def fixModelFields(self):
        return {
            "id":self.id,
            "user_name":self.user_name,
            "email":self.email
        }
