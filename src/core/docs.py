from fastapi import FastAPI, APIRouter

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

    fastapi_app: FastAPI

    def __init__(self, app: FastAPI):
        self.fastapi_app = app
        self._mount()

    def _mount(self):
        self.fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")

    def get_swagger_ui_html(self) -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=self.fastapi_app.openapi_url,
            title=self.fastapi_app.title + " - Swagger UI",
            oauth2_redirect_url=self.fastapi_app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
            swagger_ui_parameters={
                "syntaxHighlight.theme": "arta",
            }
        )

    def get_swagger_ui_oauth2_redirect_html(self) -> HTMLResponse:
        return get_swagger_ui_oauth2_redirect_html()

    def get_redoc_html(self) -> HTMLResponse:
        return get_redoc_html(
            openapi_url=self.fastapi_app.openapi_url,
            title=self.fastapi_app.title + " - ReDoc",
            redoc_js_url="/static/redoc.standalone.js",
        )
