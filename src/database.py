from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

Base = declarative_base()


async def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        yield db
    finally:
        db.close()
