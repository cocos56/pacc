"""趣头条中央控制系统模块"""
from .project import Project
from ..base import run_forever, sleep


# pylint: disable=too-few-public-methods
class Activity:
    """趣头条中央控制系统模块的安卓活动名类"""
    MainActivity = 'com.jifen.qukan/com.jifen.qkbase.main.MainActivity'


# pylint: disable=too-few-public-methods
class ResourceID:
    """趣头条中央控制系统模块的安卓资源ID类"""
    ch1 = "com.jifen.qukan:id/ch1"


# pylint: disable=too-few-public-methods
class Qtt(Project):
    """趣头条中央控制系统类"""

    def open_app(self):
        """打开趣头条APP"""
        print('正在打开快手极速版APP')
        self.adb_ins.open_app(Activity.MainActivity)
        sleep(16)

    def view_ads_video(self):
        self.reopen_app()
        self.uia_ins.get_current_ui_hierarchy()

    @run_forever
    def mainloop(self):
        """趣头条中央控制系统类的主循环成员方法"""
