"""闲鱼中控模块"""
from .project import Project
from ..base import run_forever


class PddVideo(Project):
    """拼多多视频类"""

    @run_forever
    def mainloop(self):
        """主循环函数"""
