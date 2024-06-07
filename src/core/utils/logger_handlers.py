import os, time
import logging, logging.handlers
from pathlib import Path, PurePath


# здесь я просто переопределяю метод для модификации имени файла
class CustomRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """
    Обработчик для логгирования набора файлов, который переключается с одного файла
    на другой, когда текущий файл достигает определенного размера.
    """
    def __init__(
        self, 
        filename,
        file_prefix: str | None = None,
        file_suffix: str | None = None,
        use_date_as_suffix: bool = True,
        date_suffix_format: str = "_%Y-%m-%d",
        mode: str = "a", 
        maxBytes: int = 0,  # noqa: N803
        backupCount: int = 0, 
        encoding: str | None = None, 
        delay: bool = False, 
        errors: str | None = None
    ) -> None:
        """
        Откройте указанный файл и используйте его в качестве потока для ведения журнала.

        По умолчанию размер файла увеличивается бесконечно. Вы можете указать конкретные значения
        maxBytes и backupCount, чтобы файл мог обновляться до
        заданного размера.

        Переход происходит всякий раз, когда текущий файл журнала имеет размер, близкий к
        maxBytes. Если значение backupCount равно >= 1, система последовательно создаст
        новые файлы с тем же именем, что и у базового файла, но с расширениями
        к нему добавляются ".1", ".2" и т.д. Например, с резервным числом 5
        и базовое имя файла "app.log", вы получите "app.log",
        "app.1.log", "app.2.log", ... вплоть до "app.5.log". Файл, который
        всегда записывается в "app.log" - когда он заполняется, он закрывается
        и переименовывается в "app.1.log", и если файлы "app.1.log", "app.2.log" и т.д.
        существуют, затем они переименовываются в "app.2.log", "app.3.log" и т.д.
        соответственно.

        Если необходимо использовать другой формат для имени файла, используйте:

        - file_prefix - префикс для имени файла
        - file_suffix - суффикс для имени файла
        - use_date_as_suffix - использовать дату в имени файла
        - date_suffix_format - формат даты в имени файла

        Например:
        ```
        handler = CustomRotatingFileHandler(
             filename="my_log.log", 
             file_prefix="prefix_", 
             file_suffix="_suffix",
             use_date_as_suffix=True, 
             date_suffix_format="_%Y-%m-%d", 
             mode="a", 
             maxBytes=13, 
             backupCount=15, 
             encoding="utf-8", 
        ) -> None

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        for i in range(1, 5):
            logger.debug(f"Logger test {i}")
        ```
        В таком случае, после выполнения цикла будут созданы файлы
        ```
        "prefix_my_log_2024-06-07_suffix.1.log" - самые актуальные логи
        "prefix_my_log_2024-06-07_suffix.2.log"
        "prefix_my_log_2024-06-07_suffix.3.log"
        "prefix_my_log_2024-06-07_suffix.4.log" - самые старые логи
        ...
        ```
        если, например, текущая дата 7 июня 2024 года.

        Если значение maxBytes равно нулю, ролловер никогда не происходит.
        """
        super().__init__(filename, mode, maxBytes, backupCount, encoding, delay, errors)

        self.file_prefix = file_prefix
        self.file_suffix = file_suffix
        self.use_date_as_suffix = use_date_as_suffix
        self.date_suffix_format = date_suffix_format

    def _generate_filename(self, backup_number: int | None = None) -> str:
        base_filename = PurePath(self.baseFilename)
        pwd = base_filename.parent
        name = base_filename.stem
        ext = base_filename.suffix
        new_name = name

        if backup_number:
            ext = f".{backup_number}{ext}"

        if self.file_prefix:
            new_name = f"{self.file_prefix}{name}"
        if self.use_date_as_suffix:
            new_name += f"{time.strftime(self.date_suffix_format, time.localtime())}"
        if self.file_suffix:
            new_name += f"{self.file_suffix}"

        new_name = f"{new_name}{ext}"

        return PurePath(pwd).joinpath(new_name).as_posix()

    def doRollover(self):  # noqa: N802
        if self.stream:
            self.stream.close()
            self.stream = None

        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.rotation_filename(self._generate_filename(backup_number=i))
                dfn = self.rotation_filename(self._generate_filename(backup_number=i + 1))
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)

            dfn = self.rotation_filename(self._generate_filename(backup_number=1))

            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)

        if not self.delay:
            self.stream = self._open()
