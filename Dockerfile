# https://testdriven.io/blog/docker-best-practices/


# Разбиваем сборку на этапы
# Каждая команда (слой) кэшируется докером; файлы, которые будут часто изменяться, нужно выполнять одними из последних
# поэтому команда с копированием файлов приложения (COPY . .) помещена вниз в этом файле

# Всегда размещай слои, которые могут измениться, как можно ниже в файле Dockerfile
# Объединяй команды RUN apt-get update и RUN apt-get install (это минимизирует количество слоёв)
# Если хочешь отключить кэширование для конкретной сборки Docker, добавь флаг --no-cache=True
# Используй легковесные базовые образы (-slim, -alpine)
# apt-get clean && rm -rf /var/lib/apt/lists/* - удаляет все списки пакетов и временные файлы

# --------------------------- temp stage
FROM python:3.12.2-slim as builder

# Запрещает Python записывать файлы pyc (__pycache__) на диск 
# Запрещает Python буферизировать stdout и stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# В файловой системе контейнера создаем папку с приложением
WORKDIR /app

# Обновляем пакеты, очищаем временные файлы
RUN pip install --no-cache-dir -U pip \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создаём виртуальное окружение
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем файл с зависимостями в контейнер
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt


# --------------------------- final stage
FROM python:3.12.2-slim

# В файловой системе контейнера создаем папку с приложением
WORKDIR /app

# Копируем окружение из предыдущего этапа
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копировать все из текущего каталога в папку с приложением в контейнере
COPY . .
# Запускаем main.py, внутри которого запускается uvicorn
CMD [ "python", "src/__main__.py" ]
