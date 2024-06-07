import os
import logging

import inspect
import traceback

from pathlib import Path
import idna

from isort import file

from core.config import settings
from core.utils.logger_handlers import CustomRotatingFileHandler


class AppLogger:
    """
    Записывает строку лога в файл и выводит ее в терминал. Если размер файла
    превышает лимит, файл переименовывается и для записи открывается новый файл.
    Например, если лимит составляет 512 КБ и `base_filename` = `"app.log"`, тогда
    будет создан файл `"app.log"`:

    ```
    - app.log - 0 KB - самые актуальные данные
    ```

    Когда его размер станет равен 512 КБ - файл будет переименован в `"app.1.log"`, 
    а для записи будет открыт новый файл с именем `"app.log"`:

    ```
    - app.log - 0 KB - самые актуальные данные
    - app.1.log - 512 KB - бэкап
    ```

    Когда `"app.log"` снова будет переполнен, существующий на этот момент `"app.1.log"` 
    будет переименован в `"app.2.log"`, а `"app.log"` будет переименован в `"app.1.log"`
    и так далее:

    ```
    - app.log - 0 KB - самые актуальные данные
    - app.1.log - 512 KB - бэкап
    - app.2.log - 512 KB - бэкап - самые старые данные
    ```

    Таким образом выполняется бэкап файла. Логи всегда пишутся в файл `"app.log"`, устаревшие
    данные выносятся в файл `"app.N.log"`.

    >Примечание: на самом деле файл никогда не будет весить ровно 512 КБ, он будет иметь размер
    максимально близкий к лимиту, например 498 КБ или 505 КБ.

    - subsystem: имя подсистемы, которая будет использоваться в имени папки для логов
    - base_filename: имя файла, в который будет записан лог
    - file_prefix: префикс для имени файла
    - file_suffix: суффикс для имени файла
    - use_date_as_suffix: использовать дату в имени файла
    - date_suffix_format: формат даты в имени файла
    - use_debug_format: использовать дебаг информацию в логе
    - level: уровень логирования
    """

    def __init__(
        self,
        subsystem: str, 
        base_filename: str, 
        file_prefix: str | None = None,
        file_suffix: str | None = None,
        use_date_as_suffix: bool = True,
        date_suffix_format: str = "_%Y-%m-%d",
        use_debug_format: bool = True,
        level: int = settings.logger.LOG_LEVEL,
    ):

        self.subsystem = subsystem
        self.base_filename = self._get_filename(base_filename)
        self.file_prefix = file_prefix
        self.file_suffix = file_suffix
        self.use_date_as_suffix = use_date_as_suffix
        self.date_suffix_format = date_suffix_format
        self.use_debug_format = use_debug_format
        self.level = level

        self.formatter = self._get_formatter(with_debug_info=self.use_debug_format)

        # создает директорию, если не существует
        Path(os.path.join(settings.logger.LOGS_DIR, self.subsystem)).mkdir(parents=True, exist_ok=True)
        self.log_file_path: str = os.path.join(settings.logger.LOGS_DIR, self.subsystem, self.base_filename)

        self.logger = logging.getLogger(self._get_logger_id())
        self.logger.setLevel(level=self.level)

        self.logger.addHandler(self._get_rotating_handler())
        self.logger.addHandler(self._get_console_handler())

    def _get_formatter(self, with_debug_info: bool = False):
        if with_debug_info:
            format = "%(asctime)s [%(filename)s:%(lineno)s] %(levelname)s %(message)s"
        else:
            format = "%(asctime)s %(levelname)s %(message)s"

        return logging.Formatter(format)

    def _get_filename(self, value: str):
        if '.log' in value:
            return value
        else:
            return f"{value}.log"

    def _get_logger_id(self):
        filename = self._get_filename(self.base_filename)
        target = Path(filename).stem

        return f"{self.subsystem}::{target}"

    def _get_rotating_handler(self):
        rotating_handler = CustomRotatingFileHandler(
            filename=self.log_file_path,
            file_prefix=self.file_prefix,
            file_suffix=self.file_suffix,
            use_date_as_suffix=self.use_date_as_suffix,
            date_suffix_format=self.date_suffix_format,
            maxBytes=settings.logger.LOG_FILE_LENGTH_LIMIT, 
            backupCount=settings.logger.LOG_BACKUPS_COUNT, 
            encoding="utf-8", 
            mode="a"
        )
        rotating_handler.setFormatter(self.formatter)

        return rotating_handler

    def _get_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)

        return console_handler

    def _get_traceback(self):
        frame = inspect.currentframe()
        stack_trace = traceback.format_stack(frame)[-5:-2]
        stack_trace.insert(0, '\n')

        return ' -> '.join(stack_trace)

    def info(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        id = self._get_logger_id()
        trace = f"({id}) {msg}\n{self._get_traceback()}\n"
        self.logger.debug(trace, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.logger.warn(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        self.logger.fatal(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)
