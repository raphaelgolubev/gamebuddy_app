from datetime import datetime
from typing import Annotated
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column

from core.config import database_settings


class Base(DeclarativeBase):
    pass


class Annotations:
    """ Класс с аннотациями для переиспользуемости кода в объявлении таблиц """
    primary_id = Annotated[UUID, mapped_column(primary_key=True)]
    created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
    updated_at = Annotated[datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"), 
        onupdate=text("TIMEZONE('utc', now())")
    )]


async_engine = create_async_engine(
    database_settings.asyncpg_url, 
    echo=True,
    pool_size=10,
    max_overflow=10,
)
async_session_factory = async_sessionmaker(async_engine)


def create_tables():
    Base.metadata.drop_all(async_engine)
    Base.metadata.create_all(async_engine)
