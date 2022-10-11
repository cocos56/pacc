"""雷电模拟器控制台模块"""
from os import popen, system

from ..base import sleep

LDC = 'ldconsole.exe '


class LDConsole:
    """雷电模拟器控制台类"""

    def __init__(self, dn_index):
        self.dn_index = dn_index

    @classmethod
    def quit_all(cls):
        system(f'{LDC}quitall')
        sleep(13)

    def run_app(self, packagename):
        # launchex : 启动扩展命令(启动模拟器后自动打开某一应用)
        cmd = f'{LDC}launchex --index {self.dn_index} --packagename {packagename}'
        print(cmd)
        popen(cmd)
        sleep(5, False, False)
