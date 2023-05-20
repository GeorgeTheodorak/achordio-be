import time
from psycopg2 import OperationalError
from sqlalchemy import create_engine


def check_postgres_ready(connection_string):
    while True:
        try:
            print(connection_string)
            time.sleep(5)
            engine = create_engine(connection_string)

            with engine.connect():
                return engine
        except OperationalError:
            print("no active db was found. retrying.")
            time.sleep(1)