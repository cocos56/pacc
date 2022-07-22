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
        self.enter_wealth_interface()
        print('逛街')
        try:
            self.uia_ins.click(text='浏览低价商品领金币')
        except FileNotFoundError as err:
            print_err(err)
            self.shopping()

    def open_treasure_box(self):
        """开宝箱"""
        # 60*5, 60*9, 1200
        self.enter_wealth_interface()
        print('开宝箱')
        try:
            if self.uia_ins.click(text='开宝箱得金币', xml=self.uia_ins.xml):
                if self.uia_ins.click_by_xml_texts(['去看视频再赚', '看精彩视频赚更多', '金币看视频就赚']):
                    sleep(60)
                    self.adb_ins.press_back_key()
                    self.uia_ins.click(ResourceID.award_video_close_dialog_abandon_button)
                self.uia_ins.xml = ''
        except FileNotFoundError as err:
            print_err(err)
            self.open_treasure_box()

    def watch_live(self):
        """看直播"""
        self.enter_wealth_interface()
        self.random_swipe(True)
        print('看直播')
        while True:
            try:
                while self.uia_ins.get_point(text='live_activity_download') == (0, 0):
                    self.random_swipe(True)
                if not self.uia_ins.get_dict(text='live_activity_download', xml=self.uia_ins.xml):
                    self.watch_live()
                    return
                if self.uia_ins.click_by_xml_texts(
                        ['观看精彩直播得110金币', '每次110金币'], xml=self.uia_ins.xml):
                    sleep(6)
                    if self.uia_ins.get_dict(ResourceID.award_title_prefix):
                        self.uia_ins.click(ResourceID.nick)
                    sleep(20)
                    if Activity.PhotoDetailActivity not in self.adb_ins.get_current_focus():
                        self.watch_live()
                        return
                    sleep(89)
                    self.exit_live()
                else:
                    break
            except FileNotFoundError as err:
                print_err(err)
                self.watch_live()

    def exit_live(self):
        """退出直播界面"""
        print(f'exit_live_cnt={self.exit_live_cnt}')
        self.exit_live_cnt += 1
        if self.exit_live_cnt >= 10:
            self.reopen_app()
            self.exit_live_cnt = 0
            return
        self.adb_ins.press_back_key()
        current_focus = self.adb_ins.get_current_focus()
        if Activity.AwardFeedFlowActivity in current_focus:
            self.adb_ins.press_back_key()
        if Activity.PhotoDetailActivity not in current_focus:
            return
        try:
            if self.uia_ins.click(ResourceID.live_exit_button):
                self.uia_ins.xml = ''
            self.uia_ins.click(ResourceID.exit_btn, xml=self.uia_ins.xml)
        except FileNotFoundError as err:
            print_err(err)
            self.exit_live()
        if Activity.PhotoDetailActivity in self.adb_ins.get_current_focus():
            self.exit_live()
        self.exit_live_cnt = 0

    def view_ads(self):
        """看广告"""
        self.enter_wealth_interface()
        self.random_swipe(True)
        print('看广告')
        while True:
            try:
                if Activity.KwaiYodaWebViewActivity not in self.adb_ins.get_current_focus():
                    self.view_ads()
                    return
                if self.uia_ins.click_by_xml_texts(['观看广告单日最高可得', '每次100金币，每天1000金币']):
                    sleep(50)
                    self.adb_ins.press_back_key()
                    if Activity.HomeActivity not in self.adb_ins.get_current_focus():
                        self.enter_wealth_interface()
                        print('等待看广告')
                        sleep(1200)
                        self.view_ads()
                else:
                    break
            except FileNotFoundError as err:
                print_err(err)
                self.view_ads()

    def sign_in(self):
        """签到"""
        self.enter_wealth_interface()
        print('签到')
        if not self.uia_ins.get_dict(text='今天签到可领'):
            return
        try:
            while self.uia_ins.get_point(text='今天签到可领') == (0, 0):
                self.random_swipe(True)
            self.uia_ins.click(text='今天签到可领')
            self.after_sign_in()
        except FileNotFoundError as err:
            print_err(err)
            self.sign_in()

    def after_sign_in(self):
        """执行签到之后"""
        if self.uia_ins.click('', '打开签到提醒'):  # 需要授权
            self.uia_ins.xml = ''
        elif self.uia_ins.click('', '看广告再得', xml=self.uia_ins.xml):
            sleep(60)
            self.adb_ins.press_back_key()
            self.uia_ins.xml = ''
        if self.uia_ins.get_dict(text='邀请好友赚更多'):
            self.enter_wealth_interface()

    def enter_wealth_interface(self, reopen=True, sleep_time=16):
        """进入财富界面

        param reopen: 是否需要重启快手极速版APP
        param sleep_time: 睡眠时间
        """
        if reopen:
            self.reopen_app()
        try:
            if not self.uia_ins.click(ResourceID.red_packet_anim, xml=self.uia_ins.xml) and \
                    Activity.MiniAppActivity0 in self.adb_ins.get_current_focus():
                self.random_swipe(True)
                self.enter_wealth_interface(False)
                return
            sleep(sleep_time)
            if Activity.KwaiYodaWebViewActivity not in self.adb_ins.get_current_focus():
                self.enter_wealth_interface(sleep_time=sleep_time + 6)
            self.uia_ins.getCurrentUIHierarchy()
            print('已进入财富界面')
            if self.uia_ins.click(text='立即领取今日现金'):
                self.uia_ins.xml = ''
                self.enter_wealth_interface()
                return
            if self.uia_ins.click_by_xml_texts(texts=['立即签到', '签到立得'], xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
                self.after_sign_in()
            if self.uia_ins.click(bounds=Bounds.closeCongratulations, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            self.enter_wealth_interface(False)

    def enterMyWealthInterface(self, reopen=True):
        """进入我的财富界面

        param reopen: 是否需要重启快手极速版APP
        """
        self.enter_wealth_interface(reopen)
        self.uia_ins.click_by_xml_texts(texts=['可用抵用金(张)', '可用抵用金（张）'])
        sleep(9)

    def updateWealth(self, reopen=True):
        """更新财富值

        param reopen: 是否需要重启快手极速版APP
        """
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
        """获取财富值"""
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
        """打开快手极速版APP

        param reopen: 是否需要重启快手极速版APP
        """
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
            while not self.uia_ins.get_dict(ResourceID.red_packet_anim, xml=self.uia_ins.xml):
                if Activity.HomeActivity not in self.adb_ins.get_current_focus():
                    self.reopen_app()
                    return
                self.random_swipe(True)
                self.uia_ins.xml = ''
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            self.random_swipe(True)
            sleep(6)
            self.reopen_app()

    def initSleepTime(self):
        """初始化睡眠时间"""
        print(f'restTime={self.rest_time}')
        if self.rest_time <= 0:
            return
        elif self.uia_ins.get_dict(ResourceID.live_simple_play_swipe_text, xml=self.uia_ins.xml):
            pass
        elif self.uia_ins.get_dict(ResourceID.open_long_atlas, xml=self.uia_ins.xml):
            pass
        else:
            return
        self.rest_time = 0

    def watch_video(self):
        """看视频"""
        if self.reopenAppPerHour(False):
            self.adb_ins.keep_online()
            self.open_treasure_box()
            self.reopen_app()
        try:
            if datetime.now().hour > 5 and self.uia_ins.get_dict(ResourceID.red_packet_anim):
                if not self.uia_ins.get_dict(ResourceID.cycle_progress, xml=self.uia_ins.xml):
                    self.view_ads()
                    self.watch_live()
                    self.open_treasure_box()
                    self.sign_in()
                    self.updateWealth()
                    self.freeMemory()
                    self.adb_ins.press_power_key()
                    self.start_day = (datetime.now() + timedelta(days=1)).day
                    return
            current_focus = self.adb_ins.get_current_focus()
            if Activity.PhotoDetailActivity in current_focus:
                self.exit_live()
                self.random_swipe(True)
            elif Activity.UserProfileActivity in current_focus:
                self.adb_ins.press_back_key()
            elif Activity.KwaiYodaWebViewActivity in current_focus:
                self.adb_ins.press_back_key()
            elif Activity.SearchActivity in current_focus:
                self.reopen_app()
            self.uia_ins.click(ResourceID.button2, xml=self.uia_ins.xml)
            self.initSleepTime()
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            self.random_swipe(True)
        self.rest_time = self.rest_time + self.last_time - time()
        self.last_time = time()
        self.random_swipe()
        self.uia_ins.xml = ''

    # pylint: disable=arguments-differ
    def random_swipe(self, init_rest_time=False):
        """随机滑动一段长度

        :param init_rest_time: 是否初始化剩余时间
        """
        super().random_swipe(360, 390, 360, 390, 1160, 1190, 260, 290, init_rest_time)

    def mainloop(self):
        """主循环"""
        while True:
            if datetime.now().day == self.start_day:
                self.watch_video()
            else:
                self.open_treasure_box()
                self.view_ads()
                break
            show_datetime('ksjsb.mainloop')
