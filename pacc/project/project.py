from datetime import datetime
from random import randint
from time import time
from ..config import Config
from ..adb import ADB, UIAutomator
from ..multi import threadLock
from ..tools import sleep


class ResourceID:
    clearAnimView = 'com.android.systemui:id/clearAnimView'  # 内存清理图标
    clearAnimView2 = 'com.miui.home:id/clearAnimView'  # 内存清理图标


class Activity:
    Launcher = 'com.miui.home/com.miui.home.launcher.Launcher'
    RecentsActivity = 'com.android.systemui/com.android.systemui.recents.RecentsActivity'


class Project:
    instances = []
    startTime = datetime.now()

    def __init__(self, deviceSN, add=True):
        self.adbIns = ADB(deviceSN)
        self.uIAIns = UIAutomator(deviceSN)
        self.lastReopenHour = -1
        self.restTime = 0
        self.lastTime = time()
        if add:
            threadLock.acquire()
            self.instances.append(self)
            threadLock.release()

    def __del__(self):
        threadLock.acquire()
        if self in self.instances:
            self.instances.remove(self)
        threadLock.release()

    def randomSwipe(self, xA, xB, xC, xD, yA, yB, yC, yD, initRestTime=False):
        if initRestTime and self.restTime > 0:
            self.restTime = 0
        elif self.restTime > 0:
            return
        self.adbIns.swipe(randint(xA, xB), randint(yA, yB), randint(xC, xD), randint(yC, yD))
        self.restTime += randint(3, 15)

    def reopenAppPerHour(self, execute=True):
        if self.lastReopenHour == datetime.now().hour:
            return False
        self.lastReopenHour = datetime.now().hour
        if execute:
            self.reopenApp()
        return True

    def tapFreeButton(self):
        if 'MI 4' in self.adbIns.device.Model:
            self.uIAIns.click(ResourceID.clearAnimView)
        elif 'MI 5' in self.adbIns.device.Model:
            self.uIAIns.click(ResourceID.clearAnimView)
        elif 'MI 6' in self.adbIns.device.Model:
            self.uIAIns.click(ResourceID.clearAnimView)
        elif 'Redmi K20' in self.adbIns.device.Model:
            self.uIAIns.click(ResourceID.clearAnimView2)

    def reopenApp(self):
        self.freeMemory()
        if not Config.debug and 'MI 4' in self.adbIns.device.Model:
            self.adbIns.pressPowerKey()
            sleep(60)
        self.adbIns.pressHomeKey()
        self.openApp()

    def openApp(self, activity):
        self.adbIns.pressHomeKey()
        self.adbIns.start(activity)

    def freeMemory(self):
        self.adbIns.pressHomeKey()
        self.adbIns.pressHomeKey()
        self.adbIns.pressMenuKey()
        try:
            self.tapFreeButton()
        except FileNotFoundError as e:
            print(e)
            self.freeMemory()
        currentFocus = self.adbIns.getCurrentFocus()
        if Activity.RecentsActivity in currentFocus:
            self.adbIns.pressHomeKey()
            currentFocus = self.adbIns.getCurrentFocus()
        if Activity.Launcher not in currentFocus:
            self.adbIns.reboot()
            self.freeMemory()
