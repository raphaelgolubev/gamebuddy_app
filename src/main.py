""" Точка входа в приложение """

from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.config import AppSettings

from src.routers import main_router
import src.database as database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await database.create_tables()
    yield
    # shutdown


app = FastAPI(
    title="gamebuddy", 
    description="A simple API for gamebuddy",
    version=AppSettings.APP_VERSION.value,
    lifespan=lifespan
)

app.include_router(main_router, prefix=AppSettings.API_URL.value)


@app.get(AppSettings.prefix('ping'))
def ping(): 
    return "pong"
