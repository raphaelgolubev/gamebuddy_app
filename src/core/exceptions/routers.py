from fastapi import status
from fastapi.responses import JSONResponse

from core.utils.logging.logger import AppLogger

logger = AppLogger(__name__)


class InvalidRequestError(Exception):
    pass


async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": exc.errors()}
    )


async def invalid_request_exception_handler(request, exc: InvalidRequestError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": f"{exc}"})


async def generic_exception_handler(request, exc):
    logger.error(f"An unexpected error occurred: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )
