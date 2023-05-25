from datetime import datetime

from sqlalchemy import Date
from models import SessionLocal, Article
from helpers.image_helper import downscale_image


def createArticleWithParams(image_src, article_title, article_date, text, description):
    session_db = SessionLocal()
    # Read the image file as binary data
    image_data = downscale_image(image_src, (256, 256))

    # Create a new record in the table
    article = Article(
        title=article_title,
        created_at=article_date,
        thumbnail=image_data,
        content=text,
        description=description
    )

    # Add the new record to the session and commit it
    session_db.add(article)
    session_db.commit()

    return article.id
