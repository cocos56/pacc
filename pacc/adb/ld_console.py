"""雷电模拟器控制台模块"""
from os import popen

from ..base import sleep


class LDConsole:
    """雷电模拟器控制台类"""

    def __init__(self, dn_index):
        self.dn_index = dn_index

    def run_app(self, packagename):
        cmd = f'ldconsole.exe runapp --index {self.dn_index} --packagename {packagename}'
        print(cmd)
        popen(cmd)
        sleep(5, False, False)
