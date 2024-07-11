""" Конфигурация приложения """

from logging import (INFO, DEBUG, WARNING, ERROR, CRITICAL)

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

model_config = SettingsConfigDict(
    env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="allow"
)


class Settings:
    def __init__(self):
        self.app = Settings.AppSettings()
        self.logger = Settings.LoggerSettings()
        self.uvicorn = Settings.UvicornSettings()
        self.database = Settings.DatabaseSettings()

    class LoggerSettings(BaseSettings):
        IS_LOGGER_ENABLED: bool = True

        LEVEL: int = DEBUG
        DIR: str = "logs"
        BACKUPS_COUNT: int = 15
        FILE_LENGTH_LIMIT: int = 1024 * 1024 * 1

        FILE_PREFIX: str | None = None
        FILE_SUFFIX: str | None = None
        USE_DATE_AS_SUFFIX: bool = False
        DATE_SUFFIX_FORMAT: str = "_%Y-%m-%d"
        SHOW_TRACEBACK: bool = False
        MAX_LENGTH: int = 180

        SENSITIVE_REGEX_PATTERNS: list[str] = [
            r"\d{3}-\d{2}-\d{4}"
        ]
        SENSITIVE_KEYS: tuple = (
            "headers",
            "credentials",
            "Authorization",
            "token",
            "password",
        )

        model_config = model_config

    class AppSettings(BaseSettings):
        """Класс конфигурации приложения"""

        VERSION: str = "0.0.1"
        API_PATH: str = "/api"
        API_VERSION: str = "v1"
        API_URL: str = f"{API_PATH}/{API_VERSION}"

        model_config = model_config

    class UvicornSettings(BaseSettings):
        """Класс конфигурации uvicorn"""

        HOST: str = Field(default="127.0.0.1", alias="uvicorn_host")
        PORT: int = Field(default=8000, alias="uvicorn_port")
        LOG_LEVEL: str = Field(default="info", alias="uvicorn_log_level")

        model_config = model_config

    class DatabaseSettings(BaseSettings):
        """Класс конфигурации базы данных"""

        HOST: str = Field(default="localhost", alias="db_host")
        PORT: int = Field(default=5432, alias="db_port")
        NAME: str = Field(default="mydatabase", alias="db_name")
        USER: str = Field(default="user", alias="db_user")
        PASSWORD: str = Field(default="password", alias="db_password")
        DRIVER: str = "psycopg2"

        model_config = model_config

        @property
        def url(self) -> str:
            """Возвращает URL для подключения к базе данных"""
            return f"postgresql+{self.DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


settings = Settings()
