import os
import subprocess


def echo(message: str):
    print(f"> {message}")


def get_pwd() -> str:
    result = run_command("", "pwd", output=False)
    if result:
        return result.stdout.decode("utf-8").rstrip()
    else:
        raise Exception("Не удалось получить путь к директории")


def get_venv() -> str:
    return os.path.join(get_pwd(), "venv")


def run_command(label: str, cmd: str, output: bool = True):
    try:
        task = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        if len(label) > 0:
            echo(label)
        if output:
            echo(task.stdout.decode("utf-8"))

        return task

    except subprocess.CalledProcessError as e:
        echo(f"Ошибка: {e}")
        exit()


def create_venv():
    pwd = get_pwd()
    venv_path = os.path.join(pwd, "venv")

    if os.path.exists(venv_path):
        echo("Виртуальное окружение уже существует")
    else:
        run_command("Создаем виртуальное окружение...", cmd="python3 -m venv venv")


def install_requirements():
    pip = os.path.join(get_venv(), "bin", "pip")
    echo("Установка зависимостей")

    run_command("Проверка pip-а...", cmd=f"{pip} install --upgrade pip")
    run_command("Установка зависимостей...", cmd=f"{pip} install -r requirements.txt")


def run():
    create_venv()
    install_requirements()

    python = os.path.join(get_venv(), "bin", "python")
    run_command("Поднимаем PostgreSQL...", cmd="docker-compose up postgres")
    run_command("Запускаем миграцию...", "alembic upgrade head")

    os.system(f"{python} src/__main__.py --debug")


try:
    run()
except Exception as e:
    print(f"Проблема при запуске приложения: {e}")
    exit()
