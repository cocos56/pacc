"""时间模块"""
from datetime import datetime


# pylint: disable=too-few-public-methods
class Datetime:
    """时间类"""
    start_time = datetime.now()

    @classmethod
    def get_run_time(cls):
        """获取程序自启动以来已运行的时间"""
        return datetime.now() - cls.start_time


def show_datetime(text):
    """打印程序自启动以来已运行的时间"""
    print(f"\n现在是：{datetime.now()}，正在执行{text}，已运行{Datetime.get_run_time()}")
