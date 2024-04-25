""" Точка входа в приложение """
from core.application import gamebuddy_app


if __name__ == "__main__":
    gamebuddy_app.run(debug_mode=True)
