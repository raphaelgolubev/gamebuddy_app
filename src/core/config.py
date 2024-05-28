""" Конфигурация приложения """

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

model_config = SettingsConfigDict(
    env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="allow"
)


class Settings:
    def __init__(self):
        self.app = Settings.AppSettings()
        self.uvicorn = Settings.UvicornSettings()
        self.database = Settings.DatabaseSettings()

    class AppSettings(BaseSettings):
        """Класс конфигурации приложения"""

        APP_VERSION: str = "0.0.1"
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

        model_config = model_config

        @property
        def asyncpg_url(self) -> str:
            """Возвращает URL для подключения к базе данных c asyncpg"""
            return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


settings = Settings()
