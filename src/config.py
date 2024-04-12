""" Конфигурация приложения """

from dotenv import load_dotenv
import os

from enum import Enum


load_dotenv()


class AppSettings(Enum):
    """ Перечисление параметров конфигурации приложения """
    APP_VERSION = "0.0.1"
    API_PATH = "/api"
    API_VERSION = "v1"
    API_URL = f"{API_PATH}/{API_VERSION}"

    def prefix(method: str = "") -> str:
        """ 
        Возвращает путь к методу API с указанным именем.
        Если метод не передан, то возвращает путь к API.
        """

        if method:
            return f"{AppSettings.API_URL.value}/{method}"

        return AppSettings.API_URL.value


class UvicornSettings(Enum):
    """ Перечисление параметров конфигурации uvicorn """
    RELOAD = os.environ.get("UVICORN_RELOAD")
    HOST = os.environ.get("UVICORN_HOST")
    PORT = int(os.environ.get("UVICORN_PORT"))
    LOG_LEVEL = os.environ.get("UVICORN_LOG_LEVEL")
