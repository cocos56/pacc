"""雷电自动化测试模块"""
from os import system, remove
from os.path import exists

from ..config import Config
from ..tools import create_dir, get_pretty_xml, get_xml


class LDUIAutomator:  # pylint: disable=too-few-public-methods
    """雷电模拟器UI自动化测试类"""
    def __init__(self, ipv4_addr):
        """构造函数

        :param ipv4_addr: 目标设备的IPv4地址
        """
        self.ipv4_addr = ipv4_addr
        self.xml = ''

    # pylint: disable=duplicate-code
    def get_current_ui_hierarchy(self):
        """获取当前用户界面上元素的层次布局信息

        :return: 正常情况下会返回当前的用户界面上的元素的层次布局信息所构成的xml字符串，如果遇到异常则不做处理直接传递
        """
        system(f'adb -s {self.ipv4_addr} shell rm /sdcard/window_dump.xml')
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
