import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = os.environ.get('DATABASE_USER')
db_password = os.environ.get('DATABASE_PASSWORD')
db_host = os.environ.get('DATABASE_HOST')
db_port = os.environ.get('DATABASE_PORT')
db_name = os.environ.get('DATABASE_NAME')

# DB_PATH = os.environ.get('DATABASE_URL')

if db_host:
    db_path = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
else:
    db_path = 'sqlite:///:memory:'

engine = create_engine(db_path)
Session = sessionmaker(bind=engine)

Base = declarative_base()


def open_session():
    return Session()
