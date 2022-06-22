from .project import Project
from ..tools import sleep, showDatetime
from xml.parsers.expat import ExpatError


class ResourceID:
    button2 = 'android:id/button2'  # 确定（联机业务异常，请重新联机）、立即连接（连接异常,正在重新连接......）
    button1 = 'android:id/button1'  # 取消
    auto_wait_btn = 'com.dd.rclient:id/auto_wait_btn'
    mec_connect_state = 'com.dd.rclient:id/mec_connect_state'  # 正在连接服务器...
    btn_exit_app = 'com.dd.rclient:id/btn_exit_app'  # 退出程序
    icon_title = 'com.miui.home:id/icon_title'  # 桌面图标


class Activity:
    MainActivity = 'com.dd.rclient/com.dd.rclient.ui.activity.MainActivity'
    LoginActivity = 'com.dd.rclient/com.dd.rclient.ui.activity.LoginActivity'  # 登录


class SD(Project):
    instances = []

    def __init__(self, SN):
        super(SD, self).__init__(SN)

    def check(self):
        self.adbIns.keepOnline()
        try:
            self.uIAIns.click(ResourceID.button2)
            dic = self.uIAIns.getDict(ResourceID.mec_connect_state, xml=self.uIAIns.xml)
            currentFocus = self.adbIns.get_current_focus()
            if dic and dic['@text'] == '正在连接服务器...':
                self.reopenApp()
            elif not dic and Activity.MainActivity in currentFocus:
                self.reopenApp()
            elif Activity.LoginActivity in currentFocus:
                self.adbIns.reboot()
                self.openApp()
        except (FileNotFoundError, ExpatError) as e:
            print(e)
            sleep(60)
            self.check()

    def reopenApp(self):
        self.exitApp()
        self.openApp()

    def openApp(self):
        self.freeMemory()
        self.uIAIns.click(ResourceID.icon_title, '滴滴助手')
        sleep(12)
        self.uIAIns.click(ResourceID.auto_wait_btn)
        self.uIAIns.click(ResourceID.button1)

    def exitApp(self):
        self.uIAIns.click(ResourceID.btn_exit_app, xml=self.uIAIns.xml)
        self.uIAIns.click(ResourceID.button2)

    @classmethod
    def mainloop(cls, devicesSN):
        for deviceSN in devicesSN:
            cls.instances.append(cls(deviceSN))
        while True:
            for i in cls.instances:
                i.check()
            sleep(600)
            showDatetime('mainloop')
