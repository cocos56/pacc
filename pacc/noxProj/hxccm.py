from .noxProj import NoxProj
from pacc.nox.noxConsole import NoxConsole
from pacc.nox.noxADB import getOnlineDevices, NoxADB
from pacc.nox.noxUIA import NoxUIAutomator
from datetime import datetime
from pacc.tools import sleep
from pacc.multi.thread import runThreadsWithArgsList

root = 'com.vbzWSioa.vmNksMrCYo/com.a4XytlcZMv.oYB40hzBgv.'


class Activity:
    MainActivity = root + 'MainActivity'  # 程序入口（广告页）


class HXCCM(NoxProj):
    def __init__(self, startIndex, iCode='F3GWZN', noxWorkPath=r'D:\Program Files\Nox\bin', noxStep=3):
        self.startIndex = startIndex
        self.iCode = iCode
        super(HXCCM, self).__init__(noxWorkPath)
        self.noxStep = noxStep
        self.lastOnlineDevices = []

    @classmethod
    def getStatus(cls):
        for i in getOnlineDevices():
            adbIns = NoxADB(i)
            uiaIns = NoxUIAutomator(i)
            adbIns.getCurrentFocus()
            uiaIns.getScreen()
            uiaIns.getCurrentUIHierarchy()

    def doWorkWhenInputICode(self, adbIns, uiaIns):
        uiaIns.click(contentDesc='输入邀请码')
        uiaIns.click(text='请输入邀请码')
        adbIns.inputText(self.iCode)
        uiaIns.click(contentDesc='提交')
        pass

    def doAllWork(self, deviceIP):
        adbIns = NoxADB(deviceIP)
        while Activity.MainActivity not in adbIns.getCurrentFocus():
            sleep(5, False, False)
        uiaIns = NoxUIAutomator(deviceIP)
        uiaIns.getCurrentUIHierarchy()
        isConfirmed = False
        hasMy = False
        while not uiaIns.click(contentDesc='跳过', offset_y=20):
            uiaIns.click(contentDesc='重新检测')
            if uiaIns.click(contentDesc='确定'):
                isConfirmed = True
                break
            if uiaIns.click(contentDesc='我的'):
                hasMy = True
                break
            sleep(5, False, False)
        while not uiaIns.click(contentDesc='确定'):
            if isConfirmed:
                break
            elif hasMy:
                break
            elif uiaIns.click(contentDesc='我的'):
                break
            sleep(5, False, False)
        uiaIns.tap((484, 925))  # 点击【我的】
        adbIns.pressBackKey()  # 从【保存凭据】返回
        uiaIns.click(contentDesc='账号设置')
        self.doWorkWhenInputICode(adbIns, uiaIns)

    def doWork(self, deviceIP):
        try:
            self.doAllWork(deviceIP)
        except FileNotFoundError as e:
            print(e)

    def runApp(self):
        NoxConsole(self.startIndex).runApp('com.vbzWSioa.vmNksMrCYo')

    def mainLoop(self):
        while True:
            print(datetime.now())
            NoxConsole.quitAll()
            for i in range(self.noxStep):
                self.startIndex += 1
                self.runApp()
            sleep(20)
            onlineDevices = getOnlineDevices()
            while True:
                # print(onlineDevices)
                sleep(5, False, False)
                for i in onlineDevices:
                    if i in self.lastOnlineDevices:
                        continue
                if len(onlineDevices) == self.noxStep:
                    break
                onlineDevices = getOnlineDevices()
            self.lastOnlineDevices = onlineDevices
            print(onlineDevices)
            runThreadsWithArgsList(self.doWork, onlineDevices)
            for i in onlineDevices:
                uiaIns = NoxUIAutomator(i)
                if not uiaIns.getDict(contentDesc='您绑定的邀请码为：'):
                    self.cleanUIAFiles()
                    adbIns = NoxADB(i)
                    if uiaIns.getDict(contentDesc='您绑定的邀请码为：'):
                        continue
                    elif uiaIns.getDict(text='请输入邀请码'):
                        adbIns.pressBackKey()
                        self.doWorkWhenInputICode(adbIns, uiaIns)
                        continue
                    elif uiaIns.getDict(contentDesc='输入邀请码'):
                        self.doWorkWhenInputICode(adbIns, uiaIns)
                        continue
                    elif uiaIns.getDict(text='请输入12位激活码'):
                        adbIns.pressBackKey()
                        uiaIns.click(contentDesc='账号设置')
                        self.doWorkWhenInputICode(adbIns, uiaIns)
                        continue
                    elif uiaIns.click(contentDesc='账号设置'):
                        self.doWorkWhenInputICode(adbIns, uiaIns)
                        continue
                    elif uiaIns.getDict(contentDesc='——·含羞草公告·——'):
                        uiaIns.click(contentDesc='确定')
                        uiaIns.tap((484, 925))  # 点击【我的】
                        adbIns.pressBackKey()  # 从【保存凭据】返回
                        uiaIns.click(contentDesc='账号设置')
                        self.doWorkWhenInputICode(adbIns, uiaIns)
                        continue
                    adbIns.getCurrentFocus()
                    uiaIns.getScreen()
                    uiaIns.getCurrentUIHierarchy()
                    input('结束页错误，请按Enter键以继续\n')
