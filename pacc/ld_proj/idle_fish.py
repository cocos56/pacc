"""咸鱼全自动刷咸鱼币中央监控系统模块"""
from .ld_proj import LDProj
from ..adb.ld_console import LDConsole


# pylint: disable=too-few-public-methods
class Activity:
    """咸鱼全自动刷咸鱼币中央监控系统模块的安卓活动名类"""
    MainActivity = 'com.taobao.idlefish/com.taobao.idlefish.maincontainer.activity.MainActivity'


class IdleFish(LDProj):
    """含羞草传媒模块"""

    def __init__(self, start_index=0):
        super().__init__()
        self.start_index = start_index

    def run_app(self):
        LDConsole(self.start_index).run_app('com.taobao.idlefish')
