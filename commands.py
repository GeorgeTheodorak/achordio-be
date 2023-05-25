import random
from datetime import datetime, timedelta
from faker import Faker
from commands.article_command import createArticleWithParams
import sys


# python commands.py article --create --rand
def createRandomArticle():
    random_number = random.randint(1, 30)

    imagePath = f"data/random_images/{random_number}.jpg"

    fake = Faker()
    article_name = fake.catch_phrase()
    fakeParagraph = fake.text()
    text = f"<p>{fakeParagraph}</p>"
    current_date = datetime.now().date()

    random_days = random.randint(1, 365)
    random_date = current_date - timedelta(days=random_days)
    description = fake.text()

    _id = createArticleWithParams(imagePath, article_name, random_date, text, description)
    print(f"Created new article with name {article_name} and id {_id}")

def createArticle(l)->None:
    pass


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'article' and sys.argv[2] == "--create":
            if sys.argv[3] == "--rand":
                createRandomArticle()
            else:
                createArticle(sys.argv)
            exit(1)
    else:
        print("Invalid command")


if __name__ == "__main__":
    main()
