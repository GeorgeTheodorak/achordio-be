import time
from psycopg2 import OperationalError
from sqlalchemy import create_engine


def check_postgres_ready(connection_string):
    while True:
        try:
            print("Trying to connect to db.")
            time.sleep(3)
            engine = create_engine(connection_string)
            with engine.connect():
                print("CONNEXCTED TO DB")
                return engine
        except OperationalError:
            print("no active db was found. retrying.")
            time.sleep(1)