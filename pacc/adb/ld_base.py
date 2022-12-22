"""雷电模拟器基类"""
# pylint: disable=redefined-builtin
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from os import popen, system
from datetime import datetime

from ..base import print_err, sleep
from ..config import LDC


class LDBase:  # pylint: disable=too-few-public-methods
    """雷电模拟器基类"""

    def __init__(self, ld_index):
        """构造函数：初始化雷电模拟器安卓调试桥类的对象

        :param ld_index: 雷电模拟器的索引
        """
        self.ld_index = ld_index

    def timeout_monitoring(self, start_datetime, timeout=10):
        """超时监控

        :param start_datetime: 开始时间
        :param timeout: 超时退出时间，默认10秒
        """
        used_datetime = datetime.now()-start_datetime
        while used_datetime < timeout:
            sleep(1)
            used_datetime = datetime.now() - start_datetime
            print(f'{self.ld_index} timeout_monitoring: used_datetime={used_datetime}s')

    def sys_run(self, command='', ext='', timeout=5):
        """使用system运行命令函数（带超时强制中断功能）

        :param command: adb命令
        :param ext: 命令的扩展参数
        :param timeout: 超时中断时间，默认5秒
        :return: 成功执行（未超时中断）返回True，否则返回False
        """
        pool = ThreadPoolExecutor(max_workers=2)
        cmd = f'{LDC}adb --index {self.ld_index} --command "{command}"{ext}'
        print(cmd)
        start_datetime = datetime.now()
        future = pool.submit(system, cmd)
        pool.submit(self.timeout_monitoring, start_datetime)
        try:
            future.result(timeout=timeout)
            print(datetime.now()-start_datetime)
        except TimeoutError:
            pool.shutdown()
            print_err(f'线程{future}因超{timeout}秒而强制终止')
            return False
        pool.shutdown()
        return True

    def popen_run(self, command='', ext='', timeout=5):
        """运行命令函数

        :param command: adb命令
        :param ext: 命令的扩展参数
        :param timeout: 超时中断时间，默认5秒
        """
        pool = ThreadPoolExecutor(max_workers=2)
        cmd = f'{LDC}adb --index {self.ld_index} --command "{command}"{ext}'
        print(cmd)
        start_datetime = datetime.now()
        future = pool.submit(popen, cmd)
        pool.submit(self.timeout_monitoring, start_datetime)
        try:
            res = future.result(timeout=timeout).read()
            print(datetime.now()-start_datetime)
            pool.shutdown()
            return res
        except TimeoutError:
            pool.shutdown()
            print_err(f'线程{future}因超{timeout}秒而强制终止')
            return False

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
