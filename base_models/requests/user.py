from pydantic import BaseModel


class userUpdateThumbnail(BaseModel):
    thumbnail: bytes
