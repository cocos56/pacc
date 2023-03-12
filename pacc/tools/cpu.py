"""中央处理器（Central Processing Unit）模块"""
from psutil import cpu_percent

from ..base import sleep


class CPU:
    """中央处理器（Central Processing Unit）类"""

    @classmethod
    def is_idle(cls, threshold_value):
        """判断CPU是否处于空闲状态

        :param threshold_value: CPU利用率的最大阈值
        :return: CPU当前的利用率小于指定的阈值返回True，否则返回False
        """
        cpu_use = cpu_percent()
        print(f'cpu_use={cpu_use}, threshold_value={threshold_value}')
        return cpu_use < threshold_value

    @classmethod
    def wait_until_idle(cls, threshold_value=60, wait_time=5):
        """等待CPU处于空闲状态

        :param threshold_value: CPU利用率的最大阈值
        :param wait_time: 两次判断间的等待时间
        :return: CPU处于空闲状态时返回True，否则将一直等待至CPU处于空闲状态
        """
        while not cls.is_idle(threshold_value):
            sleep(wait_time)
        return True
