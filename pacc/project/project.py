from datetime import datetime
from random import randint
from time import time

from ..adb import ADB, UIAutomator
from ..config import Config
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

    def __init__(self, device_sn, add_flag=True):
        """构造函数

        :param device_sn: 设备编号
        :param add_flag: 是否将此对象追加到实例列表中，默认会自动追加
        """
        self.adbIns = ADB(device_sn)
        self.uIAIns = UIAutomator(device_sn)
        self.lastReopenHour = -1
        self.restTime = 0
        self.lastTime = time()
        if add_flag:
            threadLock.acquire()
            self.instances.append(self)
            threadLock.release()

    def __del__(self):
        """析构函数"""
        threadLock.acquire()
        if self in self.instances:
            self.instances.remove(self)
        threadLock.release()

    def random_swipe(self, xA, xB, xC, xD, yA, yB, yC, yD, initRestTime=False):
        if initRestTime and self.restTime > 0:
            self.restTime = 0
        elif self.restTime > 0:
            return
        self.adbIns.swipe(randint(xA, xB), randint(yA, yB), randint(xC, xD), randint(yC, yD))
        self.restTime += randint(3, 15)

    def reopen_app_per_hour(self, execute=True):
        if self.lastReopenHour == datetime.now().hour:
            return False
        self.lastReopenHour = datetime.now().hour
        if execute:
            self.reopen_app()
        return True

    def tap_free_button(self):
        """点击清理按钮"""
        if 'MI 4' in self.adbIns.device.Model:
            self.uIAIns.click(ResourceID.clearAnimView)
        elif 'MI 5' in self.adbIns.device.Model:
            self.uIAIns.click(ResourceID.clearAnimView)
        elif 'MI 6' in self.adbIns.device.Model:
            self.uIAIns.click(ResourceID.clearAnimView)
        elif 'Redmi K20' in self.adbIns.device.Model:
            self.uIAIns.click(ResourceID.clearAnimView2)

    def reopen_app(self):
        """重新打开APP"""
        self.free_memory()
        if not Config.debug and 'MI 4' in self.adbIns.device.Model:
            self.adbIns.press_power_key()
            sleep(60)
        self.adbIns.press_home_key()
        self.open_app()

    def open_app(self, activity):
        """打开APP"""
        self.adbIns.press_home_key()
        self.adbIns.start(activity)

    def free_memory(self):
        """清理内存"""
        self.adbIns.press_home_key()
        self.adbIns.press_home_key()
        self.adbIns.press_menu_key()
        try:
            self.tap_free_button()
        except FileNotFoundError as e:
            print(e)
            self.free_memory()
        current_focus = self.adbIns.get_current_focus()
        if Activity.RecentsActivity in current_focus:
            self.adbIns.press_home_key()
            current_focus = self.adbIns.get_current_focus()
        if Activity.Launcher not in current_focus:
            self.adbIns.reboot()
            self.free_memory()
