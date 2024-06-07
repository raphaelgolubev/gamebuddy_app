from fastapi import FastAPI

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


class Docs:
    """
    Класс документации FastAPI.
    """

    def __init__(self, app: FastAPI):
        self.fastapi_app = app
        self._mount()

    def _mount(self):
        self.fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")

    def get_swagger_ui_html(self) -> HTMLResponse:
        openapi_url = self.fastapi_app.openapi_url or "/openapi.json"
        return get_swagger_ui_html(
            openapi_url=openapi_url,
            title=self.fastapi_app.title + " - Swagger UI",
            oauth2_redirect_url=self.fastapi_app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
            swagger_ui_parameters={
                "syntaxHighlight.theme": "arta",
            }
        )

    @property
    def get_swagger_ui_ouath2_redirect_url(self) -> str:
        return self.fastapi_app.swagger_ui_oauth2_redirect_url or "/redirect_url"

    def get_swagger_ui_oauth2_redirect_html(self) -> HTMLResponse:
        return get_swagger_ui_oauth2_redirect_html()

    def get_redoc_html(self) -> HTMLResponse:
        openapi_url = self.fastapi_app.openapi_url or "/openapi.json"
        return get_redoc_html(
            openapi_url=openapi_url,
            title=self.fastapi_app.title + " - ReDoc",
            redoc_js_url="/static/redoc.standalone.js",
        )


class AppMetadata:
    """Метаданные для Swagger"""

    title = "GameBuddy"
    summary = "Сервис поиска тиммейтов для сетевых видеоигр"
    description = """
## Содержание
* [Регистрация](https://github.com/raphaelgolubev/gamebuddy_app/blob/main/docs/Register.md)
* [Авторизация](https://github.com/raphaelgolubev/gamebuddy_app/blob/main/docs/Login.md)
* [Аутентификация](https://github.com/raphaelgolubev/gamebuddy_app/blob/main/docs/Auth.md)

## Коды ошибок
### Регистрация
* 1000 - регистрация
* 1001 - пользователь с таким email уже существует
* 1002 - пользователь не найден
* 1003 - код верификации неверный
* 1004 - время действия кода истекло

### Авторизация
* 2000 - авторизация

### Аутентификация
* 3000 - аутентификация

"""

    tags = [
        {
            "name": "Регистрация",
            "description": "Методы для регистрации нового пользователя",
            "externalDocs": {
                "description": "Ссылка на полную документацию",
                "url": "https://github.com/raphaelgolubev/gamebuddy_app/blob/main/docs/Register.md"
            }
        }
    ]
