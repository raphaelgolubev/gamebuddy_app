from fastapi import APIRouter
from .dependencies import get_docs


router = APIRouter()
docs = get_docs()


@router.get("/docs/swagger", include_in_schema=False)
async def custom_swagger_ui():
    return docs.get_swagger_ui_html()


@router.get(docs.get_swagger_ui_ouath2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return docs.get_swagger_ui_oauth2_redirect_html()


@router.get("/docs/redoc", include_in_schema=False)
async def redoc_html():
    return docs.get_redoc_html()
