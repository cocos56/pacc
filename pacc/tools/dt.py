"""时间模块"""
from datetime import datetime


class Datetime:
    """时间类"""
    startTime = datetime.now()

    @classmethod
    def getRunTime(cls):
        return datetime.now() - cls.startTime


def showDatetime(text):
    print("现在是：%s，正在执行%s，已运行%s\n" % (datetime.now(), text, Datetime.getRunTime()))
