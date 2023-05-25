from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func

from models import SessionLocal, get_db, Article

router = APIRouter(prefix="/v1/api")


@router.get("/articles", summary="returns constants and important data", response_model=None)
async def getArticles(db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100):
    articles = db.query(Article) \
        .offset(skip).limit(limit) \
        .all()

    response = []
    for article in articles:
        response.append(article.fixModelFieldsForResponse(False))

    return {"data": {
        "articles": response
        }
    }


@router.get("/articles/{article_id}")
async def getArticle(article_id: int, db: SessionLocal = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        return {"data": {}}

    response = {
        "data": {
            "articles": article.fixModelFieldsForResponse(is_light_mode=False)
        }
    }

    return response
