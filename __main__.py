""" Точка входа в приложение """

import uvicorn

from src.config import uvicorn_settings


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=uvicorn_settings.HOST,
        port=uvicorn_settings.PORT,
        log_level=uvicorn_settings.LOG_LEVEL,
        reload=uvicorn_settings.RELOAD,
    )
