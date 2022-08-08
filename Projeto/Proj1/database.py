from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import database_exists, create_database
import secrets


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{secrets.username}:{secrets.password}@localhost:3306/Oximetro2"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

