"""自动远程控制手机APP中央控制系统工程模块"""
from datetime import datetime, timedelta
from random import randint

from ..adb import ADB, UIAutomator
from ..base import sleep


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
    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备编号
        """
        self.serial_num = serial_num
        self.adb_ins = ADB(serial_num)
        self.uia_ins = UIAutomator(serial_num)
        self.last_reopen_datetime = datetime.now() - timedelta(minutes=30)

    def random_swipe(self, x_range, y_list):
        """随机滑动一段长度

        :param x_range : x_min（A、C点的X轴坐标）与x_max（B、D点的X轴坐标）
        :param y_list: [A点的Y轴坐标，B点的Y轴坐标，C点的Y轴坐标，D点的Y轴坐标]
        """
        x_min, x_max = x_range
        a_y, b_y, c_y, d_y = y_list
        self.adb_ins.swipe(randint(x_min, x_max), randint(a_y, b_y), randint(x_min, x_max),
                           randint(c_y, d_y))

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
        print('重新打开APP')
        self.free_memory()
        if 'MI 4' in self.adb_ins.device.model:
            sleep(60)
        self.adb_ins.press_home_key()
        self.open_app()

    def open_app(self):
        """打开APP，该方法父类中未实现，需要在子类中实现"""
        print('打开APP，该方法父类中未实现，需要在子类中实现')

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
