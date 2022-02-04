from ..tools import sleep
from .project import Project


class Activity:
    HomeActivity = 'com.xunmeng.pinduoduo/com.xunmeng.pinduoduo.ui.activity.HomeActivity'
    NewPageActivity = 'com.xunmeng.pinduoduo/com.xunmeng.pinduoduo.activity.NewPageActivity'


class ResourceID:
    icon_icon = 'com.miui.home:id/icon_icon'  # 桌面图标


class PDD(Project):
    def __init__(self, deviceSN):
        super(PDD, self).__init__(deviceSN)

    def openApp(self):
        self.adbIns.pressHomeKey()
        self.uIAIns.click(ResourceID.icon_icon, contentDesc='拼多多')

    def enterHumanServiceInterface(self):
        self.reopenApp()
        self.uIAIns.click(text='个人中心')
        self.uIAIns.click(text='官方客服')
        self.uIAIns.click(text='联系官方客服')

    def continueToConsulting(self):
        while not self.uIAIns.getDict(text='茫茫人海，相遇就是缘分，我是人工客服：火多多'):
            self.uIAIns.click(text='继续咨询')
            self.sendQuestion()
            sleep(10)

    def sendQuestion(self):
        if Activity.NewPageActivity not in self.adbIns.getCurrentFocus():
            return
        self.uIAIns.click(text='请描述下您遇到的问题～')
        self.adbIns.inputText('210901-646667386383208超时发货好几天了，但是一直没有收到赔付，麻烦看一下怎么回事儿')
        self.uIAIns.click(text='发送')

    def contactHumanService(self):
        self.enterHumanServiceInterface()
        if not self.uIAIns.getDict(text='当前人工客服繁忙，你已进入排队，请耐心等待'):
            while not self.uIAIns.click(text='联系人工客服'):
                self.uIAIns.click(text='请描述下您遇到的问题～', xml=self.uIAIns.xml)
                self.adbIns.inputText('人工服务')
                self.uIAIns.click(text='发送')
        self.uIAIns.click(text='以上都不是')
        self.uIAIns.click(text='非订单问题，点此直接进入人工客服')
        try:
            self.continueToConsulting()
        except FileNotFoundError as e:
            print(e)
            self.uIAIns.clickByScreenText('继续咨询')
            self.continueToConsulting()
        self.sendQuestion()
