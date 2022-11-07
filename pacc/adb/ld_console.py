"""雷电模拟器控制台模块"""
from os import popen

from ..base import sleep
from ..config import LDC
from ..tools import system


class LDConsole:
    """雷电模拟器控制台类"""

    def __init__(self, dn_index):
        """构造函数：初始化雷电模拟器控制台类的对象

        :param dn_index: 雷电模拟器的索引
        """
        self.dn_index = dn_index

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
        # print(cmd)
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
        return self.dn_index in self.list()

    @classmethod
    def quit(cls, dn_index, print_flag=False):
        """关闭某一指定的雷电模拟器

        :param dn_index: 待关闭雷电模拟器的索引值
        :param print_flag: 是否打印正常退出的信息
        """
        if cls.is_running(dn_index):
            system(f'{LDC}quit --index {dn_index}')
            sleep(3)
            print_flag = True
        if cls.is_running(dn_index):
            print(f'检测到编号为{dn_index}的雷电模拟器未正常退出，正在重复执行退出操作')
            cls.quit(dn_index, print_flag=True)
        if print_flag:
            print(f'编号为{dn_index}的雷电模拟器已正常退出')

    @classmethod
    def is_running(cls, dn_index):
        """判断某一指定的雷电模拟器是否正在运行

        :param dn_index: 待关闭雷电模拟器的索引值
        """
        return popen(f'{LDC}isrunning --index {dn_index}').read() == 'running'

    def run_app(self, packagename):
        """启动雷电模拟器并自动打开某一指定的应用

        :param packagename: 待自动打开应用的包名
        """
        cmd = f'{LDC}launchex --index {self.dn_index} --packagename {packagename}'
        # print(cmd)
        popen(cmd)
        print(f'正在启动编号为{self.dn_index}的虚拟机')
        sleep(5, False, False)
