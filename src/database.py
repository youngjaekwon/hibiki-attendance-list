from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
