""" Точка входа в приложение """

import sys

from core.dependencies import get_gamebuddy_app

gamebuddy_app = get_gamebuddy_app()

if __name__ == "__main__":
    if "--debug" in sys.argv:
        gamebuddy_app.run(debug_mode=True)
    else:
        gamebuddy_app.run(debug_mode=False)
