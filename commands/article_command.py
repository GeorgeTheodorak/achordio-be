from sqlalchemy.orm import session
from models import SessionLocal, Article

text = "<h1>THIS IS A TEST</h1>"
title = "First article"
article_date = '1/1/1'
description = "my_first_desc"

# title = Column(String, nullable=False)
# content = Column(Text, nullable=False)
# thumbnail = Column(LargeBinary, nullable=False)
# article_date = Column(String, nullable=False)
# description = Column(String, nullable=False)
# created_at = Column(DateTime, nullable=False, default=func.now())
# updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())


def createArticle(image_src):
    session_db = SessionLocal()
    # Read the image file as binary data
    with open(image_src, 'rb') as file:
        image_data = file.read()

    # Create a new record in the table
    article = Article(
        title=title,
        article_date=article_date,
        thumbnail=image_data,
        content=text,
        description=description
    )

    # Add the new record to the session and commit it
    session_db.add(article)
    session_db.commit()
