from fastapi import Request
from loguru import logger


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
