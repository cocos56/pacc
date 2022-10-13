"""雷电模拟器工程基类"""
import os

from ..adb import LDADB
from ..adb.ld_adb import get_online_devices


class LDProj:
    """雷电模拟器的工程类"""
    def __init__(self, ld_work_path=r'F:\leidian\LDPlayer4'):
        """构造函数

        :param ld_work_path: 雷电模拟器的工作路径
        """
        self.ld_work_path = ld_work_path
        os.chdir(self.ld_work_path)

    @classmethod
    def get_status(cls):
        for i in get_online_devices():
            adb_ins = LDADB(i)
            # uia_ins = NoxUIAutomator(i)
            adb_ins.get_current_focus()
            # uia_ins.getScreen()
            # uia_ins.getCurrentUIHierarchy()
