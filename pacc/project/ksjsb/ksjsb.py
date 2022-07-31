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


# pylint: disable=too-many-instance-attributes
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
        self.last_video_username = ''
        self.last_video_description = ''
        self.last_video_music = ''
        self.not_same_video_cnt = 0

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
                self.uia_ins.tap((530, 1330), 6)
                if Activity.AwardVideoPlayActivity in self.adb_ins.get_current_focus():
                    sleep(60)
                    self.adb_ins.press_back_key()
                # if self.uia_ins.click_by_xml_texts(['去看视频再赚', '看精彩视频赚更多', '金币看视频就赚']):
                #     sleep(60)
                #     self.adb_ins.press_back_key()
                #     self.uia_ins.click(ResourceID.award_video_close_dialog_abandon_button)
                self.uia_ins.xml = ''
        except FileNotFoundError as err:
            print_err(err)
            # self.open_treasure_box()

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
                if self.uia_ins.click_by_xml_texts(
                        ['观看广告单日最高可得', '每次100金币，每天1000金币']):
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

    def enter_wealth_interface(self, reopen=True, sleep_time=29):
        """进入财富界面

        param reopen: 是否需要重启快手极速版APP
        param sleep_time: 睡眠时间
        """
        if reopen:
            self.reopen_app()
        print('准备进入财富界面')
        try:
            if not self.uia_ins.click(ResourceID.red_packet_anim) and \
                    Activity.MiniAppActivity0 in self.adb_ins.get_current_focus():
                self.random_swipe(True)
                self.enter_wealth_interface(False)
                return
            sleep(sleep_time)
            if Activity.KwaiYodaWebViewActivity not in self.adb_ins.get_current_focus():
                self.enter_wealth_interface(sleep_time=sleep_time + 6)
            self.uia_ins.get_current_ui_hierarchy()
            print('已进入财富界面')
            if self.uia_ins.click(text='立即领取今日现金'):
                self.uia_ins.xml = ''
                self.enter_wealth_interface()
                return
            if self.uia_ins.click_by_xml_texts(texts=['立即签到', '签到立得'],
                                               xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
                self.after_sign_in()
            if self.uia_ins.click(bounds=Bounds.closeCongratulations, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            # self.enter_wealth_interface(False)

    def open_exclusive_gold_coin_gift_pack(self):
        """领取专属金币礼包"""
        self.enter_wealth_interface()
        try:
            self.uia_ins.get_current_ui_hierarchy()
        except FileNotFoundError as err:
            print_err(err)
            self.adb_ins.swipe(600, 1830, 600, 1750)
            # self.uia_ins.click_by_screen_text()
            print(self.uia_ins.get_texts_from_pic())

    def enter_my_wealth_interface(self, reopen=True):
        """进入我的财富界面

        param reopen: 是否需要重启快手极速版APP
        """
        self.enter_wealth_interface(reopen)
        try:
            self.uia_ins.click_by_xml_texts(texts=['可用抵用金(张)', '可用抵用金（张）'])
        except FileNotFoundError as err:
            print_err(err)
            self.uia_ins.tap((668, 360))
        sleep(9)

    def update_wealth(self, reopen=True):
        """更新财富值

        param reopen: 是否需要重启快手极速版APP
        """
        print('更新财富值')
        self.enter_my_wealth_interface(reopen)
        try:
            gold_coins, cash_coupons = self.get_wealth()
            if gold_coins != self.dbr.gold_coins:
                UpdateKSJSB(self.adb_ins.device.serial_num).update_gold_coins(gold_coins)
            if cash_coupons != self.dbr.cash_coupons:
                UpdateKSJSB(self.adb_ins.device.serial_num).update_cash_coupons(cash_coupons)
        except FileNotFoundError as err:
            print_err(err)
            self.update_wealth(False)

    def get_wealth(self):
        """获取财富值"""
        print('正在获取财富值')
        dics = self.uia_ins.get_dict(index='0', text='我的收益')['node']
        # print(dics)
        # for i, v in enumerate(dics):
        #     print(i, v)
        gold_coins = dics[2]['@text']
        if 'w' in gold_coins:
            gold_coins = 10000 * float(gold_coins[:-1])
        else:
            gold_coins = float(gold_coins)
        cash_coupons = float(dics[7]['@text'])
        # print(f"gold_coins={gold_coins}, cash_coupons={cash_coupons}")
        return gold_coins, cash_coupons

    def change_money(self):
        """把金币兑换钱"""
        self.enter_wealth_interface()
        self.uia_ins.tap((866, 349), 6)
        webview_dic = self.uia_ins.get_dict(class_=ResourceID.WebView)
        cash = float(webview_dic['node'][0]['node'][1]['@text'])
        # print(cash)
        dics = webview_dic['node'][1]['node']
        for dic in dics[4:0:-1]:
            dic = dic['node']
            if isinstance(dic, list):
                dic = dic[0]
            money = float(dic['@text'][:-1])
            # print(dic)
            if cash >= money:
                print(money)
                self.uia_ins.click_by_bounds(dic['@bounds'])
                break
        self.uia_ins.click(text='立即兑换', xml=self.uia_ins.xml)
        self.uia_ins.tap((536, 1706), 12)
        self.uia_ins.click(text='立即提现')

    # pylint: disable=arguments-renamed
    def open_app(self, reopen=True):
        """打开快手极速版APP

        param reopen: 是否需要重启快手极速版APP
        """
        if reopen:
            super().open_app(Activity.HomeActivity)
            sleep(19)
        try:
            if self.uia_ins.click(ResourceID.close):
                self.uia_ins.xml = ''
            if self.uia_ins.click(ResourceID.iv_close_common_dialog, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
            if self.uia_ins.click(ResourceID.click_double, xml=self.uia_ins.xml):
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

    def init_sleep_time(self):
        """初始化睡眠时间"""
        print(f'restTime={self.rest_time}')
        if self.rest_time <= 0:
            return
        if self.uia_ins.get_dict(ResourceID.live_simple_play_swipe_text, xml=self.uia_ins.xml):
            pass
        elif self.uia_ins.get_dict(ResourceID.open_long_atlas, xml=self.uia_ins.xml):
            pass
        else:
            return
        self.rest_time = 0

    def is_same_video(self):
        """判断当前和上一次是否是同一视频"""
        try:
            last_video_username = self.uia_ins.get_dict(
                ResourceID.user_name_text_view, xml=self.uia_ins.xml)['@text']
        except TypeError as err:
            print_err(err)
            return False
        try:
            last_video_description = self.uia_ins.get_dict(
                ResourceID.caption_scroll_container, xml=self.uia_ins.xml)['node']['@text']
        except TypeError as err:
            print_err(err)
            last_video_description = ''
        last_video_music = self.uia_ins.get_dict(
            ResourceID.music_textview, xml=self.uia_ins.xml)['@text']
        # print(last_video_username, last_video_description, last_video_music)
        is_same_video_flag = last_video_username == self. \
            last_video_username and last_video_description == self. \
                                 last_video_description and last_video_music == self.last_video_music
        self.last_video_username = last_video_username
        self.last_video_description = last_video_description
        self.last_video_music = last_video_music
        if is_same_video_flag:
            self.not_same_video_cnt += 1
        else:
            self.not_same_video_cnt = 0
        return is_same_video_flag

    def watch_video(self):
        """看视频"""
        if self.reopen_app_per_hour(False):
            self.adb_ins.keep_online()
            # self.open_treasure_box()
            self.reopen_app()
        try:
            if datetime.now().hour > 5 and self.uia_ins.get_dict(ResourceID.red_packet_anim):
                if not self.uia_ins.get_dict(ResourceID.cycle_progress, xml=self.uia_ins.xml):
                    self.view_ads()
                    self.watch_live()
                    # self.open_treasure_box()
                    self.sign_in()
                    self.update_wealth()
                    self.free_memory()
                    self.adb_ins.press_power_key()
                    self.start_day = (datetime.now() + timedelta(days=1)).day
                    return
            current_focus = self.adb_ins.get_current_focus()
            if Activity.PhotoDetailActivity in current_focus:
                self.exit_live()
                self.random_swipe(True)
            elif Activity.LiveSlideActivity in current_focus:
                self.exit_live()
                self.random_swipe(True)
            elif Activity.UserProfileActivity in current_focus:
                self.adb_ins.press_back_key()
            elif Activity.KwaiYodaWebViewActivity in current_focus:
                self.adb_ins.press_back_key()
            elif Activity.SearchActivity in current_focus:
                self.reopen_app()
            elif self.uia_ins.get_dict(ResourceID.item_title, xml=self.uia_ins.xml):
                self.adb_ins.press_back_key()
            elif self.is_same_video() and self.not_same_video_cnt >= 5:
                print('由于视频连续相同五次而重启APP')
                self.reopen_app()
            self.uia_ins.click(ResourceID.button2, xml=self.uia_ins.xml)
            self.init_sleep_time()
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            self.random_swipe(True)
            self.adb_ins.press_back_key()
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
                # self.open_treasure_box()
                self.view_ads()
                break
            show_datetime('ksjsb.mainloop')
