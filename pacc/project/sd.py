"""淘宝/拼多多全自动远程刷单APP中央控制系统模块"""
from xml.parsers.expat import ExpatError

from .project import Project
from ..base import show_datetime, sleep, print_err
from ..tools import EMail

ROOT = 'com.dd.rclient/com.dd.rclient.ui.activity.'


# pylint: disable=too-few-public-methods
class Activity:
    """淘宝/拼多多全自动远程刷单APP中央控制系统模块的安卓的活动名类"""
    MainActivity = f'{ROOT}MainActivity'
    LoginActivity = f'{ROOT}LoginActivity'  # 登录


# pylint: disable=too-few-public-methods
class ResourceID:
    """淘宝/拼多多全自动远程刷单APP中央控制系统模块的安卓的资源ID类"""
    # 确定（联机业务异常，请重新联机）、立即连接（连接异常,正在重新连接......）、
    # （切换账号将会结束您当前的挂机,是否继续?）
    button2 = 'android:id/button2'
    button1 = 'android:id/button1'  # 取消
    auto_wait_btn = 'com.dd.rclient:id/auto_wait_btn'
    # 连接状态信息：【正在连接服务器...】、【已连接到服务器,等待控制端连接】
    mec_connect_state = 'com.dd.rclient:id/mec_connect_state'
    btn_exit_app = 'com.dd.rclient:id/btn_exit_app'  # 退出程序
    icon_title = 'com.miui.home:id/icon_title'  # 桌面图标
    message = 'android:id/message'  # 切换账号将会结束您当前的挂机,是否继续?


class SD(Project):
    """刷单类"""

    instances = []

    def check(self):
        """检查"""
        self.adb_ins.keep_online()
        current_focus = self.adb_ins.get_current_focus()
        dic = self.uia_ins.get_dict(ResourceID.message)
        if dic and dic['@text'] == '切换账号将会结束您当前的挂机,是否继续?':
            self.uia_ins.click(ResourceID.button1, xml=self.uia_ins.xml)
            self.uia_ins.xml = ''
        self.uia_ins.click(ResourceID.button2, xml=self.uia_ins.xml)
        dic = self.uia_ins.get_dict(ResourceID.mec_connect_state, xml=self.uia_ins.xml)
        if dic and dic['@text'] == '正在连接服务器...':
            self.reopen_app()
        elif not dic and Activity.MainActivity in current_focus:
            self.reopen_app()
        elif Activity.LoginActivity in current_focus:
            self.adb_ins.reboot()
            self.open_app()
            if Activity.LoginActivity in self.adb_ins.get_current_focus():
                EMail(self.serial_num).send_offline_error()
                sleep(600)

    def reopen_app(self):
        """重新打开APP"""
        self.exit_app()
        self.open_app()

    def open_app(self):
        """打开淘宝/拼多多全自动远程刷单APP"""
        self.free_memory()
        self.uia_ins.click(ResourceID.icon_title, '滴滴助手')
        sleep(12)
        self.uia_ins.click(ResourceID.auto_wait_btn)
        self.uia_ins.click(ResourceID.button1)

    def exit_app(self):
        """退出APP"""
        self.uia_ins.click(ResourceID.btn_exit_app, xml=self.uia_ins.xml)
        self.uia_ins.click(ResourceID.button2)

    @classmethod
    def mainloop(cls, devices_sn):
        """主循环函数

        :param devices_sn: 多个设备的编号
        """
        for device_sn in devices_sn:
            cls.instances.append(cls(device_sn))
        while True:
            for i in cls.instances:
                i.check()
            sleep(600)
            show_datetime('mainloop')
