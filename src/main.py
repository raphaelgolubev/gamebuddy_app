""" Точка входа в приложение """

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from config import AppSettings, UvicornSettings

from routers import main_router
import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await database.create_tables()
    yield
    # shutdown


app = FastAPI(
    title="Soyamate", 
    description="A simple API for Soyamate",
    version=AppSettings.APP_VERSION.value,
    lifespan=lifespan
)

app.include_router(main_router, prefix=AppSettings.API_URL.value)


@app.get(AppSettings.prefix('ping'))
def ping(): 
    return "pong"


if __name__ == "__main__":
    # первая находка: аргумент reload работает только в методе uvicorn.run()
    # вторая находка: для доступа к значению перечисления,
    # нужно обращаться к value
    uvicorn.run(
        "main:app",
        host=UvicornSettings.HOST.value,
        port=UvicornSettings.PORT.value,
        log_level=UvicornSettings.LOG_LEVEL.value,
        reload=UvicornSettings.RELOAD.value,
    )
