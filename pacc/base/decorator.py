"""装饰器模块"""


def run_forever(func):
    """一直运行"""
    def wrapper(*args):
        while True:
            func(*args)
    return wrapper
