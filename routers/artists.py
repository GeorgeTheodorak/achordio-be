from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func

from base_models.responses.base_response import BaseResponse
from models import SessionLocal, get_db, Article

router = APIRouter(prefix="/v1/api")


@router.get("/artists", summary="returns all the artists", response_model=BaseResponse)
async def getArticles(db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100):
    articles = db.query(Article) \
        .offset(skip).limit(limit) \
        .all()

    response_data = []
    for article in articles:
        response_data.append(article.fixModelFieldsForResponse(False))

    response = BaseResponse(data=response_data)
    return response


@router.get("/articles/{article_id}", response_model=BaseResponse)
async def getArticle(article_id: int, db: SessionLocal = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if article is None:
        data = {"articles": []}
    else:
        data = {"articles": article.fixModelFieldsForResponse(is_light_mode=False)}

    response = BaseResponse(data=data)
    return response
