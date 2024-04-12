""" Точка входа в приложение """

import uvicorn
from fastapi import FastAPI
from config import AppSettings, UvicornSettings

app = FastAPI(
    title="Soyamate", 
    description="A simple API for Soyamate",
    version=AppSettings.APP_VERSION.value
)


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
