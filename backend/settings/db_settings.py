import os
from sqlalchemy import create_engine


class DBSettings:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_MAIN_DATABASE = os.getenv("DB_MAIN_DATABASE")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    CONNECTION_DATA = f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_MAIN_DATABASE}"

    engine = create_engine(f'postgresql+psycopg2://{CONNECTION_DATA}')
