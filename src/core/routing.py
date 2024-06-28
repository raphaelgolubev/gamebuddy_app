from fastapi import APIRouter, Depends

from core.dependencies import log_request_info
from modules.register.routers import router as register_router


main_router = APIRouter(prefix="/api/v1")
main_router.include_router(register_router, dependencies=[Depends(log_request_info)])
