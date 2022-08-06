"""拼多多视频模块"""
from random import randint

from .project import Project
from ..base import run_forever, sleep


class PddVideo(Project):
    """拼多多视频类"""

    @run_forever
    def mainloop(self):
        self.adb_ins.swipe(600, 1860, 600, 360)
        sleep(randint(12, 15))
