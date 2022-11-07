"""雷电自动化测试模块"""
from os import system, remove
from os.path import exists

from .ld_base import LDBase
from ..base import sleep
from ..config import Config
from ..tools import create_dir, get_pretty_xml, get_xml


class LDUIA(LDBase):
    """雷电模拟器UI自动化测试类"""
    def __init__(self, dn_index):
        """构造函数

       :param dn_index: 雷电模拟器的索引
        """
        super().__init__(dn_index)
        self.ipv4_addr = ''
        self.xml = ''

    def tap(self, point, interval=1):
        """点击

        :param point: 点的x和y坐标
        :param interval: 停顿时间
        """
        x_coordinate, y_coordinate = point
        print(f'正在让编号为{self.dn_index}的模拟器点击({x_coordinate},{y_coordinate})')
        self.exe_cmd(f'shell input tap {x_coordinate} {y_coordinate}')
        sleep(interval, Config.debug, Config.debug)

    def get_screen(self):
        """获取屏幕（截屏）

        :return: 截图文件的路径
        """
        dir_name = 'CurrentUIHierarchy'
        create_dir(dir_name)
        png_path = f'{dir_name}/{self.dn_index}.png'
        self.exe_cmd(f'shell rm /sdcard/{self.dn_index}.png')
        self.exe_cmd(f'shell screencap -p /sdcard/{self.dn_index}.png')
        self.exe_cmd(f'pull /sdcard/{self.dn_index}.png CurrentUIHierarchy')
        sleep(1)
        return png_path

    def get_current_ui_hierarchy(self):
        """获取当前用户界面上元素的层次布局信息

        :return: 正常情况下会返回当前的用户界面上的元素的层次布局信息所构成的xml字符串，如果遇到异常则不做处理直接传递
        """
        system(f'adb -s {self.ipv4_addr} shell rm /sdcard/window_dump.xml')
        # pylint: disable=duplicate-code
        cmd = f'adb -s {self.ipv4_addr} shell uiautomator dump /sdcard/window_dump.xml'
        if Config.debug:
            print(cmd)
        system(cmd)
        dir_name = 'CurrentUIHierarchy'
        create_dir(dir_name)
        file_path = f"{dir_name}/{self.ipv4_addr.replace('127.0.0.1:', '')}.xml"
        print(file_path)
        if exists(file_path):
            remove(file_path)
        system(f'adb -s {self.ipv4_addr} pull /sdcard/window_dump.xml {file_path}')
        if Config.debug:
            return get_pretty_xml(file_path)
        return get_xml(file_path)
