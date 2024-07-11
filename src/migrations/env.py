from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.core.config import settings

from entities.models.user import User # noqa
# from src.modules.profile.models import Profile # noqa

from src.core.database.classes import Base

# Это объект конфигурации Alembic, который предоставляет
# доступ к значениям в используемом файле .ini.
config = context.config

# Переопределяем URL для подключения к базе данных
config.set_main_option('sqlalchemy.url', settings.database.url)  # + "?async_fallback=True")

# Интерпретация файла конфигурации для логирования Python.
# Эта строка настраивает логгеры.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# добавьте объект MetaData вашей модели здесь
# для поддержки 'autogenerate'
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

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
    url = config.get_main_option("sqlalchemy.url")
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

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
