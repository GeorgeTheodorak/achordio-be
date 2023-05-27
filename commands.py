import argparse
import os
import random
from datetime import datetime, timedelta

from dotenv import load_dotenv
from faker import Faker
# from commands.article_command import createArticleWithParams
import sys
from commands.artist_command import createBaseTopArtists


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


def createArticle(l) -> None:
    pass


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'article' and sys.argv[2] == "--create":
            if sys.argv[3] == "--rand":
                createRandomArticle()
            else:
                createArticle(sys.argv)
            exit(1)
        if sys.argv[1] == "artists" and sys.argv == "--create":
            if sys.argv[3] == "--rand":

                genre = sys.argv[4]

                last_fm_url = os.environ.get("LAST_FM_URL")
                last_fm_api_key = os.environ.get("LAST_FM_API_KEY")

                createBaseTopArtists(genre, last_fm_url, last_fm_api_key)
            else:
                createArticle(sys.argv)
    else:
        print("Invalid command")


def modifiedMain():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    article_parser = subparsers.add_parser('article', help='Create an article')
    article_parser.add_argument('--create', action='store_true', help='Create an article')
    article_parser.add_argument('--rand', action='store_true', help='Create a random article')

    artists_parser = subparsers.add_parser('artists', help='Get top artists')
    artists_parser.add_argument('--create', action='store_true', help='Create base top artists')
    artists_parser.add_argument('--rand', action='store_true', help='Create random base top artists')
    artists_parser.add_argument('genre', type=str, help='Specify the genre')

    args = parser.parse_args()

    if args.command == 'article':
        if args.create:
            if args.rand:
                createRandomArticle()
            else:
                createArticle(sys.argv)
        else:
            print("Invalid command")

    elif args.command == 'artists':
        if args.create:
            if args.rand:
                last_fm_url = os.environ.get("LAST_FM_URL")
                last_fm_api_key = os.environ.get("LAST_FM_API_KEY")
                createBaseTopArtists(args.genre, last_fm_url, last_fm_api_key)
            else:
                print("NOT YET IMPLEMENTED")
                pass
        else:
            print("Invalid command")

    else:
        print("Invalid comand")

if __name__ == "__main__":
    load_dotenv(".env")
    modifiedMain()