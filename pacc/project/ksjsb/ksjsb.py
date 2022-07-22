"""快手极速版模块"""
from datetime import datetime, timedelta
from time import time
from xml.parsers.expat import ExpatError
from ...base import sleep, show_datetime
from ...mysql import RetrieveKSJSB, UpdateKSJSB
from ...multi import run_threads_with_args_list, run_threads_with_functions
from ..project import Project
from . import resourceID, activity, bounds


class KSJSB(Project):
    def __init__(self, deviceSN):
        super(KSJSB, self).__init__(deviceSN)
        self.startDay = datetime.now().day
        self.dbr = RetrieveKSJSB(deviceSN)
        self.currentFocus = ''
        self.exitLiveCnt = 0

    def shopping(self):
        self.enterWealthInterface()
        print('逛街')
        try:
            self.uia_ins.click(text='浏览低价商品领金币')
        except FileNotFoundError:
            self.shopping()

    def openTreasureBox(self):
        # 60*5, 60*9, 1200
        self.enterWealthInterface()
        print('开宝箱')
        try:
            if self.uia_ins.click(text='开宝箱得金币', xml=self.uia_ins.xml):
                if self.uia_ins.clickByXMLTexts(['去看视频再赚', '看精彩视频赚更多', '金币看视频就赚']):
                    sleep(60)
                    self.adbIns.press_back_key()
                    self.uia_ins.click(resourceID.award_video_close_dialog_abandon_button)
                self.uia_ins.xml = ''
        except FileNotFoundError:
            self.openTreasureBox()

    def watchLive(self):
        self.enterWealthInterface()
        self.randomSwipe(True)
        print('看直播')
        while True:
            try:
                while self.uia_ins.getCP(text='live_activity_download') == (0, 0):
                    self.randomSwipe(True)
                if not self.uia_ins.getDict(text='live_activity_download', xml=self.uia_ins.xml):
                    self.watchLive()
                    return
                if self.uia_ins.clickByXMLTexts(['观看精彩直播得110金币', '每次110金币'],
                                               xml=self.uia_ins.xml):
                    sleep(6)
                    if self.uia_ins.getDict(resourceID.award_title_prefix):
                        self.uia_ins.click(resourceID.nick)
                    sleep(20)
                    if activity.PhotoDetailActivity not in self.adbIns.get_current_focus():
                        self.watchLive()
                        return
                    sleep(89)
                    self.exitLive()
                else:
                    break
            except FileNotFoundError as e:
                print(e)
                self.watchLive()

    def exitLive(self):
        print('exitLiveCnt=%d' % self.exitLiveCnt)
        self.exitLiveCnt += 1
        if self.exitLiveCnt >= 10:
            self.reopenApp()
            self.exitLiveCnt = 0
            return
        self.adbIns.press_back_key()
        cf = self.adbIns.get_current_focus()
        if activity.AwardFeedFlowActivity in cf:
            self.adbIns.press_back_key()
        if activity.PhotoDetailActivity not in cf:
            return
        try:
            if self.uia_ins.click(resourceID.live_exit_button):
                self.uia_ins.xml = ''
            self.uia_ins.click(resourceID.exit_btn, xml=self.uia_ins.xml)
        except FileNotFoundError as e:
            print(e)
            self.exitLive()
        if activity.PhotoDetailActivity in self.adbIns.get_current_focus():
            self.exitLive()
        self.exitLiveCnt = 0

    def viewAds(self):
        self.enterWealthInterface()
        self.randomSwipe(True)
        print('看广告')
        while True:
            try:
                if activity.KwaiYodaWebViewActivity not in self.adbIns.get_current_focus():
                    self.viewAds()
                    return
                elif self.uia_ins.clickByXMLTexts(['观看广告单日最高可得',
                                                  '每次100金币，每天1000金币']):
                    sleep(50)
                    self.adbIns.press_back_key()
                    if activity.HomeActivity not in self.adbIns.get_current_focus():
                        self.enterWealthInterface()
                        print('等待看广告')
                        sleep(1200)
                        self.viewAds()
                else:
                    break
            except FileNotFoundError as e:
                print(e)
                self.viewAds()

    def signIn(self):
        self.enterWealthInterface()
        print('签到')
        if not self.uia_ins.getDict(text='今天签到可领'):
            return
        try:
            while self.uia_ins.getCP(text='今天签到可领') == (0, 0):
                self.randomSwipe(True)
            self.uia_ins.click(text='今天签到可领')
            self.afterSignIn()
        except FileNotFoundError as e:
            print(e)
            self.signIn()

    def afterSignIn(self):
        if self.uia_ins.click('', '打开签到提醒'):  # 需要授权
            self.uia_ins.xml = ''
        elif self.uia_ins.click('', '看广告再得', xml=self.uIAIns.xml):
            sleep(60)
            self.adbIns.press_back_key()
            self.uia_ins.xml = ''
        if self.uia_ins.getDict(text='邀请好友赚更多'):
            self.enterWealthInterface()

    def enterWealthInterface(self, reopen=True, sleepTime=16):
        if reopen:
            self.reopenApp()
        try:
            if not self.uia_ins.click(resourceID.red_packet_anim, xml=self.uia_ins.xml) and \
                    activity.MiniAppActivity0 in self.adbIns.get_current_focus():
                self.randomSwipe(True)
                self.enterWealthInterface(False)
                return
            sleep(sleepTime)
            if activity.KwaiYodaWebViewActivity not in self.adbIns.get_current_focus():
                self.enterWealthInterface(sleepTime=sleepTime+6)
            self.uia_ins.getCurrentUIHierarchy()
            print('已进入财富界面')
            if self.uia_ins.click(text='立即领取今日现金'):
                self.uia_ins.xml = ''
                self.enterWealthInterface()
                return
            if self.uia_ins.clickByXMLTexts(texts=['立即签到', '签到立得'], xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
                self.afterSignIn()
            if self.uia_ins.click(bounds=bounds.closeCongratulations, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
        except (FileNotFoundError, ExpatError) as e:
            print(e)
            self.enterWealthInterface(False)

    def enterMyWealthInterface(self, reopen=True):
        self.enterWealthInterface(reopen)
        self.uia_ins.clickByXMLTexts(texts=['可用抵用金(张)', '可用抵用金（张）'])
        sleep(9)

    def updateWealth(self, reopen=True):
        print('更新财富值')
        self.enterMyWealthInterface(reopen)
        try:
            goldCoins, cashCoupons = self.getWealth()
            if not goldCoins == self.dbr.goldCoins:
                UpdateKSJSB(self.adbIns.device.SN).updateGoldCoins(goldCoins)
            if not cashCoupons == self.dbr.cashCoupons:
                UpdateKSJSB(self.adbIns.device.SN).updateCashCoupons(cashCoupons)
        except FileNotFoundError as e:
            print(e)
            self.updateWealth(False)

    def getWealth(self):
        dics = self.uia_ins.getDicts(bounds='[-1,351][-1,459]')
        # print(dics)
        goldCoins = dics[0]['@text']
        if 'w' in goldCoins:
            goldCoins = 10000 * float(goldCoins[:-1])
        else:
            goldCoins = float(goldCoins)
        cashCoupons = float(dics[1]['@text'])
        # print(goldCoins, cashCoupons)
        return goldCoins, cashCoupons

    def openApp(self, reopen=True):
        if reopen:
            super(KSJSB, self).openApp(activity.HomeActivity)
            sleep(19)
        try:
            if self.uia_ins.click(resourceID.close):
                self.uia_ins.xml = ''
            if self.uia_ins.click(resourceID.iv_close_common_dialog, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
            if self.uia_ins.click(resourceID.positive, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
            if self.uia_ins.click(resourceID.tv_upgrade_now, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
                self.adbIns.press_back_key()
            while not self.uia_ins.getDict(resourceID.red_packet_anim, xml=self.uia_ins.xml):
                if activity.HomeActivity not in self.adbIns.get_current_focus():
                    self.reopenApp()
                    return
                self.randomSwipe(True)
                self.uia_ins.xml = ''
        except (FileNotFoundError, ExpatError) as e:
            print(e)
            self.randomSwipe(True)
            sleep(6)
            self.reopenApp()

    def initSleepTime(self):
        print('restTime=%s' % self.restTime)
        if self.restTime <= 0:
            return
        elif self.uia_ins.getDict(resourceID.live_simple_play_swipe_text, xml=self.uia_ins.xml):
            pass
        elif self.uia_ins.getDict(resourceID.open_long_atlas, xml=self.uia_ins.xml):
            pass
        else:
            return
        self.restTime = 0

    def watchVideo(self):
        if self.reopenAppPerHour(False):
            self.adbIns.keep_online()
            self.openTreasureBox()
            self.reopenApp()
        try:
            if datetime.now().hour > 5 and self.uia_ins.getDict(resourceID.red_packet_anim):
                if not self.uia_ins.getDict(resourceID.cycle_progress, xml=self.uia_ins.xml):
                    self.viewAds()
                    self.watchLive()
                    self.openTreasureBox()
                    self.signIn()
                    self.updateWealth()
                    self.freeMemory()
                    self.adbIns.press_power_key()
                    self.startDay = (datetime.now() + timedelta(days=1)).day
                    return
            currentFocus = self.adbIns.get_current_focus()
            if activity.PhotoDetailActivity in currentFocus:
                self.exitLive()
                self.randomSwipe(True)
            elif activity.UserProfileActivity in currentFocus:
                self.adbIns.press_back_key()
            elif activity.KwaiYodaWebViewActivity in currentFocus:
                self.adbIns.press_back_key()
            elif activity.SearchActivity in currentFocus:
                self.reopenApp()
            self.uia_ins.click(resourceID.button2, xml=self.uia_ins.xml)
            self.initSleepTime()
        except (FileNotFoundError, ExpatError) as e:
            print(e)
            self.randomSwipe(True)
        self.restTime = self.restTime + self.lastTime - time()
        self.lastTime = time()
        self.randomSwipe()
        self.uia_ins.xml = ''

    def randomSwipe(self, initRestTime=False):
        super(KSJSB, self).randomSwipe(360, 390, 360, 390, 1160, 1190, 260, 290, initRestTime)

    def mainloop(self):
        while True:
            if datetime.now().day == self.startDay:
                self.watchVideo()
            else:
                self.openTreasureBox()
                self.viewAds()
                break
            show_datetime('ksjsb.mainloop')
