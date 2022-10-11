"""咸鱼全自动刷咸鱼币中央监控系统模块"""
from .ld_proj import LDProj
from ..adb.ld_console import LDConsole
from ..base import run_forever


# pylint: disable=too-few-public-methods
class Activity:
    """咸鱼全自动刷咸鱼币中央监控系统模块的安卓活动名类"""
    MainActivity = 'com.taobao.idlefish/com.taobao.idlefish.maincontainer.activity.MainActivity'


class IdleFish(LDProj):
    """含羞草传媒模块"""

    def __init__(self, start_index=1):
        super().__init__()
        self.start_index = start_index

    def run_app(self):
        LDConsole(self.start_index).run_app('com.taobao.idlefish')

    def enter_my_interface(self):
        """进入我的界面"""

    @classmethod
    @run_forever
    def mainloop(cls, start_index=1):
        """主循环"""
        LDConsole.quit_all()
        cls(start_index).run_app()
        print('请按回车键以继续')
        input()
        start_index += 1
