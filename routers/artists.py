from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func

from base_models.responses.base_response import BaseResponse
from models import SessionLocal, get_db, Article, Artists

router = APIRouter(prefix="/v1/api")


@router.get("/artists", summary="returns all the artists", response_model=BaseResponse)
async def getArticles(db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100):
    artists = db.query(Artists) \
        .offset(skip).limit(limit) \
        .all()

    response_data = []
    for artist in artists:
        response_data.append(artist.fixModelFieldsForResponse(False))

    response = BaseResponse(data={"artists": response_data})
    return response


@router.get("/artists/{article_id}", response_model=BaseResponse)
async def getArticle(article_id: int, db: SessionLocal = Depends(get_db)):
    artist = db.query(Artists).filter(Artists.id == article_id).first()

    if artist is None:
        data = {"artists": []}
    else:
        data = {"artists": artist.fixModelFieldsForResponse(is_light_mode=False)}

    response = BaseResponse(data=data)
    return response
