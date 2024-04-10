import uvicorn
import uvicorn.config

from fastapi import FastAPI

from config import UVICORN_HOST, UVICORN_PORT, UVICORN_LOG_LEVEL, UVICORN_RELOAD, UVICORN_RELOAD_DIRS

app = FastAPI(title="Soyamate", description="A simple API for Soyamate")

if __name__ == "__main__":
    # первая находка: аргумент reload работает только в методе uvicorn.run()
    uvicorn.run(
        "main:app", 
        host=UVICORN_HOST, 
        port=UVICORN_PORT, 
        log_level=UVICORN_LOG_LEVEL, 
        reload=UVICORN_RELOAD, 
        reload_dirs=UVICORN_RELOAD_DIRS
    )