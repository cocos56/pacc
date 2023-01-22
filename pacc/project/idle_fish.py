"""闲鱼中控模块"""
from .project import Project
from ..base import run_forever


class IdleFish(Project):
    """闲鱼中控类"""

    @run_forever
    def mainloop(self):
        """主循环函数"""
        self.adb_ins.get_current_focus()
