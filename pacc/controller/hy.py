from pacc.tools import sleep
from pacc.project.project import Project


class Activity:
    KiwiChatActivity = 'com.sh.shuihulu.kiwi/k.i.w.i.m.assemble.activity.KiwiChatActivity'
    AccessibilitySettingsActivity = 'u0 com.android.settings/com.android.settings' \
                                    '.Settings$AccessibilitySettingsActivity'
    MainActivity = 'com.sh.shuihulu.kiwi/com.yicheng.assemble.activity.MainActivity'
    KiwiPicturePreviewActivity = 'com.sh.shuihulu.kiwi/k.i.w.i.m.assemble.activity.KiwiPicturePreviewActivity'


class ResourceID:
    iv_tippopu_close = 'com.sh.shuihulu.kiwi:id/iv_tippopu_close'  # 回复男生搭讪需先录制交友宣言和真人认证，认证后可以继续领取搭讪红包哦
    atv_right = 'com.sh.shuihulu.kiwi:id/atv_right'  # 我知道了（对方余额不足，可能导致通话结束,提醒一下对方充值哦～）


class Text:
    toMakeFriendsDeclaration = '去交友宣言'


class HY(Project):
    def __init__(self, deviceSN):
        super(HY, self).__init__(deviceSN)

    def openApp(self):
        super(HY, self).openApp(Activity.MainActivity)
        sleep(6)

    def mainloop(self, reopen=False):
        self.uIAIns.tap([56, 126])
        if reopen:
            self.reopenApp()
        currentFocus = self.adbIns.getCurrentFocus()
        if 'com.sh.shuihulu.kiwi' not in currentFocus:
            self.uIAIns.tap([56, 126])
            self.mainloop(True)
            return
        elif Activity.KiwiPicturePreviewActivity in currentFocus:
            self.adbIns.pressBackKey()
        try:
            # if self.uIAIns.click(ResourceID.iv_tippopu_close):
            #     self.uIAIns.xml = ''
            # if self.uIAIns.click(text=Text.toMakeFriendsDeclaration):
            #      = ''
            if self.uIAIns.click(text='恭喜获得'):
                self.uIAIns.xml = ''
            self.uIAIns.click(ResourceID.atv_right, xml=self.uIAIns.xml)
        except FileNotFoundError as e:
            print(e)
            self.uIAIns.tap([56, 126])
            self.mainloop(True)
            return
        self.uIAIns.tap([56, 126])
