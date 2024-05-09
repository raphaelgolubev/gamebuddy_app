""" Содержит главный роутер, собирающий в себя все другие """

from fastapi import APIRouter

from modules.register.routers import router as register_router


main_router = APIRouter(prefix="/api/v1")
main_router.include_router(register_router)
