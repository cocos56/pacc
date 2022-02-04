from ...tools import sleep, getURLsFromString
from ..project import Project


class Activity:
    LauncherUI = 'com.tencent.mm/com.tencent.mm.ui.LauncherUI'  # 微信程序
    Launcher = 'com.miui.home/com.miui.home.launcher.Launcher'  # 桌面


class ResourceID:
    nk = 'com.tencent.mm:id/nk'  # 主界面未读总消息数【微信(9)】
    iot = 'com.tencent.mm:id/iot'  # 主界面未读项（0-n个对话）
    fzg = 'com.tencent.mm:id/fzg'  # 主界面的消息项（所有对话）
    auk = 'com.tencent.mm:id/auk'  # 聊天界面消息项（多条消息）
    auj = 'com.tencent.mm:id/auj'  # 聊天界面的输入框
    ay5 = 'com.tencent.mm:id/ay5'  # 聊天界面的发送按钮


class MM(Project):
    def __init__(self, deviceSN):
        super(MM, self).__init__(deviceSN, False)

    def enterLatestMsgInterface(self):
        self.reopenApp()
        if self.uIAIns.click(ResourceID.iot):
            return True

    def getLatestMsg(self):
        if not self.enterLatestMsgInterface():
            return
        res = self.uIAIns.getDicts(ResourceID.auk)
        if res:
            return res[-1]['@text']

    def getLatestURL(self):
        res = self.getLatestMsg()
        if res:
            urls = getURLsFromString(res)
        url = urls[0] if len(urls) == 1 else None
        self.exitApp()
        print(urls)
        print(url)
        return url

    def sendURL(self):
        url = self.getLatestURL()
        self.reopenApp()
        self.uIAIns.click(ResourceID.fzg)
        self.uIAIns.click(ResourceID.auj)
        self.adbIns.inputText(url)
        self.uIAIns.click(ResourceID.ay5)

    def exitApp(self):
        self.openApp(1)
        while Activity.Launcher not in self.adbIns.getCurrentFocus():
            self.adbIns.pressBackKey()

    def reopenApp(self):
        self.exitApp()
        super(MM, self).reopenApp()

    def openApp(self, interval=6):
        super(MM, self).openApp(Activity.LauncherUI)
        sleep(interval)
