import logging

from fastapi import Request


logging.basicConfig(
    level=logging.INFO, 
    filename="logs/app.log", 
    format="%(asctime)s %(levelname)s %(message)s"
)


async def log_request_info(request: Request):
    request_body = await request.json()

    logging.info(
        f"{request.method} request to {request.url} metadata\n"
        f"\tHeaders: {request.headers}\n"
        f"\tBody: {request_body}\n"
        f"\tPath Params: {request.path_params}\n"
        f"\tQuery Params: {request.query_params}\n"
        f"\tCookies: {request.cookies}\n"
    )
