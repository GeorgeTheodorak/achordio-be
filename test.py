# import random
# from datetime import datetime, timedelta
#
# from faker import Faker
#
# random_number = random.randint(1, 30)
#
# imagePath = f"data/images/{random_number}.jpg"
#
# fake = Faker()
#
# article_name = fake.catch_phrase()
# fakeParagraph = fake.text()
# text = f"<p>{fakeParagraph}</p>"
# current_date = datetime.now().date()
# # Generate a random number of days between 1 and 365
# random_days = random.randint(1, 365)
# # Subtract the random number of days from the current date
# random_date = current_date - timedelta(days=random_days)
# description = fake.text()