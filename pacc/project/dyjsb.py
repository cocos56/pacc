from time import time
from datetime import datetime, timedelta
from xml.parsers.expat import ExpatError
from .project import Project
from ..tools import sleep, showDatetime


class Activity:
    SplashActivity = 'com.ss.android.ugc.aweme.lite/com.ss.android.ugc.aweme.splash.SplashActivity'  # 抖音极速版程序入口
    ExcitingVideoActivity = 'com.ss.android.ugc.aweme.lite/com.ss.android.excitingvideo.ExcitingVideoActivity'  # 广告界面


class Text:
    iKnow = '我知道了'  # 儿童/青少年模式提醒


class ResourceID:
    av0 = 'com.ss.android.ugc.aweme.lite:id/av0'  # 关闭（12个红包 超多现金福利）
    bai = 'com.ss.android.ugc.aweme.lite:id/bai'  # 关闭（邀请5个好友必赚136元/恭喜你被红包砸中）
    bc1 = 'com.ss.android.ugc.aweme.lite:id/bc1'  # 开红包（恭喜你被红包砸中）
    e0p = 'com.ss.android.ugc.aweme.lite:id/e0p'  # 暂时不要（发现通讯录好友）
    c1m = 'com.ss.android.ugc.aweme.lite:id/c1m'  # 开宝箱（财富界面）


class Bounds:
    WatchAdsToEarnGoldCoins = '[206,1201][874,1316]'


class DYJSB(Project):
    def __init__(self, deviceSN):
        super(DYJSB, self).__init__(deviceSN)
        self.startDay = datetime.now().day

    def enterWealthInterface(self):
        self.reopenApp()
        if not self.uIAIns.clickByScreenTexts(['来赚钱', '金币']):
            self.enterWealthInterface()
            return
        sleep(20)
        print('已进入财富界面')
        if self.uIAIns.clickByScreenText('立即签到'):
            if self.uIAIns.clickByScreenTexts(['看广告视频再赚', '打开签到提醒']):
                self.afterEnterAdsInterface()
            self.uIAIns.txt = ''

    def openTreasureBox(self):
        self.enterWealthInterface()
        if self.uIAIns.clickByScreenText('开宝箱得金币', txt=self.uIAIns.txt):
            if self.uIAIns.clickByScreenText('看广告视频再赚'):
                self.afterEnterAdsInterface()

    def viewAds(self):
        self.enterWealthInterface()
        if self.uIAIns.clickByScreenText('看广告赚金币', txt=self.uIAIns.txt):
            self.uIAIns.clickByScreenText('看广告视频再赚')
            self.afterEnterAdsInterface()

    def afterEnterAdsInterface(self):
        sleep(20)
        if Activity.ExcitingVideoActivity in self.adbIns.get_current_focus():
            sleep(60)
            self.adbIns.pressBackKey()
        if Activity.ExcitingVideoActivity in self.adbIns.get_current_focus() and self.uIAIns.click(
                contentDesc='再看一个获取'):
            sleep(60)
            self.adbIns.pressBackKey()

    def openApp(self):
        super(DYJSB, self).openApp(Activity.SplashActivity)
        sleep(20)
        try:
            if self.uIAIns.click(text=Text.iKnow):
                sleep(3)
                self.uIAIns.xml = ''
            if self.uIAIns.click(ResourceID.av0, xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            if self.uIAIns.click(ResourceID.e0p, xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            self.uIAIns.click(ResourceID.bai, xml=self.uIAIns.xml)
        except FileNotFoundError as e:
            print(e)

    def randomSwipe(self, initRestTime=False):
        super(DYJSB, self).randomSwipe(530, 560, 530, 560, 1160, 1190, 360, 390, initRestTime)

    def watchVideo(self):
        if datetime.now().hour == 23 and datetime.now().day == self.startDay:
            self.freeMemory()
            self.adbIns.pressPowerKey()
            self.startDay = (datetime.now() + timedelta(days=1)).day
            return
        try:
            self.uIAIns.click(ResourceID.bc1)
            self.uIAIns.click(ResourceID.bai, xml=self.uIAIns.xml)
        except (FileNotFoundError, ExpatError) as e:
            print(e)
        if self.reopenAppPerHour(False):
            self.adbIns.keepOnline()
            self.openTreasureBox()
            self.viewAds()
            self.reopenApp()
        # if Activity.SplashActivity not in self.adbIns.getCurrentFocus():
        #     self.reopenApp()
        self.restTime = self.restTime + self.lastTime - time()
        self.lastTime = time()
        self.randomSwipe()

    def mainloop(self):
        if not self.adbIns.device.SN == '003001001':
            return
        while True:
            if datetime.now().day == self.startDay:
                self.watchVideo()
            else:
                break
            showDatetime('dyjsb.mainloop')
