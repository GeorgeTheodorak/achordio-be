import time
from psycopg2 import OperationalError
from sqlalchemy import create_engine


def check_postgres_ready(connection_string):
    while True:
        try:
            print("{BE} Trying to connect to db.")

            time.sleep(3)
            engine = create_engine(connection_string)
            with engine.connect():
                print("{BE} Connected to db successfully ")
                return engine
        except OperationalError:
            print("{BE} Failed to connect to db,retrying in 3 sec.")
            time.sleep(3)
