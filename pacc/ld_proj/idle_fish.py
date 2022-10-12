"""咸鱼全自动刷咸鱼币中央监控系统模块"""
from .ld_proj import LDProj
from ..adb import LDADB
from ..adb.ld_adb import get_online_devices
from ..adb.ld_console import LDConsole
from ..base import sleep


# pylint: disable=too-few-public-methods
class Activity:
    """咸鱼全自动刷咸鱼币中央监控系统模块的安卓活动名类"""
    MainActivity = 'com.taobao.idlefish/com.taobao.idlefish.maincontainer.activity.MainActivity'


class IdleFish(LDProj):
    """咸鱼模块"""

    def __init__(self, start_index=1):
        super().__init__()
        self.start_index = start_index

    def run_app(self):
        LDConsole(self.start_index).run_app('com.taobao.idlefish')

    def enter_my_interface(self):
        """进入我的界面"""

    @classmethod
    def mainloop(cls, start_index, end_index):
        """主循环

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        while True:
            cls(start_index).run_app()
            sleep(90)
            adb_ins = LDADB(get_online_devices()[0])
            if 'Application Not Responding: com.taobao.idlefish' in adb_ins.get_current_focus():
                print('检测到咸鱼无响应，正在重启模拟器')
                LDConsole.quit(start_index)
                cls(start_index).run_app()
                sleep(90)
            sleep(210)
            LDConsole.quit(start_index)
            print(f'第{start_index}项已执行完毕')
            if start_index >= end_index:
                print(f'所有共{end_index-src_start_index+1}项已执行完毕')
                input()
            start_index += 1
