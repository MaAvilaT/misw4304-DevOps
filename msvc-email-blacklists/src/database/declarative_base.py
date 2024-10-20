import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')

DB_PATH = os.environ.get('DATABASE_URL')

if not DB_PATH:
    db_path = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
else:
    db_path = DB_PATH

engine = create_engine(db_path)
Session = sessionmaker(bind=engine)

Base = declarative_base()


def open_session():
    return Session()
