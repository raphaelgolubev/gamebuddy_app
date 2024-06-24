class StringTool:
    @staticmethod
    def is_empty(s):
        return s is None or s == ''

    @staticmethod
    def get_last_space(text: str, max_length: int):
        txt_list = list(text)
        for i in range(len(text) - 1, 0, -1):
            if txt_list[i].isspace() and i < max_length:
                return i

        return -1

    @staticmethod
    def get_first_space(text: str, max_length: int):
        txt_list = list(text)
        for i in range(0, len(text) - 1):
            if txt_list[i].isspace():
                return i

        return -1

    # ----------------------------------|
    # ----------------------------------|
    # ----------------------------------*
    # Создание async_engine: url='postgresql+asyncpg://postgres:postgres@192.168.1.101:5432/postgres' config={'echo': True, 'pool_size': 10, 'max_overflow': 10} # noqa

    # Создание async_engine:

    # ----------------------------------|------------------------------------------------------------------------------------------------|
    # ----------------------------------|------------------------------------------------------------------------------------------------|
    # ----------------------------------*------------------------------------------------------------------------------------------------*
    # url='postgresql+asyncpg://postgres:postgres@192.168.1.101:5432/postgres' config={'echo': True, 'pool_size': 10, 'max_overflow': 10} # noqa

    @staticmethod
    def wrap(text: str, max_length: int):
        length = len(text)
        result = text
        if length > max_length:
            index = StringTool.get_last_space(text, max_length)

            if index == -1:
                result = text[:max_length] + '\n' + StringTool.wrap(text[max_length:], max_length)
            else:
                left = StringTool.wrap(text[:index], max_length)
                right = StringTool.wrap(text[index + 1:], max_length)
                result = left + '\n' + right

        return result
