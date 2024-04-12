# Памятка для разработчика (меня)

## Работа с Docker
- ``docker system prune`` - почистить копии контейнеров и кэш
- ``docker ps -a`` - список всех контейнеров
- ``docker-compose up --build`` - собрать и запустить контейнеры
- ``docker exec -it <id контейнера> bash <команда>`` - запуск команды
- ``docker exec -it <id контейнера> python -c "import sys; print(sys.path)"`` - проверить пути
- ``docker down`` - удалить контейнеры
- ``docker down -v`` - удалить все контейнеры и volumes
- ``docker images`` - список всех контейнеров
- ``${VARIABLE_NAME}`` - в ``docker-compose.yml`` таким образом можно указать переменные из файла ``.env``
### Postgres
- ``docker exec -it <id контейнера postgres> psql -U postgres`` - провалиться внутрь postgres контейнера

## Чекнуть
- dev контейнеры в vscode чекнуть
- pydantic settings чекнуть