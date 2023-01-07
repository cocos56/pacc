"""雷电模拟器基类"""
# pylint: disable=redefined-builtin
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from os import popen, system
from datetime import datetime
from time import sleep

from ..base import print_err
from ..config import LDC
from .ld_console import LDConsole


class LDBase:  # pylint: disable=too-few-public-methods
    """雷电模拟器基类"""

    def __init__(self, ld_index):
        """构造函数：初始化雷电模拟器安卓调试桥类的对象

        :param ld_index: 雷电模拟器的索引
        """
        self.ld_index = ld_index
        self.end_flag = False

    def timeout_monitoring(self, start_datetime, timeout=15):
        """超时监控

        :param start_datetime: 开始时间
        :param timeout: 超时退出时间，默认12秒
        """
        used_datetime = datetime.now()-start_datetime
        print(f'{self.ld_index} timeout_monitoring starting : used_datetime.seconds='
              f'{used_datetime.seconds}s')
        while used_datetime.seconds < timeout and not self.end_flag:
            sleep(1)
            used_datetime = datetime.now() - start_datetime
            print(f'{self.ld_index} timeout_monitoring: used_datetime={used_datetime}s')
        if self.end_flag:
            print(f'{self.ld_index} timeout_monitoring: 无需处理')
            return True
        print(f'{self.ld_index} timeout_monitoring: 检测到设备{self.ld_index}于{datetime.now()}'
              f'超时未响应，需要该设备关闭')
        LDConsole.quit(self.ld_index)

    def sys_run(self, command, ext=''):
        """使用system运行命令函数

        :param command: adb命令
        :param ext: 命令的扩展参数
        :return: 成功执行（未超时中断）返回True，否则返回False
        """
        return self.exe_cmd(command, ext, return_flag=False)

    def popen_run(self, command, ext=''):
        """使用popen运行命令函数

        :param command: adb命令
        :param ext: 命令的扩展参数
        :return: 成功执行（未超时中断）返回从管道中读取的结果，否则返回False
        """
        return self.exe_cmd(command, ext)

    def exe_cmd(self, command='', ext='', timeout=12, return_flag=True):
        """执行命令函数

        :param command: adb命令
        :param ext: 命令的扩展参数
        :param timeout: 超时中断时间，默认9秒
        :param return_flag: 是否需要返回值，默认不需要
        :return: 成功执行（未超时中断）返回从管道中读取的结果或True，否则返回False
        """
        pool = ThreadPoolExecutor(max_workers=2)
        cmd = f'{LDC}adb --index {self.ld_index} --command "{command}"{ext}'
        print(cmd)
        start_datetime = datetime.now()
        self.end_flag = False
        if return_flag:
            future = pool.submit(popen, cmd)
        else:
            future = pool.submit(system, cmd)
        pool.submit(self.timeout_monitoring, start_datetime)
        try:
            if return_flag:
                res = future.result(timeout=timeout).read()
            else:
                future.result(timeout=timeout)
                res = True
            self.end_flag = True
            print(datetime.now()-start_datetime)
            pool.shutdown()
            return res
        except TimeoutError:
            LDConsole.quit(self.ld_index)
            self.end_flag = True
            print_err(f'线程{future}因超{timeout}秒而强制终止')
            pool.shutdown()
            return False
