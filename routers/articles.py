from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func

from models import SessionLocal, get_db, Article

router = APIRouter(prefix="/v1/api")


@router.get("/articles", summary="returns constants and important data", response_model=None)
async def getArticles(db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100):
    articles = db.query(Article.id, Article.title, Article.description, Article.article_date) \
        .offset(skip).limit(limit) \
        .add_columns(
        func.json_build_object('id', Article.id, 'title', Article.title, 'description', Article.description,
                               'article_date', Article.article_date).label('article')) \
        .all()

    # response = {"data":{}}
    # for row in articles:
    #     response['data'].append
    # # Extract the 'article' dictionary from each row
    articles = [row.article for row in articles]

    return articles

@router.get("/articles/{article_id}")
async def getArticle(article_id: int, db: SessionLocal = Depends(get_db)):
    articles = db.query(Article).offset(skip).limit(limit).all()
    db.close()
    return articles
