from datetime import datetime
from xml.parsers.expat import ExpatError
from ..multi.thread import runThreadsWithArgsList
from ..nox import getOnlineDevices, NoxADB, NoxConsole, NoxUIAutomator
from ..tools import sleep
from .noxProj import NoxProj

root = 'com.o77d33143cca.xbf0768683dz/com.aF1HrwA52uEd.ovSxbQjBF7Av.'


class Activity:
    MainActivity = root + 'MainActivity'  # 程序入口（广告页）
    Launcher = 'com.android.launcher3/com.android.launcher3.launcher3.Launcher'


class HXCCM(NoxProj):
    def __init__(self, startIndex=0, iCode='F3GWZN', noxWorkPath=r'D:\Program Files\Nox\bin', noxStep=3):
        self.startIndex = startIndex
        self.iCode = iCode
        super(HXCCM, self).__init__(noxWorkPath)
        self.noxStep = noxStep
        self.noxNum = NoxConsole.getNumber()
        self.lastOnlineDevices = []

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
        errCnt = 0
        uiaIns.click(text='关闭应用')
        while not uiaIns.click(contentDesc='跳过', offset_y=20, interval=3):
            uiaIns.click(contentDesc='重新检测')
            if uiaIns.click(contentDesc='确定'):
                isConfirmed = True
                break
            if uiaIns.click(contentDesc='我的'):
                hasMy = True
                break
            if errCnt >= 9:
                break
            sleep(5, False, False)
            errCnt += 1
        errCnt = 0
        while not uiaIns.click(contentDesc='确定'):
            if isConfirmed:
                break
            elif hasMy:
                break
            elif uiaIns.click(contentDesc='我的'):
                break
            if errCnt >= 5:
                break
            sleep(5, False, False)
            errCnt += 1
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
        NoxConsole(self.startIndex).runApp('com.o77d33143cca.xbf0768683dz')

    def launchAllByStep(self):
        print(datetime.now())
        NoxConsole.quit_all()
        for i in range(self.noxStep):
            self.startIndex += 1
            self.runApp()
        sleep(45)
        onlineDevices = getOnlineDevices()
        errCnt = 0
        while True:
            sleep(5, False, False)
            for i in onlineDevices:
                if i in self.lastOnlineDevices:
                    continue
            if len(onlineDevices) == self.noxStep:
                break
            if errCnt >= 9:
                break
            errCnt += 1
            onlineDevices = getOnlineDevices()
        self.lastOnlineDevices = onlineDevices
        print(onlineDevices)
        runThreadsWithArgsList(self.doWork, onlineDevices)
        for i in onlineDevices:
            uiaIns = NoxUIAutomator(i)
            try:
                if uiaIns.getDict(contentDesc='您绑定的邀请码为：'):
                    continue
                self.clean_uia_files()
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
                elif Activity.Launcher in adbIns.getCurrentFocus():
                    adbIns.start(Activity.MainActivity)
                    self.doAllWork(i)
                    continue
            except (ExpatError, FileNotFoundError) as e:
                print(e)

    def mainLoop(self):
        while True:
            if self.startIndex >= self.noxNum:
                break
            self.launchAllByStep()
