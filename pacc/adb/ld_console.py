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
    def quit(cls, dn_index):
        """关闭某一指定的雷电模拟器

        :param dn_index: 待关闭雷电模拟器的索引值
        """
        system(f'{LDC}quit --index {dn_index}')
        sleep(3)
        if cls.is_running(dn_index):
            print(f'检测到编号为{dn_index}的雷电模拟器未正常退出，正在重复执行退出操作')
            cls.quit(dn_index)
        print(f'编号为{dn_index}的雷电模拟器已正常退出')

    @classmethod
    def get_current_focus(cls, dn_index):
        """获取当前界面的Activity

        :param dn_index: 待获取界面Activity雷电模拟器的索引值
        """
        cmd = f'{LDC}adb --index {dn_index} --command ' \
              f'"shell dumpsys window windows" | findstr mCurrentFocus'
        res = popen(cmd).read()[2:-2]
        print(cmd)
        print(res)
        return res

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
        print(cmd)
        popen(cmd)
        sleep(5, False, False)
