from sqlalchemy.orm import  declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import os

import logging

from .config import load_env

load_env()

#DSN для примера: DSN=postgresql+asyncpg://user:password@localhost:5432/postgres
DATABASE_URL = os.getenv("DSN")

engine = create_async_engine(
    DATABASE_URL,
    echo = True,
    connect_args={"check_same_thread": False},
)

SessionLocal = async_sessionmaker(
    autoflush=False,
    bind=engine,
    class_= AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

logger = logging.getLogger(__name__)

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
            logger.info("Transaction committed")
        except Exception as e:
            logger.error(f"Transaction rolled back due to exception: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()