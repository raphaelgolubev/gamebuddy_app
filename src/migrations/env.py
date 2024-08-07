import alembic_postgresql_enum

from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context

import sys
sys.path = ['', '..', 'src', 'src/core'] + sys.path[1:]

import dotenv
# from src.core.config import settings


# возникла проблема с использованием pysettings. Проблема была в том, что
# в строку подключения попадали УСТАРЕВШИЕ значения, которые были взяты непонятно откуда
# то ли из кэшированного байт-кода, то ли еще откуда, хер его знает. 
# Поэтому решил брать данные напрямую из файла .env
def get_url():
    dotenv_file = dotenv.find_dotenv('.env')
    dotenv.load_dotenv()

    host = dotenv.get_key(dotenv_file, 'DB_HOST')
    port = dotenv.get_key(dotenv_file, 'DB_PORT')
    user = dotenv.get_key(dotenv_file, 'DB_USER')
    password = dotenv.get_key(dotenv_file, 'DB_PASSWORD')
    name = dotenv.get_key(dotenv_file, 'DB_NAME')

    # return settings.database.url
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


# Это объект конфигурации Alembic, который предоставляет
# доступ к значениям в используемом файле .ini.
config = context.config

# Интерпретация файла конфигурации для логирования Python.
# Эта строка настраивает логгеры.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# добавьте объект MetaData вашей модели здесь
# для поддержки 'autogenerate'
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

from entities.models.user import User # noqa
from entities.models.profile import Profile # noqa

from src.core.database.classes import Base

target_metadata = User.metadata

# другие значения из конфигурации, определенные потребностями env.py,
# могут быть получены:
# my_important_option = config.get_main_option("my_important_option")
# ... и т.д.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(get_url(), pool_pre_ping=True)

    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
