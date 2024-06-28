import os
import logging

import inspect
import traceback

from pathlib import Path

from core.config import settings
from core.utils.logging.handlers import CustomRotatingFileHandler
from core.utils.logging.formatters import CustomFormatter
from core.utils.logging.filters import SensitiveDataFilter
from core.utils.tools.ansi_colors import ANSIColor


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

    - base_filename: имя файла, в который будет записан лог
    - subsystem: имя подсистемы, которая будет использоваться в имени папки для логов
    - file_prefix: префикс для имени файла
    - file_suffix: суффикс для имени файла
    - use_date_as_suffix: использовать дату в имени файла
    - date_suffix_format: формат даты в имени файла
    - show_traceback: показывать стек вызовов
    - level: уровень логирования
    - max_length: максимальная длина строки
    """

    def __init__(
        self,
        base_filename: str, 
        subsystem: str = "", 
        file_prefix: str | None = settings.logger.FILE_PREFIX,
        file_suffix: str | None = settings.logger.FILE_SUFFIX,
        use_date_as_suffix: bool = settings.logger.USE_DATE_AS_SUFFIX,
        date_suffix_format: str = settings.logger.DATE_SUFFIX_FORMAT,
        show_traceback: bool = settings.logger.SHOW_TRACEBACK,  # показывает стек вызовов
        level: int = settings.logger.LEVEL,
        max_length: int = settings.logger.MAX_LENGTH  # максимальная длина строки лога
    ):

        if settings.logger.IS_LOGGER_ENABLED:
            self.subsystem = subsystem
            self.base_filename = self._get_filename(base_filename)
            self.file_prefix = file_prefix
            self.file_suffix = file_suffix
            self.use_date_as_suffix = use_date_as_suffix
            self.date_suffix_format = date_suffix_format
            self.show_traceback = show_traceback
            self.level = level
            self.max_length = max_length

            # создает директорию, если не существует
            Path(os.path.join(settings.logger.DIR, self.subsystem)).mkdir(parents=True, exist_ok=True)
            self.log_file_path: str = os.path.join(settings.logger.DIR, self.subsystem, self.base_filename)

            self.logger = logging.getLogger(self._get_logger_id())
            self.logger.propagate = False  # не дублировать в корневой логгер
            self.logger.setLevel(level=self.level)
            self.logger.addFilter(SensitiveDataFilter(
                settings.logger.SENSITIVE_REGEX_PATTERNS,
                settings.logger.SENSITIVE_KEYS
            ))

            self.logger.addHandler(self._get_rotating_handler())
            self.logger.addHandler(self._get_console_handler())

    def _get_formatter(self, colorize: bool = True):
        """Создает форматтер для логов.

        Args:
            colorize (bool, optional): выполнять ли выделение строк цветом ANSI. По умолчанию True.

        Returns:
            `CustomFormatter`: кастомный форматтер логов.
        """
        id = self._get_logger_id()

        if colorize:
            format = f"%(asctime)s %(levelname)s ({ANSIColor.bright_magenta}{id}{ANSIColor.reset}) %(message)s"
            return CustomFormatter(format, max_length=self.max_length, colorize=True)
        else:
            format = f"%(asctime)s %(levelname)s ({id}) %(message)s"
            return CustomFormatter(format, max_length=self.max_length, colorize=False)

    def _get_filename(self, value: str):
        """Возвращает имя файла с добавлением расширения `.log`.

        Args:
            value (str): имя файла, переданное пользователем, которое может не содержать `.log`

        Returns:
            `str`: имя файла, переданное пользователем в параметре `value` с добавлением расширения `.log` в конце
        """
        if '.log' in value:
            return value
        else:
            return f"{value}.log"

    def _get_logger_id(self):
        """Создает уникальный идентификатор для логера.

        Returns:
            `str`: идентификатор логгера в формате `<подсистема>::<имя файла>`
        """
        filename = self._get_filename(self.base_filename)
        target = Path(filename).stem

        return f"{self.subsystem}::{target}"

    def _get_rotating_handler(self):
        """Создает обработчик вывода записей лога в файл.

        Returns:
            `CustomRotatingFileHandler`: кастомный обработчик вывода записей лога в файл
        """

        rotating_handler = CustomRotatingFileHandler(
            filename=self.log_file_path,
            file_prefix=self.file_prefix,
            file_suffix=self.file_suffix,
            use_date_as_suffix=self.use_date_as_suffix,
            date_suffix_format=self.date_suffix_format,
            maxBytes=settings.logger.FILE_LENGTH_LIMIT, 
            backupCount=settings.logger.BACKUPS_COUNT, 
            encoding="utf-8", 
            mode="a"
        )
        rotating_handler.setFormatter(self._get_formatter(colorize=False))

        return rotating_handler

    def _get_console_handler(self):
        """Создает обработчик вывода записей лога в консоль.

        Returns:
            `StreamHandler`: обработчик вывода записей лога в консоль.
        """
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._get_formatter(colorize=True))

        return console_handler

    def _get_traceback(self):
        """Получает стэк вызовов и форматирует его.

        Returns:
            `str`: форматированный стэк вызовов.
        """
        def format_line(line: str):
            f_result = []
            result = []
            splitted = line.split(',')
            for item in splitted:
                if 'File' in item:
                    new_item = item.replace('File', '').replace('"', '').strip()
                    f_result.append(new_item)
                elif 'line' in item:
                    item_splitted = item.strip().split(' ')
                    f_result.append(item_splitted[1])
                else:
                    result.append(item.strip())

            first = ':'.join(f_result)
            result.insert(0, first)

            return ', '.join(result)

        frame = inspect.currentframe()
        stack_trace = traceback.format_stack(frame)  # [-15:-2]
        clear_trace = list(filter(lambda x: '<frozen' not in x, stack_trace))
        clear_trace = clear_trace[:-3]

        for i, line in enumerate(clear_trace):
            new_line = line.strip().replace('\n', '')
            new_line = format_line(new_line)

            clear_trace[i] = new_line + '\n'

        clear_trace.insert(0, '\n')

        return ' -> '.join(clear_trace)

    def _display_trace(self):
        """Добавляет в лог стэк вызовов, если `self.show_traceback` = `True`
        """
        if self.show_traceback:
            trace = f"TRACEBACK:\n{self._get_traceback()}\n"
            self.logger.debug(trace)

    def info(self, msg, *args, **kwargs):
        if settings.logger.IS_LOGGER_ENABLED:
            self.logger.info(msg, *args, **kwargs)
            self._display_trace()

    def debug(self, msg, *args, **kwargs):
        if settings.logger.IS_LOGGER_ENABLED:
            self.logger.debug(msg, *args, **kwargs)
            self._display_trace()

    def error(self, msg, *args, **kwargs):
        if settings.logger.IS_LOGGER_ENABLED:
            self.logger.error(msg, *args, **kwargs)
            self._display_trace()

    def warn(self, msg, *args, **kwargs):
        if settings.logger.IS_LOGGER_ENABLED:
            self.logger.warn(msg, *args, **kwargs)
            self._display_trace()

    def warning(self, msg, *args, **kwargs):
        if settings.logger.IS_LOGGER_ENABLED:
            self.logger.warning(msg, *args, **kwargs)
            self._display_trace()

    def fatal(self, msg, *args, **kwargs):
        if settings.logger.IS_LOGGER_ENABLED:
            self.logger.fatal(msg, *args, **kwargs)
            self._display_trace()

    def critical(self, msg, *args, **kwargs):
        if settings.logger.IS_LOGGER_ENABLED:
            self.logger.critical(msg, *args, **kwargs)
            self._display_trace()

    def exception(self, msg, *args, **kwargs):
        if settings.logger.IS_LOGGER_ENABLED:
            self.logger.exception(msg, *args, **kwargs)
            self._display_trace()
