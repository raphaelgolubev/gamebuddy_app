import logging
import re


class SensitiveDataFilter(logging.Filter):
    """Класс для фильтрации логов от чувствительных данных.
    """
    def __init__(
        self, 
        patterns: list[str], 
        sensitive_keys: tuple,
        name: str = ""
    ) -> None:
        """Создает экземпляр класса.

        Args:
            patterns (list[str]): regex-паттерны для маскирования секретных данных.
            sensitive_keys (tuple): ключи словарей, значения которых нужно маскировать.
            name (str, optional): имя логгера, события которого, как и его дочерние элементы, 
            будут пропущены через фильтр. Если имя не указано, разрешается каждое событие. По умолчнанию "".
        """
        super().__init__(name)

        self._patterns = patterns
        self._sensitive_keys = sensitive_keys

    def filter(self, record):
        try:
            record.args = self.mask_sensitive_args(record.args)
            record.msg = self.mask_sensitive_msg(record.msg)

            return True
        except Exception:
            return True

    def mask_sensitive_args(self, args):
        if isinstance(args, dict):
            new_args = args.copy()
            for key in args.keys():
                if key in self._sensitive_keys:
                    new_args[key] = "******"
                else:
                    # маскируем секретные данные в словаре
                    new_args[key] = self.mask_sensitive_msg(args[key])
            return new_args
        # когда несклько элементов в record.args
        return tuple([self.mask_sensitive_msg(arg) for arg in args])

    def mask_sensitive_msg(self, message):
        # маскируем секретные данные в нескольких элементах record.args
        if isinstance(message, dict):
            return self.mask_sensitive_args(message)
        if isinstance(message, str):
            for pattern in self._patterns:
                message = re.sub(pattern, "******", message)
            for key in self._sensitive_keys:
                pattern_str = rf"'{key}': '[^']+'"
                replace = f"'{key}': '******'"
                message = re.sub(pattern_str, replace, message)
        return message
