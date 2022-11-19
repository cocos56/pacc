"""雷电模拟器控制台模块"""
from os import popen, system

from ..base import sleep
from ..config import LDC


class LDConsole:
    """雷电模拟器控制台类"""

    def __init__(self, ld_index):
        """构造函数：初始化雷电模拟器控制台类的对象

        :param ld_index: 雷电模拟器的索引
        """
        self.ld_index = ld_index

    @classmethod
    def quit_all(cls):
        """关闭所有雷电模拟器"""
        system(f'{LDC}quitall')
        sleep(6)

    @classmethod
    def list(cls):
        """获取所有虚拟机的列表

        :return: 字典，键是索引值，值是虚拟机名
        """
        cmd = f'{LDC}list2'
        res = popen(cmd).read()[:-1]
        res = [(int(i[0]), i[1]) for i in [i.split(',')[:2] for i in res.split()[:-1]]]
        # print(res, len(res))
        dic = dict(res)
        # print(dic)
        return dic

    def is_exist(self):
        """判断虚拟机是否存在

        :return: 布尔值，存在返回True，否则返回False
        """
        return self.ld_index in self.list()

    def get_name(self):
        """获取虚拟机名"""
        return self.list().get(self.ld_index)

    def launch(self):
        """启动某一指定的雷电模拟器"""
        cmd = f'{LDC}launch --index {self.ld_index}'
        # print(cmd)
        popen(cmd)
        print(f'正在启动模拟器{self.ld_index}')
        sleep(5, False, False)

    @classmethod
    def quit(cls, ld_index, print_flag=False):
        """关闭某一指定的雷电模拟器

        :param ld_index: 待关闭雷电模拟器的索引值
        :param print_flag: 是否打印正常退出的信息
        """
        if cls.is_running(ld_index):
            print(f'正在退出模拟器{ld_index}')
            system(f'{LDC}quit --index {ld_index}')
            sleep(3)
            print_flag = True
        if cls.is_running(ld_index):
            print(f'检测到模拟器{ld_index}未正常退出，正在重复执行退出操作')
            return cls.quit(ld_index, print_flag=True)
        if print_flag:
            print(f'模拟器{ld_index}已正常退出')
        return True

    @classmethod
    def is_running(cls, ld_index):
        """判断某一指定的雷电模拟器是否正在运行

        :param ld_index: 待关闭雷电模拟器的索引值
        """
        return popen(f'{LDC}isrunning --index {ld_index}').read() == 'running'

    def run_app(self, packagename):
        """启动雷电模拟器并自动打开某一指定的应用

        :param packagename: 待自动打开应用的包名
        """
        cmd = f'{LDC}launchex --index {self.ld_index} --packagename {packagename}'
        # print(cmd)
        popen(cmd)
        print(f'正在启动模拟器{self.ld_index}并开启应用{packagename}')
        sleep(5, False, False)
