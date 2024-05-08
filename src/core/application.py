import uvicorn
from fastapi import FastAPI

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)
from fastapi.staticfiles import StaticFiles

from core.config import settings
from core.database import create_tables

from core.routing import main_router


class GameBuddyApp:
    """Объект, управляющий жизненным циклом приложения"""

    fastapi_app: FastAPI

    def __init__(self):
        self._build_fastapi()
        self.setup()

    def _build_fastapi(self):
        self.fastapi_app = FastAPI(
            docs_url=None,  # отключаем дефолтные доки
            redoc_url=None,
            title="GameBuddy",
            summary="A simple API for GameBuddy",
            version=settings.app.APP_VERSION,
        )

        self.fastapi_app.include_router(main_router)

    def setup(self):
        pass
        # create_tables()

    def run(self, debug_mode=False):
        """
        ### Описание
        Запускает сервер, который будет принимать запросы на API.

        ### Параметры:
            - `debug_mode: Bool`
                - `True` - передает в `uvicorn.run` строку пути к экземпляру приложения
                - `False` - передает в `uvicorn.run` сам экземпляр приложения, что гарантирует выключение `reload`,
                  даже если `reload=True` (так работает uvicorn).
        """
        instance: FastAPI | str = (
            "core.application:gamebuddy_app.fastapi_app"
            if debug_mode
            else self.fastapi_app
        )

        uvicorn.run(
            instance,
            host=settings.uvicorn.HOST,
            port=settings.uvicorn.PORT,
            log_level=settings.uvicorn.LOG_LEVEL,
            reload=debug_mode,
        )

    def shutdown(self):
        """А тут закрывать коннекты к БД напрмер"""
        pass


gamebuddy_app = GameBuddyApp()


app = gamebuddy_app.fastapi_app
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_ui_parameters={
            "syntaxHighlight.theme": "arta",
        }
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )
