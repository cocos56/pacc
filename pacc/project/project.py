"""自动远程控制手机APP中央控制系统工程模块"""
from datetime import datetime
from random import randint
from time import time

from ..adb import ADB, UIAutomator
from ..base import sleep
from ..config import Config
from ..multi import threadLock


# pylint: disable=too-few-public-methods
class Activity:
    """活动名类"""
    Launcher = 'com.miui.home/com.miui.home.launcher.Launcher'
    RecentsActivity = 'com.android.systemui/com.android.systemui.recents.RecentsActivity'


# pylint: disable=too-few-public-methods
class ResourceID:
    """资源的ID类"""
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
        self.adb_ins = ADB(serial_num)
        self.uia_ins = UIAutomator(serial_num)
        self.last_reopen_hour = -1
        self.rest_time = 0
        self.last_time = time()
        if add_flag:
            with threadLock:
                self.instances.append(self)

    def __del__(self):
        """析构函数"""
        with threadLock:
            if self in self.instances:
                self.instances.remove(self)

    # pylint: disable=too-many-arguments
    def random_swipe(self, a_x, b_x, c_x, d_x, a_y, b_y, c_y, d_y, init_rest_time=False):
        """随机滑动一段长度

        :param a_x: A点的X轴坐标
        :param b_x: B点的X轴坐标
        :param c_x: C点的X轴坐标
        :param d_x: D点的X轴坐标
        :param a_y: A点的Y轴坐标
        :param b_y: B点的Y轴坐标
        :param c_y: C点的Y轴坐标
        :param d_y: D点的Y轴坐标
        :param init_rest_time: 是否初始化剩余时间
        """
        if init_rest_time and self.rest_time > 0:
            self.rest_time = 0
        elif self.rest_time > 0:
            return
        self.adb_ins.swipe(randint(a_x, b_x), randint(a_y, b_y), randint(c_x, d_x),
                           randint(c_y, d_y))
        self.rest_time += randint(3, 15)

    def reopen_app_per_hour(self, execute=True):
        """每小时重启一下APP

        :param execute: 是否执行重启APP
        """
        if self.last_reopen_hour == datetime.now().hour:
            return False
        self.last_reopen_hour = datetime.now().hour
        if execute:
            self.reopen_app()
        return True

    def tap_free_button(self):
        """点击清理按钮"""
        if 'MI 4' in self.adb_ins.device.model:
            self.uia_ins.click(ResourceID.clearAnimView)
        elif 'MI 5' in self.adb_ins.device.model:
            self.uia_ins.click(ResourceID.clearAnimView)
        elif 'MI 6' in self.adb_ins.device.model:
            self.uia_ins.click(ResourceID.clearAnimView)
        elif 'Redmi K20' in self.adb_ins.device.model:
            self.uia_ins.click(ResourceID.clearAnimView2)

    def reopen_app(self):
        """重新打开APP"""
        self.free_memory()
        if not Config.debug and 'MI 4' in self.adb_ins.device.model:
            self.adb_ins.press_power_key()
            sleep(60)
        self.adb_ins.press_home_key()
        # pylint: disable=no-value-for-parameter
        self.open_app()

    def open_app(self, activity):
        """打开APP

        param activity: 活动名
        """
        self.adb_ins.press_home_key()
        self.adb_ins.start(activity)

    def free_memory(self):
        """清理内存"""
        self.adb_ins.press_home_key()
        self.adb_ins.press_home_key()
        self.adb_ins.press_menu_key()
        try:
            self.tap_free_button()
        except FileNotFoundError as error:
            print(error)
            self.free_memory()
        current_focus = self.adb_ins.get_current_focus()
        if Activity.RecentsActivity in current_focus:
            self.adb_ins.press_home_key()
            current_focus = self.adb_ins.get_current_focus()
        if Activity.Launcher not in current_focus:
            self.adb_ins.reboot()
            self.free_memory()
