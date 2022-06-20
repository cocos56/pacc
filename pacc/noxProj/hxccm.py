"""
含羞草传媒模块
"""
# pylint: disable=R0801
from datetime import datetime
from xml.parsers.expat import ExpatError

from .noxProj import NoxProj
from ..multi.thread import runThreadsWithArgsList
from ..nox import getOnlineDevices, NoxADB, NoxConsole, NoxUIAutomator
from ..tools import sleep

ROOT = 'com.o77d33143cca.xbf0768683dz/com.aF1HrwA52uEd.ovSxbQjBF7Av.'


# pylint: disable=R0903
class Activity:
    """安卓的活动名"""
    MainActivity = ROOT + 'MainActivity'  # 程序入口（广告页）
    Launcher = 'com.android.launcher3/com.android.launcher3.launcher3.Launcher'


class HXCCM(NoxProj):
    """含羞草传媒模块"""
    def __init__(self, start_index=0, i_code='F3GWZN', nox_work_path=r'D:\Program Files\Nox\bin',
                 nox_step=3):
        self.start_index = start_index
        self.i_code = i_code
        super().__init__(nox_work_path)
        self.nox_step = nox_step
        self.nox_num = NoxConsole.getNumber()
        self.last_online_devices = []

    def do_work_when_input_i_code(self, adb_ins, uia_ins):
        """进入输入邀请码界面输入邀请码并提交

        :param adb_ins: 安卓调试桥类的实例
        :param uia_ins: UI自动化测试类的实例
        """
        uia_ins.click(contentDesc='输入邀请码')
        uia_ins.click(text='请输入邀请码')
        adb_ins.inputText(self.i_code)
        uia_ins.click(contentDesc='提交')

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
        self.do_work_when_input_i_code(adbIns, uiaIns)

    def doWork(self, deviceIP):
        try:
            self.doAllWork(deviceIP)
        except FileNotFoundError as e:
            print(e)

    def runApp(self):
        NoxConsole(self.start_index).runApp('com.o77d33143cca.xbf0768683dz')

    def launchAllByStep(self):
        print(datetime.now())
        NoxConsole.quit_all()
        for i in range(self.nox_step):
            self.start_index += 1
            self.runApp()
        sleep(45)
        onlineDevices = getOnlineDevices()
        errCnt = 0
        while True:
            sleep(5, False, False)
            for i in onlineDevices:
                if i in self.last_online_devices:
                    continue
            if len(onlineDevices) == self.nox_step:
                break
            if errCnt >= 9:
                break
            errCnt += 1
            onlineDevices = getOnlineDevices()
        self.last_online_devices = onlineDevices
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
                    self.do_work_when_input_i_code(adbIns, uiaIns)
                    continue
                elif uiaIns.getDict(contentDesc='输入邀请码'):
                    self.do_work_when_input_i_code(adbIns, uiaIns)
                    continue
                elif uiaIns.getDict(text='请输入12位激活码'):
                    adbIns.pressBackKey()
                    uiaIns.click(contentDesc='账号设置')
                    self.do_work_when_input_i_code(adbIns, uiaIns)
                    continue
                elif uiaIns.click(contentDesc='账号设置'):
                    self.do_work_when_input_i_code(adbIns, uiaIns)
                    continue
                elif uiaIns.getDict(contentDesc='——·含羞草公告·——'):
                    uiaIns.click(contentDesc='确定')
                    uiaIns.tap((484, 925))  # 点击【我的】
                    adbIns.pressBackKey()  # 从【保存凭据】返回
                    uiaIns.click(contentDesc='账号设置')
                    self.do_work_when_input_i_code(adbIns, uiaIns)
                    continue
                elif Activity.Launcher in adbIns.getCurrentFocus():
                    adbIns.start(Activity.MainActivity)
                    self.doAllWork(i)
                    continue
            except (ExpatError, FileNotFoundError) as e:
                print(e)

    def mainLoop(self):
        while True:
            if self.start_index >= self.nox_num:
                break
            self.launchAllByStep()
