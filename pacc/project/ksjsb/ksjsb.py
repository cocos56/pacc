"""快手极速版模块"""
from datetime import datetime, timedelta
from time import time
from xml.parsers.expat import ExpatError

from .activity import Activity
from .bounds import Bounds
from .resource_id import ResourceID
from ..project import Project
from ...base import sleep, show_datetime, print_err
from ...mysql import RetrieveKSJSB, UpdateKSJSB


class KSJSB(Project):
    """快手极速版类"""
    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备编号
        """
        super().__init__(serial_num)
        self.start_day = datetime.now().day
        self.dbr = RetrieveKSJSB(serial_num)
        self.exit_live_cnt = 0

    def shopping(self):
        """逛街"""
        self.enterWealthInterface()
        print('逛街')
        try:
            self.uia_ins.click(text='浏览低价商品领金币')
        except FileNotFoundError as err:
            print_err(err)
            self.shopping()

    def open_treasure_box(self):
        """开宝箱"""
        # 60*5, 60*9, 1200
        self.enterWealthInterface()
        print('开宝箱')
        try:
            if self.uia_ins.click(text='开宝箱得金币', xml=self.uia_ins.xml):
                if self.uia_ins.clickByXMLTexts(['去看视频再赚', '看精彩视频赚更多', '金币看视频就赚']):
                    sleep(60)
                    self.adb_ins.press_back_key()
                    self.uia_ins.click(ResourceID.award_video_close_dialog_abandon_button)
                self.uia_ins.xml = ''
        except FileNotFoundError as err:
            print_err(err)
            self.open_treasure_box()

    def watch_live(self):
        """看直播"""
        self.enterWealthInterface()
        self.randomSwipe(True)
        print('看直播')
        while True:
            try:
                while self.uia_ins.getCP(text='live_activity_download') == (0, 0):
                    self.randomSwipe(True)
                if not self.uia_ins.getDict(text='live_activity_download', xml=self.uia_ins.xml):
                    self.watch_live()
                    return
                if self.uia_ins.clickByXMLTexts(['观看精彩直播得110金币', '每次110金币'],
                                                xml=self.uia_ins.xml):
                    sleep(6)
                    if self.uia_ins.getDict(ResourceID.award_title_prefix):
                        self.uia_ins.click(ResourceID.nick)
                    sleep(20)
                    if Activity.PhotoDetailActivity not in self.adb_ins.get_current_focus():
                        self.watch_live()
                        return
                    sleep(89)
                    self.exitLive()
                else:
                    break
            except FileNotFoundError as err:
                print_err(err)
                self.watch_live()

    def exitLive(self):
        print(f'exit_live_cnt={self.exit_live_cnt}')
        self.exit_live_cnt += 1
        if self.exit_live_cnt >= 10:
            self.reopenApp()
            self.exit_live_cnt = 0
            return
        self.adb_ins.press_back_key()
        cf = self.adb_ins.get_current_focus()
        if Activity.AwardFeedFlowActivity in cf:
            self.adb_ins.press_back_key()
        if Activity.PhotoDetailActivity not in cf:
            return
        try:
            if self.uia_ins.click(ResourceID.live_exit_button):
                self.uia_ins.xml = ''
            self.uia_ins.click(ResourceID.exit_btn, xml=self.uia_ins.xml)
        except FileNotFoundError as err:
            print_err(err)
            self.exitLive()
        if Activity.PhotoDetailActivity in self.adb_ins.get_current_focus():
            self.exitLive()
        self.exit_live_cnt = 0

    def viewAds(self):
        self.enterWealthInterface()
        self.randomSwipe(True)
        print('看广告')
        while True:
            try:
                if Activity.KwaiYodaWebViewActivity not in self.adb_ins.get_current_focus():
                    self.viewAds()
                    return
                elif self.uia_ins.clickByXMLTexts(['观看广告单日最高可得',
                                                   '每次100金币，每天1000金币']):
                    sleep(50)
                    self.adb_ins.press_back_key()
                    if Activity.HomeActivity not in self.adb_ins.get_current_focus():
                        self.enterWealthInterface()
                        print('等待看广告')
                        sleep(1200)
                        self.viewAds()
                else:
                    break
            except FileNotFoundError as err:
                print_err(err)
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
        except FileNotFoundError as err:
            print_err(err)
            self.signIn()

    def afterSignIn(self):
        if self.uia_ins.click('', '打开签到提醒'):  # 需要授权
            self.uia_ins.xml = ''
        elif self.uia_ins.click('', '看广告再得', xml=self.uia_ins.xml):
            sleep(60)
            self.adb_ins.press_back_key()
            self.uia_ins.xml = ''
        if self.uia_ins.getDict(text='邀请好友赚更多'):
            self.enterWealthInterface()

    def enterWealthInterface(self, reopen=True, sleepTime=16):
        if reopen:
            self.reopenApp()
        try:
            if not self.uia_ins.click(ResourceID.red_packet_anim, xml=self.uia_ins.xml) and \
                    Activity.MiniAppActivity0 in self.adb_ins.get_current_focus():
                self.randomSwipe(True)
                self.enterWealthInterface(False)
                return
            sleep(sleepTime)
            if Activity.KwaiYodaWebViewActivity not in self.adb_ins.get_current_focus():
                self.enterWealthInterface(sleepTime=sleepTime + 6)
            self.uia_ins.getCurrentUIHierarchy()
            print('已进入财富界面')
            if self.uia_ins.click(text='立即领取今日现金'):
                self.uia_ins.xml = ''
                self.enterWealthInterface()
                return
            if self.uia_ins.clickByXMLTexts(texts=['立即签到', '签到立得'], xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
                self.afterSignIn()
            if self.uia_ins.click(bounds=Bounds.closeCongratulations, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
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
                UpdateKSJSB(self.adb_ins.device.SN).updateGoldCoins(goldCoins)
            if not cashCoupons == self.dbr.cashCoupons:
                UpdateKSJSB(self.adb_ins.device.SN).updateCashCoupons(cashCoupons)
        except FileNotFoundError as err:
            print_err(err)
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
            super(KSJSB, self).openApp(Activity.HomeActivity)
            sleep(19)
        try:
            if self.uia_ins.click(ResourceID.close):
                self.uia_ins.xml = ''
            if self.uia_ins.click(ResourceID.iv_close_common_dialog, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
            if self.uia_ins.click(ResourceID.positive, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
            if self.uia_ins.click(ResourceID.tv_upgrade_now, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
                self.adb_ins.press_back_key()
            while not self.uia_ins.getDict(ResourceID.red_packet_anim, xml=self.uia_ins.xml):
                if Activity.HomeActivity not in self.adb_ins.get_current_focus():
                    self.reopenApp()
                    return
                self.randomSwipe(True)
                self.uia_ins.xml = ''
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            self.randomSwipe(True)
            sleep(6)
            self.reopenApp()

    def initSleepTime(self):
        print(f'restTime={self.restTime}')
        if self.restTime <= 0:
            return
        elif self.uia_ins.getDict(ResourceID.live_simple_play_swipe_text, xml=self.uia_ins.xml):
            pass
        elif self.uia_ins.getDict(ResourceID.open_long_atlas, xml=self.uia_ins.xml):
            pass
        else:
            return
        self.restTime = 0

    def watchVideo(self):
        if self.reopenAppPerHour(False):
            self.adb_ins.keep_online()
            self.open_treasure_box()
            self.reopenApp()
        try:
            if datetime.now().hour > 5 and self.uia_ins.getDict(ResourceID.red_packet_anim):
                if not self.uia_ins.getDict(ResourceID.cycle_progress, xml=self.uia_ins.xml):
                    self.viewAds()
                    self.watch_live()
                    self.open_treasure_box()
                    self.signIn()
                    self.updateWealth()
                    self.freeMemory()
                    self.adb_ins.press_power_key()
                    self.start_day = (datetime.now() + timedelta(days=1)).day
                    return
            currentFocus = self.adb_ins.get_current_focus()
            if Activity.PhotoDetailActivity in currentFocus:
                self.exitLive()
                self.randomSwipe(True)
            elif Activity.UserProfileActivity in currentFocus:
                self.adb_ins.press_back_key()
            elif Activity.KwaiYodaWebViewActivity in currentFocus:
                self.adb_ins.press_back_key()
            elif Activity.SearchActivity in currentFocus:
                self.reopenApp()
            self.uia_ins.click(ResourceID.button2, xml=self.uia_ins.xml)
            self.initSleepTime()
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            self.randomSwipe(True)
        self.restTime = self.restTime + self.lastTime - time()
        self.lastTime = time()
        self.randomSwipe()
        self.uia_ins.xml = ''

    def randomSwipe(self, initRestTime=False):
        super().randomSwipe(360, 390, 360, 390, 1160, 1190, 260, 290, initRestTime)

    def mainloop(self):
        while True:
            if datetime.now().day == self.start_day:
                self.watchVideo()
            else:
                self.open_treasure_box()
                self.viewAds()
                break
            show_datetime('ksjsb.mainloop')
