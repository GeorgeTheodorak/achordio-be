from pydantic import BaseModel


class userUpdateAvatar(BaseModel):
    avatar: bytes
