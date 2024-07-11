from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


engine = create_engine(
    url=settings.database.url,
    echo=True,
    max_overflow=10,
    pool_size=10
)
session = sessionmaker(bind=engine)
