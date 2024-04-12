from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from config import DatabaseSettings


engine_async = create_async_engine(DatabaseSettings.URL.value, echo=True)

Base = declarative_base()

async_session = sessionmaker(
    bind=engine_async, 
    class_=AsyncSession,
    expire_on_commit=False
)


class TestTable(Base):
    __tablename__ = 'test_table'
    id = Column(Integer, primary_key=True)


async def create_tables() -> None:
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
