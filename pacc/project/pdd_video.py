"""拼多多视频模块"""
from random import randint

from .project import Project
from ..base import run_forever, sleep


class PddVideo(Project):
    """拼多多视频类"""

    @run_forever
    def mainloop(self):
        """主循环函数"""
        self.adb_ins.swipe((600, 1560), (600, 260))
        sleep(randint(12, 15))
        if 'com.xunmeng.pinduoduo/com.xunmeng.pinduoduo.ui.activity.HomeActivity' not in self.\
                adb_ins.get_current_focus():
            print('未检测到拼多多视频的活动，请手动处理')
            input()
            print('正在往下继续执行')
