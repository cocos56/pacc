import os
from shutil import rmtree
from ..nox import getOnlineDevices, NoxADB, NoxUIAutomator


class NoxProj:

    def __init__(self, noxWorkPath=r'D:\Program Files\Nox\bin'):
        self.noxWorkPath = noxWorkPath
        os.chdir(self.noxWorkPath)

    def cleanUIAFiles(self):
        rmtree('%s/CurrentUIHierarchy' % self.noxWorkPath)

    @classmethod
    def getStatus(cls):
        for i in getOnlineDevices():
            adbIns = NoxADB(i)
            uiaIns = NoxUIAutomator(i)
            adbIns.getCurrentFocus()
            uiaIns.getScreen()
            uiaIns.getCurrentUIHierarchy()
