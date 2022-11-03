"""雷电模拟器安卓调试桥模块"""
from os import popen

from ..config import LDC


class LDADB:
    """雷电模拟器安卓调试桥类"""

    def __init__(self, dn_index):
        """构造函数：初始化雷电模拟器安卓调试桥类的对象

        :param dn_index: 雷电模拟器的索引
        """
        self.dn_index = dn_index

    def exe_cmd(self, command='', ext='', return_flag=False):
        """执行命令函数

        :param command: adb命令
        :param ext: 命令的扩展参数
        :param return_flag: 是否需要返回值，默认不需要
        """
        cmd = f'{LDC}adb --index {self.dn_index} --command "{command}"{ext}'
        print(cmd)
        if return_flag:
            return popen(cmd).read()
        return None

    def get_current_focus(self):
        """获取当前界面的Activity

        :return: 当前界面的Activity
        """
        res = self.exe_cmd('shell dumpsys window windows', ' | findstr mCurrentFocus', True)[2:-2]
        print(res)
        return res
