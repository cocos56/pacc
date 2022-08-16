"""快手极速版主循环模块"""
from ...base import run_forever


# pylint: disable=too-few-public-methods
class KsjsbMainloop:
    """快手极速版主循环类"""

    @classmethod
    @run_forever
    def run(cls):
        """开始运行"""
