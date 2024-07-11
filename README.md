# GameBuddy API

``TODO: оформить readme.md``

**GameBuddy** - это приложение для людей, которые хотят найти тиммейтов для сетевых видеоигр.

- [Документация к проекту](/docs/APP.md) 


## Запуск

Перейти в корневой каталог и запустить приложение:

```bash
cd gamebuddy_app

docker-compose up postgres

alembic upgrade head

python src/__main__.py --debug
```