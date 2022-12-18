"""雷电模拟器基类"""
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from os import popen, system
from datetime import datetime

from ..base import print_err
from ..config import LDC


class LDBase:  # pylint: disable=too-few-public-methods
    """雷电模拟器基类"""

    def __init__(self, ld_index):
        """构造函数：初始化雷电模拟器安卓调试桥类的对象

        :param ld_index: 雷电模拟器的索引
        """
        self.ld_index = ld_index

    def sys_run(self, command='', ext='', timeout=2):
        """使用system运行命令函数（带超时强制中断功能）

        :param command: adb命令
        :param ext: 命令的扩展参数
        :param timeout: 超时中断时间，默认2秒
        """
        pool = ThreadPoolExecutor(max_workers=1)
        cmd = f'{LDC}adb --index {self.ld_index} --command "{command}"{ext}'
        print(cmd)
        start_datetime = datetime.now()
        future = pool.submit(system, cmd)
        try:
            future.result(timeout=timeout)
            print(datetime.now()-start_datetime)
        except TimeoutError:
            pool.shutdown()
            print_err(f'线程{future}因超{timeout}秒而强制终止')

    def run_cmd(self, command='', ext=''):
        """运行命令函数

        :param command: adb命令
        :param ext: 命令的扩展参数
        """
        cmd = f'{LDC}adb --index {self.ld_index} --command "{command}"{ext}'
        print(cmd)
        popen(cmd)

    def exe_cmd(self, command='', ext='', return_flag=False):
        """执行命令函数

        :param command: adb命令
        :param ext: 命令的扩展参数
        :param return_flag: 是否需要返回值，默认不需要
        """
        cmd = f'{LDC}adb --index {self.ld_index} --command "{command}"{ext}'
        print(cmd)
        if return_flag:
            return popen(cmd).read()
        system(cmd)
        return None
