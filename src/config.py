from dotenv import load_dotenv
import os

load_dotenv()

UVICORN_RELOAD = os.environ.get("UVICORN_RELOAD")
UVICORN_HOST = os.environ.get("UVICORN_HOST")
UVICORN_PORT = int(os.environ.get("UVICORN_PORT"))
UVICORN_LOG_LEVEL = os.environ.get("UVICORN_LOG_LEVEL")
UVICORN_RELOAD_DIRS = os.environ.get("UVICORN_RELOAD_DIRS")

