from commands.article_command import createArticle
import sys


# python commands.py article --create "data/images/Cat03.jpg" "My First Article" "1/1/2022" "This is a dummy thing"
def runFunction(args):
    imagePath = args[3]
    text = "<h1>THIS IS A TEST</h1>"
    title = args[4]
    article_date = args[5]
    description = args[6]

    _id = createArticle(imagePath, title, article_date, text, description)
    print(f"Created new article with name {title} and id {_id}")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'article' and sys.argv[2] == "--create":
            runFunction(sys.argv)
            exit(1)
    else:
        print("Invalid command")


if __name__ == "__main__":
    main()
