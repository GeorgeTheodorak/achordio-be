from sqlalchemy.orm import session
from models import SessionLocal, Article


def createArticle(image_src, article_title, article_date, text, description):
    session_db = SessionLocal()
    # Read the image file as binary data
    with open(image_src, 'rb') as file:
        image_data = file.read()

    # Create a new record in the table
    article = Article(
        title=article_title,
        article_date=article_date,
        thumbnail=image_data,
        content=text,
        description=description
    )

    # Add the new record to the session and commit it
    session_db.add(article)
    session_db.commit()

    return article.id