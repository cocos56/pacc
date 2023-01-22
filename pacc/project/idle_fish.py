"""闲鱼中控模块"""
from .project import Project
from ..base import run_forever, sleep

ROOT = 'com.taobao.idlefish/com.taobao.idlefish.maincontainer.activity.'


class Activity:  # pylint: disable=too-few-public-methods
    """闲鱼中控模块的安卓活动名类"""
    MainActivity = f'{ROOT}MainActivity'  # 主界面


class ResourceID:  # pylint: disable=too-few-public-methods
    """闲鱼中控模块的安卓资源ID类"""
    tab_title = 'com.taobao.idlefish:id/tab_title'


class IdleFish(Project):
    """闲鱼中控类"""

    def open_app(self):
        """打开闲鱼APP"""
        self.free_memory()
        self.adb_ins.open_app(Activity.MainActivity)
        sleep(3)

    @run_forever
    def mainloop(self):
        """主循环函数"""
        self.open_app()
        self.adb_ins.get_current_focus()
        self.uia_ins.click(content_desc='我的，未选中状态')
        self.uia_ins.get_current_ui_hierarchy()
        sleep(1000)
