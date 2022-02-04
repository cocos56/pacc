from .noxProj import NoxProj
from pacc.nox.noxConsole import NoxConsole
from pacc.nox.noxADB import getOnlineDevices, NoxADB
from pacc.nox.noxUIA import NoxUIAutomator
from datetime import datetime
from pacc.tools import sleep

root = 'com.vbzWSioa.vmNksMrCYo/com.a4XytlcZMv.oYB40hzBgv.'


class Activity:
    MainActivity = root + 'MainActivity'  # 程序入口（广告页）


class HXCCM(NoxProj):
    def __init__(self, startIndex, noxWorkPath=r'D:\Program Files\Nox\bin', noxStep=3):
        super(HXCCM, self).__init__(noxWorkPath)
        self.noxStep = noxStep
        self.startIndex = startIndex

    def runApp(self):
        NoxConsole(self.startIndex).runApp('com.vbzWSioa.vmNksMrCYo')

    def quitAll(self):
        for i in range(self.noxStep):
            NoxConsole(self.startIndex - 5 + i).quit()

    def mainLoop(self):
        print('初始化中，请耐心等待')
        NoxConsole.quitAll()
        print('初始化完毕\n')
        while True:
            print(datetime.now())
            for i in range(self.noxStep):
                self.startIndex += 1
                self.runApp()
            self.quitAll()
            sleep(15)
            onlineDevices = getOnlineDevices()
            while not len(onlineDevices) == self.noxStep:
                # print(onlineDevices)
                sleep(5, False, False)
                onlineDevices = getOnlineDevices()
            print(onlineDevices)
            for i in onlineDevices:
                adbIns = NoxADB(i)
                while Activity.MainActivity not in adbIns.getCurrentFocus():
                    sleep(5, False, False)
                uiaIns = NoxUIAutomator(i)
                uiaIns.getCurrentUIHierarchy()
                while not uiaIns.click(contentDesc='跳过', offset_y=20):
                    uiaIns.click(contentDesc='重新检测')
                    sleep(5, False, False)
                while not uiaIns.click(contentDesc='确定'):
                    sleep(5, False, False)
                uiaIns.tap((484, 925))  # 点击【我的】
                adbIns.pressBackKey()  # 从【保存凭据】返回
                uiaIns.click(contentDesc='账号设置')
                uiaIns.click(contentDesc='输入邀请码')
                uiaIns.click(text='请输入邀请码')
                adbIns.inputText('19JLGP')
                uiaIns.click(contentDesc='提交')
            input('按Enter键以继续\n')
