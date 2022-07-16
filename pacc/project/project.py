"""自动远程控制手机APP中央控制系统工程模块"""
from datetime import datetime
from random import randint
from time import time

from ..adb import ADB, UIAutomator
from ..config import Config
from ..multi import threadLock
from ..tools import sleep


# pylint: disable=too-few-public-methods
class Activity:
    """活动名类"""
    Launcher = 'com.miui.home/com.miui.home.launcher.Launcher'
    RecentsActivity = 'com.android.systemui/com.android.systemui.recents.RecentsActivity'


# pylint: disable=too-few-public-methods
class ResourceID:
    """资源的鉴别码类"""
    clearAnimView = 'com.android.systemui:id/clearAnimView'  # 内存清理图标
    clearAnimView2 = 'com.miui.home:id/clearAnimView'  # 内存清理图标


class Project:
    """工程类"""
    instances = []
    startTime = datetime.now()

    def __init__(self, serial_num, add_flag=True):
        """构造函数

        :param serial_num: 设备编号
        :param add_flag: 是否将此对象追加到实例列表中，默认会自动追加
        """
        self.adbIns = ADB(serial_num)
        self.uIAIns = UIAutomator(serial_num)
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
        """每小时重启一下APP

        :param execute: 是否执行重启APP
        """
        if self.lastReopenHour == datetime.now().hour:
            return False
        self.lastReopenHour = datetime.now().hour
        if execute:
            self.reopen_app()
        return True

    def tap_free_button(self):
        """点击清理按钮"""
        if 'MI 4' in self.adbIns.device.model:
            self.uIAIns.click(ResourceID.clearAnimView)
        elif 'MI 5' in self.adbIns.device.model:
            self.uIAIns.click(ResourceID.clearAnimView)
        elif 'MI 6' in self.adbIns.device.model:
            self.uIAIns.click(ResourceID.clearAnimView)
        elif 'Redmi K20' in self.adbIns.device.model:
            self.uIAIns.click(ResourceID.clearAnimView2)

    def reopen_app(self):
        """重新打开APP"""
        self.free_memory()
        if not Config.debug and 'MI 4' in self.adbIns.device.model:
            self.adbIns.press_power_key()
            sleep(60)
        self.adbIns.press_home_key()
        self.open_app()

    def open_app(self, activity):
        """打开APP

        param activity: 活动
        """
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
