import socket
import platform
import os
import subprocess
import shutil
import dotenv


def echo(message: str):
    print(f"> {message}")


def get_pwd() -> str:
    result = run_command(label="", cmd="pwd", output=False)
    return result.stdout.decode("utf-8").rstrip()


def get_venv() -> str:
    return os.path.join(get_pwd(), "venv")


def run_command(label: str, cmd: str, output: bool = True, check: bool = True):
    task = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)

    if len(label) > 0:
        echo(label)
    if output:
        echo(task.stdout.decode("utf-8"))

    return task


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


def check_docker():
    echo("Ожидаем запуск docker...")
    while True:
        # echo("Docker все еще не запущен...")
        task = run_command("", cmd="pgrep -l Docker", output=False, check=False)
        if task.returncode == 0:
            echo("Docker запустился")
            break

    return True


def run_docker():
    try:
        run_command("Проверяем docker", cmd="pgrep -l Docker", output=False)
    except Exception:
        if platform.system() == "Darwin":
            run_command("Запускаем docker...", "open -a Docker")
        elif platform.system() == "Windows":
            print("Windows pass")
        elif platform.system() == "Linux":
            print("Linux pass")
        else:
            raise Exception("Запустите docker перед запуском этого скрипта")
    else:
        print("Docker запущен")


def get_ipv4():
    local_hostname = socket.gethostname()
    ip_addresses = socket.gethostbyname_ex(local_hostname)[2]
    filtered_ips = [ip for ip in ip_addresses if not ip.startswith("127.")]
    first_ip = filtered_ips[:1]

    return first_ip[0]


def create_env_file():
    if os.path.exists(".env"):
        fill_env()
    else:
        shutil.copyfile(".env.example", ".env")
        fill_env()


def input_env(value: str, default: str):
    output = input(value)
    if len(output) > 0:
        return output
    else:
        return default


def fill_env():
    uvicorn_port = input_env("Введите порт Uvicorn (пропустите если 8000): ", default="8000")

    db_port = input_env("Введите порт PostgreSQL (пропустите если 5432): ", default="5432")
    db_name = input_env("Введите название БД PostgreSQL (пропустите если 'postgres'): ", default="postgres")
    db_user = input_env("Введите пользователя БД PostgreSQL (пропустите если 'postgres'): ", default="postgres")
    db_password = input_env("Введите пароль БД PostgreSQL (пропустите если 'postgres'): ", default="postgres")

    dotenv_file = dotenv.find_dotenv('.env')
    dotenv.load_dotenv()

    dotenv.set_key(dotenv_file, 'UVICORN_PORT', uvicorn_port, quote_mode='never')

    dotenv.set_key(dotenv_file, 'DB_PORT', db_port, quote_mode='never')
    dotenv.set_key(dotenv_file, 'DB_HOST', get_ipv4())
    dotenv.set_key(dotenv_file, 'DB_NAME', db_name)
    dotenv.set_key(dotenv_file, 'DB_USER', db_user)
    dotenv.set_key(dotenv_file, 'DB_PASSWORD', db_password)


def run():
    create_venv()
    install_requirements()

    create_env_file()

    run_docker()

    if check_docker():
        python = os.path.join(get_venv(), "bin", "python")
        echo("Запускаем postgres...")
        os.system("docker-compose --log-level ERROR up postgres -d --build")
        echo("Запускаем alembic...")
        os.system("venv/bin/alembic upgrade head")
        echo("Запускаем сервер...")
        os.system(f"{python} src/__main__.py --debug")


try:
    run()
except Exception as e:
    print(f"Проблема при запуске приложения: {e}")
    exit()
