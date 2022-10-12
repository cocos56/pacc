"""雷电模拟器安卓调试桥模块"""
import os

from ..tools import find_all_with_re


def get_online_devices():
    """获取所有在线设备"""
    res = os.popen('adb devices').read()
    res = find_all_with_re(res, r'(127.0.0.1:.+)\tdevice')
    return res


class LDADB:  # pylint: disable=too-few-public-methods
    """雷电模拟器安卓调试桥类"""

    def __init__(self, ipv4_addr):
        """构造函数：初始化雷电模拟器安卓调试桥类的对象

        :param ipv4_addr: 目标设备的IPv4地址
        """
        self.ipv4_addr = ipv4_addr

    def get_current_focus(self):
        """获取当前界面的Activity"""
        cmd = f'adb -s {self.ipv4_addr} shell dumpsys window | findstr mCurrentFocus'
        res = os.popen(cmd).read()[2:-2]
        print(cmd)
        print(res)
        return res
