FROM python:3.12.2-slim

# Запрещает Python записывать файлы pyc (__pycache__) на диск
ENV PYTHONDONTWRITEBYTECODE 1

# Запрещает Python буферизировать stdout и stderr
ENV PYTHONUNBUFFERED 1

# В файловой системе контейнера создаем папку с приложением
WORKDIR /gamebuddy_app

# Копируем зависимости
COPY requirements.txt /gamebuddy_app/requirements.txt

# Апгрейд pip и установка зависимостей
RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

# Копировать все из текущего каталога в папку с приложением в контейнере
COPY . /gamebuddy_app

# Запускаем main.py, внутри которого запускается uvicorn
CMD [ "python", "src/main.py" ]