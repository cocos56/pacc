"""雷电模拟器工程基类"""
import os

from ..adb import LDADB
from ..adb.ld_adb import get_online_devices
from ..config import Config


class LDProj:  # pylint: disable=too-few-public-methods
    """雷电模拟器的工程类"""
    def __init__(self):
        """构造函数"""
        os.chdir(Config.ld_work_path)

    @classmethod
    def get_status(cls):
        """获取所有雷电模拟器的当前状态"""
        for i in get_online_devices():
            adb_ins = LDADB(i)
            # uia_ins = NoxUIAutomator(i)
            adb_ins.get_current_focus()
            # uia_ins.getScreen()
            # uia_ins.getCurrentUIHierarchy()
