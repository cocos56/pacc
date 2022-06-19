import os
from shutil import rmtree
from ..nox import getOnlineDevices, NoxADB, NoxUIAutomator


class NoxProj:

    def __init__(self, nox_work_path=r'D:\Program Files\Nox\bin'):
        self.nox_work_path = nox_work_path
        os.chdir(self.nox_work_path)

    def clean_uia_files(self):
        """
        清理UIA文件
        """
        rmtree('%s/CurrentUIHierarchy' % self.nox_work_path)

    @classmethod
    def get_status(cls):
        for i in getOnlineDevices():
            adb_ins = NoxADB(i)
            uia_ins = NoxUIAutomator(i)
            adb_ins.getCurrentFocus()
            uia_ins.getScreen()
            uia_ins.getCurrentUIHierarchy()
