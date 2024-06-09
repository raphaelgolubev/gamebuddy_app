import logging
from tokenize import String

from core.utils.ansi_colors import ANSIColor
from core.utils.formatting import StringTool


class CustomFormatter(logging.Formatter):

    def __init__(self, fmt, max_length: int, colorize: bool = True):
        super().__init__()
        self.fmt = fmt
        self.max_length = max_length
        self.colorize = colorize

    def _format_colorize(self, format, record) -> str:
        format = format.replace('%(asctime)s', ANSIColor.white + '%(asctime)s' + ANSIColor.reset)

        match record.levelno:
            case logging.DEBUG: 
                format = format.replace(
                    '%(levelname)s', 
                    ANSIColor.background_bright_blue + ' %(levelname)s ' + ANSIColor.reset
                )
            case logging.INFO: 
                format = format.replace(
                    '%(levelname)s', 
                    ANSIColor.background_green + ' %(levelname)s ' + ANSIColor.reset
                )
            case logging.WARNING: 
                format = format.replace(
                    '%(levelname)s', 
                    ANSIColor.background_yellow + ' %(levelname)s ' + ANSIColor.reset
                )
            case logging.ERROR:
                format = format.replace(
                    '%(levelname)s', 
                    ANSIColor.background_red + ' %(levelname)s ' + ANSIColor.reset
                )
            case logging.CRITICAL:
                format = format.replace(
                    '%(levelname)s', 
                    ANSIColor.background_bright_red + ' %(levelname)s ' + ANSIColor.reset
                )
            case logging.FATAL:
                format = format.replace(
                    '%(levelname)s', 
                    ANSIColor.background_bright_red + ' %(levelname)s ' + ANSIColor.reset
                )
            case logging.WARN:
                format = format.replace(
                    '%(levelname)s', 
                    ANSIColor.background_yellow + ' %(levelname)s ' + ANSIColor.reset
                )
            case _:
                format = format.replace(
                    '%(levelname)s', 
                    ANSIColor.background_cyan + ' %(levelname)s ' + ANSIColor.reset
                )

        return format

    def _hightlight_syntax(self, text):
        txt_list = text.split('\n')
        result = []

        for line in txt_list:
            if '->' in line:
                splitted = line.split(',')
                path = splitted[0].strip().split('->')[1].strip()
                splitted[0] = f' -> {ANSIColor.bright_cyan}"{path}"{ANSIColor.reset}'

                result.append(' '.join(splitted))
            else:
                result.append(line)

        return '\n'.join(result)

    def _wrap_lines(self, text):
        txt_list = text.split('\n')
        result = []
        for line in txt_list:
            new_line = StringTool.wrap(line, self.max_length)
            result.append(new_line)

        return '\n'.join(result)

    def format(self, record):
        message = record.getMessage()
        message = self._hightlight_syntax(message) if self.colorize else message
        message = self._wrap_lines(message)
        # message = StringTool.wrap(message, self.max_length)

        new_record = logging.LogRecord(
            name=record.name,
            level=record.levelno,
            pathname=record.pathname,
            lineno=record.lineno,
            msg=message,
            args=record.args,
            exc_info=record.exc_info
        )

        if self.colorize:
            formatter = logging.Formatter(self._format_colorize(self.fmt, new_record))
            return formatter.format(new_record)
        else:
            formatter = logging.Formatter(self.fmt)
            return formatter.format(new_record)
