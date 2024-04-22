from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import database_settings


engine_async = create_async_engine(database_settings.asyncpg_url, echo=True)

Base = declarative_base()

async_session = sessionmaker(
    bind=engine_async, 
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_tables() -> None:
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
