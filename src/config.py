""" Конфигурация приложения """
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='allow'
    )


class AppSettings(Settings):
    """ Класс конфигурации приложения """
    APP_VERSION: str = "0.0.1"
    API_PATH: str = "/api"
    API_VERSION: str = "v1"
    API_URL: str = f"{API_PATH}/{API_VERSION}"


class UvicornSettings(Settings):
    """ Перечисление параметров конфигурации uvicorn """
    RELOAD: str = Field(alias='uvicorn_reload')
    HOST: str = Field(alias='uvicorn_host')
    PORT: int = Field(alias='uvicorn_port')
    LOG_LEVEL: str = Field(alias='uvicorn_log_level')


class DatabaseSettings(Settings):
    """ Перечисление параметров конфигурации базы данных """
    HOST: str = Field(alias='db_host')
    PORT: int = Field(alias='db_port')
    NAME: str = Field(alias='db_name')
    USER: str = Field(alias='db_user')
    PASSWORD: str = Field(alias='db_password')

    @property
    def asyncpg_url(self) -> str:
        """ Возвращает URL для подключения к базе данных """
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


app_settings = AppSettings()
uvicorn_settings = UvicornSettings()
database_settings = DatabaseSettings()
