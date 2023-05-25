import datetime

from sqlalchemy import Date
from models import SessionLocal, Article
from helpers.image_helper import downscale_image


def createArticle(image_src, article_title, article_date, text, description):
    session_db = SessionLocal()
    # Read the image file as binary data
    image_data = downscale_image(image_src, (250, 250))

    date_object = datetime.strptime(article_date, "%Y-%m-%d").date()

    # Create a new record in the table
    article = Article(
        title=article_title,
        article_date=date_object,
        thumbnail=image_data,
        content=text,
        description=description
    )

    # Add the new record to the session and commit it
    session_db.add(article)
    session_db.commit()

    return article.id
