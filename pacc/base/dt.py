"""时间模块"""
from datetime import datetime

from ..config import Language


# pylint: disable=too-few-public-methods
class Datetime:
    """时间类"""
    start_time = datetime.now()

    @classmethod
    def get_run_time(cls):
        """获取程序自启动以来已运行的时间"""
        return datetime.now() - cls.start_time


def show_datetime(text: str, language=Language.CH, start_br=False):
    """打印程序自启动以来已运行的时间"""
    if language == Language.CH:
        if start_br:
            print(f'\n现在是：{datetime.now()}，正在执行{text}，已运行{Datetime.get_run_time()}\n')
        else:
            print(f'现在是：{datetime.now()}，正在执行{text}，已运行{Datetime.get_run_time()}\n')
    elif language == Language.EN:
        if start_br:
            print(f'\nNow is: {datetime.now()}, executing {text}, it has been running for '
                  f'{Datetime.get_run_time()}')
        else:
            print(f'Now is: {datetime.now()}, executing {text}, it has been running for '
                  f'{Datetime.get_run_time()}\n')
