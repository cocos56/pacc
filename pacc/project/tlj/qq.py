from ...tools import sleep
from ..project import Project


class Activity:
    SplashActivity = 'com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity'  # QQ程序
    TroopActivity = 'com.tencent.qqlite/com.tencent.mobileqq.activity.contact.troop.TroopActivity'  # 群通知
    TroopAssistantActivity = 'com.tencent.qqlite/com.tencent.mobileqq.activity.TroopAssistantActivity'  # 群助手
    ChatActivity = 'com.tencent.qqlite/com.tencent.mobileqq.activity.ChatActivity'  # 聊天界面


class ResourceID:
    unchecked_msg_num = 'com.tencent.qqlite:id/unchecked_msg_num'  # 消息按钮
    unreadmsg = 'com.tencent.qqlite:id/unreadmsg'  # 主界面未读消息项（多个对话框）
    chat_item_content_layout = 'com.tencent.qqlite:id/chat_item_content_layout'  # 聊天界面消息项（多条消息）


class QQ(Project):
    def __init__(self, deviceSN):
        super(QQ, self).__init__(deviceSN, False)

    def getUnreadMsg(self):
        self.reopenApp()
        if self.uIAIns.click(ResourceID.unreadmsg, offset_x=-200):
            if Activity.ChatActivity not in self.adbIns.getCurrentFocus():
                self.getUnreadMsg()
                return
            print(self.getLatestMsg())

    def getLatestMsg(self):
        res = self.uIAIns.getDicts(ResourceID.chat_item_content_layout)
        if res:
            return res[-1]

    def openApp(self):
        super(QQ, self).openApp(Activity.SplashActivity)
        sleep(6)
