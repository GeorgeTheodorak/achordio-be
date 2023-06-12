import base64
import os
import time
from db import check_postgres_ready
from dotenv import load_dotenv
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Text, LargeBinary, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from helpers.user_helper import generateRandomVerificationCode

Base = declarative_base()

load_dotenv(".env")
postgresUrl = os.environ.get("POSTGRES_URL")
Base = declarative_base()

# This is an infinite loop. 
engine = check_postgres_ready(postgresUrl)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db() -> sessionmaker:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    metadata = Base.metadata

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    google_id = Column(String, nullable=True)
    facebook_id = Column(String, nullable=True)
    user_visibility = Column(Integer, nullable=True, default=1)
    thumbnail = Column(LargeBinary, nullable=True)
    phone_number = Column(String, nullable=True)
    is_active = Column(Integer, nullable=False, default=1)
    is_verified = Column(Integer, nullable=False, default=0)
    verification_code = Column(String, nullable=False, default=generateRandomVerificationCode())
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def fixModelFields(self, is_light_mode: bool) -> dict:

        response = {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
            "user_visibility": self.user_visibility,
            "is_facebook_connected": self.facebook_id is not None,
            "is_google_connected": self.google_id is not None,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
        }

        if not is_light_mode:
            binaryThumb = self.thumbnail
            encoded_image = None
            if binaryThumb is not None:
                # Encode the image data as Base64
                encoded_image = base64.b64encode(binaryThumb).decode('utf-8')

            response["thumbnail"] = encoded_image
        return response


class Article(Base):
    metadata = Base.metadata

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    thumbnail = Column(LargeBinary, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def fixModelFields(self, is_light_mode: bool) -> dict:
        binaryThumb = self.thumbnail
        # Encode the image data as Base64
        encoded_image = base64.b64encode(binaryThumb).decode('utf-8')

        base_response = {
            "id": self.id,
            "title": self.title,
            "thumbnail": encoded_image,
            "description": self.description,
            "created_at": self.created_at
        }

        if not is_light_mode:
            base_response["content"] = self.content

        return base_response


class Artists(Base):
    metadata = Base.metadata
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    music_brainz_identifier = Column(String, index=True, nullable=True)
    spotify_id = Column(String, index=True, nullable=True)
    isni_code = Column(String, nullable=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def fixModelFields(self, is_light_mode: bool) -> dict:
        base_response = {
            "id": self.id,
            "name": self.name,
            "spotify_id": self.spotify_id,
            "isni_code": self.isni_code,
            "description": self.description,
            "music_brainz_identifier": self.music_brainz_identifier,
        }

        return base_response


class Songs(Base):
    metadata = Base.metadata
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    music_brainz_identifier = Column(String, index=True, nullable=True)
    spotify_id = Column(String, index=True, nullable=True)
    isni_code = Column(String, nullable=True)
    name = Column(String, nullable=False)
    info_data = Column(JSON, nullable=True)  # this schema will be later decided.


class Charts(Base):
    metadata = Base.metadata
    __tablename__ = "charts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False, index=True)
    chart = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def response(self):
        return {
            "id": self.id,
            "chart": self.chart
        }
