"""雷电自动化测试模块"""
from os import remove
from os.path import exists

from .ld_base import LDBase
from ..base import sleep
from ..config import Config
from ..tools import create_dir, get_pretty_xml, get_xml


class LDUIA(LDBase):
    """雷电模拟器UI自动化测试类"""
    def __init__(self, ld_index):
        """构造函数

       :param ld_index: 雷电模拟器的索引
        """
        super().__init__(ld_index)
        self.xml = ''

    def tap(self, point, interval=1):
        """点击

        :param point: 点的x和y坐标
        :param interval: 停顿时间
        """
        x_coordinate, y_coordinate = point
        print(f'正在让编号为{self.ld_index}的模拟器点击({x_coordinate},{y_coordinate})')
        self.exe_cmd(f'shell input tap {x_coordinate} {y_coordinate}')
        sleep(interval, Config.debug, Config.debug)

    def get_screen(self):
        """获取屏幕（截屏）

        :return: 截图文件的路径
        """
        dir_name = 'CurrentUIHierarchy'
        create_dir(dir_name)
        png_path = f'{dir_name}/{self.ld_index}.png'
        self.exe_cmd(f'shell rm /sdcard/{self.ld_index}.png')
        self.exe_cmd(f'shell screencap -p /sdcard/{self.ld_index}.png')
        self.exe_cmd(f'pull /sdcard/{self.ld_index}.png CurrentUIHierarchy')
        sleep(1)
        return png_path

    def get_current_ui_hierarchy(self):
        """获取当前用户界面上元素的层次布局信息

        :return: 正常情况下会返回当前的用户界面上的元素的层次布局信息所构成的xml字符串，如果遇到异常则不做处理直接传递
        """
        self.exe_cmd(f'shell rm /sdcard/window_dump.xml')
        self.exe_cmd(f'shell uiautomator dump /sdcard/window_dump.xml')
        dir_name = 'CurrentUIHierarchy'
        create_dir(dir_name)
        file_path = f"{dir_name}/{self.ld_index}.xml"
        print(file_path)
        if exists(file_path):
            remove(file_path)
        self.exe_cmd(f'pull /sdcard/window_dump.xml {file_path}')
        if Config.debug:
            return get_pretty_xml(file_path)
        return get_xml(file_path)
