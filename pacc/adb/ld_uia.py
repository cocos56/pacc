"""雷电自动化测试模块"""
from os import system, remove
from os.path import exists

from ..config import Config
from ..tools import create_dir, get_pretty_xml, get_xml


class NoxUIAutomator:
    def __init__(self, ip):
        self.ip = ip
        self.xml = ''

    def get_current_ui_hierarchy(self):
        system(f'adb -s {self.ip} shell rm /sdcard/window_dump.xml')
        cmd = f'adb -s {self.ip} shell uiautomator dump /sdcard/window_dump.xml'
        if Config.debug:
            print(cmd)
        system(cmd)
        dir_name = 'CurrentUIHierarchy'
        create_dir(dir_name)
        file_path = f"{dir_name}/{self.ip.replace('127.0.0.1:', '')}.xml"
        print(file_path)
        if exists(file_path):
            remove(file_path)
        system(f'adb -s {self.ip} pull /sdcard/window_dump.xml {file_path}')
        if Config.debug:
            return get_pretty_xml(file_path)
        return get_xml(file_path)
