""" Точка входа в приложение """

import uvicorn

from src.config import UvicornSettings


# первая находка: аргумент reload работает только в методе uvicorn.run()

# вторая находка: для доступа к значению перечисления,
# нужно обращаться к value

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=UvicornSettings.HOST.value,
        port=UvicornSettings.PORT.value,
        log_level=UvicornSettings.LOG_LEVEL.value,
        reload=UvicornSettings.RELOAD.value,
    )
