"""打印模块"""


def print_error(info):
    """打印错误信息

    :param info: 待打印的信息
    """
    print(f'\033[0;31m{info}\033[0m')
