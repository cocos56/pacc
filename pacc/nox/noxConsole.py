import os
from ..tools import sleep


class NoxConsole:

    @classmethod
    def quitAll(cls):
        cmd = 'NoxConsole.exe quitall'
        os.system(cmd)
        print(cmd)
        sleep(13)

    def __init__(self, noxIndex):
        self.noxIndex = noxIndex

    def quit(self):
        cmd = 'NoxConsole.exe quit -index:%d' % self.noxIndex
        print(cmd)
        os.popen(cmd)
        sleep(3, False, False)

    def runApp(self, packagename):
        cmd = 'NoxConsole.exe runapp -index:%d -packagename:%s' % (self.noxIndex, packagename)
        print(cmd)
        os.popen(cmd)
        sleep(3, False, False)
