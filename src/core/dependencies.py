from fastapi import Request
from loguru import logger

from modules.user.models import User

from modules.register.repository import RegisterRepository
from modules.register.service import RegisterService


async def log_request_info(request: Request):
    request_body = await request.json()

    logger.debug(
        f"{request.method} request to {request.url} \n"
        f"\tHeaders: {request.headers}\n"
        f"\tBody: {request_body}\n"
        f"\tPath Params: {request.path_params}\n"
        f"\tQuery Params: {request.query_params}\n"
        f"\tCookies: {request.cookies}\n"
    )


def get_register_service():
    repo = RegisterRepository(model=User)
    return RegisterService(repo)
