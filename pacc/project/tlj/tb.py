from ...tools import sleep
from ..project import Project


class Activity:
    TBMainActivity = 'com.taobao.taobao/com.taobao.tao.TBMainActivity'  # 淘宝程序


class TB(Project):
    def __init__(self, deviceSN):
        super(TB, self).__init__(deviceSN, False)

    def openApp(self):
        super(TB, self).openApp(Activity.TBMainActivity)
        sleep(6)
