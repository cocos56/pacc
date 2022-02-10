from os import popen
from datetime import datetime
from ..tools import sleep, system


class NoxConsole:

    @classmethod
    def getNumber(cls): return popen('NoxConsole.exe list"').read().count('\n') - 1

    @classmethod
    def removeAll(cls): cls.remove(cls.getNumber())

    @classmethod
    def remove(cls, stopIndex):
        if stopIndex < 1:
            return
        for i in range(1, stopIndex+1):
            system('NoxConsole.exe remove -index:%d' % i)

    @classmethod
    def copy(cls, num):
        noxNum = cls.getNumber()
        num = num - num % 3
        if num <= noxNum:
            return
        startTime = datetime.now()
        for i in range(noxNum + 1, num+1):
            iTime = datetime.now()
            print('正在复制第%04d个' % i)
            system('NoxConsole.exe copy -name:HXC%04d -from:HXC' % i, False)
            print('复制已完成，本次用时%s，总用时%s\n' % ((datetime.now()-iTime), (datetime.now()-startTime)))

    @classmethod
    def quitAll(cls):
        system('NoxConsole.exe quitall')
        sleep(13)
        if popen('tasklist | findstr "Nox.exe"').read():
            system('taskkill /IM Nox.exe')
            sleep(15)

    def __init__(self, noxIndex):
        self.noxIndex = noxIndex

    def runApp(self, packagename):
        cmd = 'NoxConsole.exe runapp -index:%d -packagename:%s' % (self.noxIndex, packagename)
        print(cmd)
        popen(cmd)
        sleep(5, False, False)
