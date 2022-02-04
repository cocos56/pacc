from .noxProj import NoxProj
from ..adb.noxADB import NoxADB
from datetime import datetime


class HXCCM(NoxProj):
    def __init__(self, startIndex, noxWorkPath=r'D:\Program Files\Nox\bin', noxStep=3):
        super(NoxProj, self).__init__(noxWorkPath)
        self.noxStep = noxStep
        self.startIndex = startIndex

    def runApp(self):
        NoxADB(self.startIndex).runApp('com.vbzWSioa.vmNksMrCYo')

    def quitAll(self):
        for i in range(self.noxStep):
            NoxADB(self.startIndex - 5 + i).quit()

    def mainLoop(self):
        print('初始化中，请耐心等待')
        NoxADB.quitAll()
        print('初始化完毕\n')
        while True:
            print(datetime.now())
            for i in range(self.noxStep):
                self.startIndex += 1
                self.runApp()
            self.quitAll()
            input('按Enter键以继续\n')
