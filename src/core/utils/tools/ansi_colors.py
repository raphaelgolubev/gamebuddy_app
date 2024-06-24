class ANSIColor:
    # цвета ANSI
    # https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html

    white = '\u001b[37m'
    blue = '\u001b[34m'
    green = '\u001b[32m'
    yellow = '\u001b[33m'
    red = '\u001b[31m'
    magenta = '\u001b[35m'
    cyan = '\u001b[36m'

    bright_blue = '\u001b[34;1m'
    bright_green = '\u001b[32;1m'
    bright_yellow = '\u001b[33;1m'
    bright_red = '\u001b[31;1m'
    bright_magenta = '\u001b[35;1m'
    bright_cyan = '\u001b[36;1m'

    background_white = '\u001b[47m'
    background_red = '\u001b[41m'
    background_green = '\u001b[42m'
    background_yellow = '\u001b[43m'
    background_blue = '\u001b[44m'
    background_magenta = '\u001b[45m'
    background_cyan = '\u001b[46m'

    background_bright_white = '\u001b[47;1m'
    background_bright_red = '\u001b[41;1m'
    background_bright_green = '\u001b[42;1m'
    background_bright_yellow = '\u001b[43;1m'
    background_bright_blue = '\u001b[44;1m'
    background_bright_magenta = '\u001b[45;1m'
    background_bright_cyan = '\u001b[46;1m'

    reset = '\u001b[0m'

    @staticmethod
    def color(text: str, color: str) -> str:
        return color + text + ANSIColor.reset
