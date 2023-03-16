"""BlackBox中控模块"""
from .project import Project
from ..base import sleep

ROOT = 'top.niunaijun.blackboxa64/top.niunaijun.blackboxa.view.main.'


class Activity:  # pylint: disable=too-few-public-methods
    """BlackBox中控模块的安卓活动名类"""
    MainActivity = f'{ROOT}MainActivity'  # 主界面


class ResourceID:  # pylint: disable=too-few-public-methods
    """BlackBox中控模块的安卓资源ID类"""
    toolbar_layout = 'top.niunaijun.blackboxa64:id/toolbar_layout'


class BlackBox(Project):
    """BlackBox中控类"""

    def open_app(self) -> None:
        """打开BlackBox应用"""
        self.free_memory()
        self.adb_ins.open_app(Activity.MainActivity)
        sleep(5)

    def get_name(self):
        """获取名字"""
