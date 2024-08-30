import logging

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.settings import SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DATABASE_URL_ASYNC

logger = logging.getLogger(__name__)


def get_db_context():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_async_db_context():
    async with AsyncSessionLocal() as async_db:
        yield async_db


try:
    logger.debug(f"Creating engine with URL: {SQLALCHEMY_DATABASE_URL}")
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    metadata = MetaData()
    metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"Error creating synchronous engine: {str(e)}")
    raise

try:
    logger.debug(f"Creating async engine with URL: {SQLALCHEMY_DATABASE_URL_ASYNC}")
    async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC)
    AsyncSessionLocal = async_sessionmaker(
        async_engine, autocommit=False, autoflush=False
    )
except Exception as e:
    logger.error(f"Error creating asynchronous engine: {str(e)}")
    raise

Base = declarative_base()
