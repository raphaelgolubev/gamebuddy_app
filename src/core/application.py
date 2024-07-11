import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.docs import (AppMetadata, Docs)
from core.routing import main_router

from pydantic_core import ValidationError
from core.exceptions import (
    routers,
    register_errors
)


class GameBuddyApp:
    """Объект, управляющий жизненным циклом приложения"""

    fastapi_app: FastAPI

    def __init__(self):
        self._build_fastapi()

    def _build_fastapi(self):
        self.fastapi_app = FastAPI(
            docs_url=None,  # отключаем дефолтные доки
            redoc_url=None,
            title=AppMetadata.title,
            summary=AppMetadata.summary,
            description=AppMetadata.description,
            openapi_tags=AppMetadata.tags,
            version=settings.app.VERSION,
        )

        self._attach_exception_handlers()
        self.fastapi_app.include_router(main_router)

    def _attach_exception_handlers(self):
        self.fastapi_app.add_exception_handler(
            ValidationError, 
            routers.validation_exception_handler
        )
        self.fastapi_app.add_exception_handler(
            routers.InvalidRequestError, 
            handler=routers.invalid_request_exception_handler
        )
        self.fastapi_app.add_exception_handler(
            Exception, 
            routers.generic_exception_handler
        )

        self.fastapi_app.add_exception_handler(
            register_errors.UserAlreadyExistsError, 
            handler=register_errors.user_already_exists
        )

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

# =============== SWAGGER UI ===============

docs = Docs(app=gamebuddy_app.fastapi_app)


@docs.fastapi_app.get("/docs/swagger", include_in_schema=False)
async def custom_swagger_ui():
    return docs.get_swagger_ui_html()


@docs.fastapi_app.get(docs.get_swagger_ui_oauth2_redirect_url, include_in_schema=False)  # type: ignore
async def swagger_ui_redirect():
    return docs.get_swagger_ui_oauth2_redirect_html()


@docs.fastapi_app.get("/docs/redoc", include_in_schema=False)
async def redoc_html():
    return docs.get_redoc_html()
