"""快手极速版模块"""
from datetime import datetime, timedelta
from time import time
from xml.parsers.expat import ExpatError

from .activity import Activity
from .resource_id import ResourceID
from ..project import Project
from ...base import sleep, show_datetime, print_err
from ...mysql import RetrieveKsjsb, UpdateKsjsb


# pylint: disable=too-many-instance-attributes, too-many-public-methods
class Ksjsb(Project):
    """快手极速版类"""

    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备编号
        """
        super().__init__(serial_num)
        self.start_day = datetime.now().day
        self.dbr = RetrieveKsjsb(serial_num)
        self.dbu = UpdateKsjsb(serial_num)
        self.last_video_username = ''
        self.last_video_description = ''
        self.last_video_music = ''
        self.not_same_video_cnt = 0
        self.no_treasure_box_flag = False

    def shopping(self):
        """逛街"""
        self.enter_wealth_interface()
        print('逛街')
        try:
            self.uia_ins.click(text='浏览低价商品领金币')
        except FileNotFoundError as err:
            print_err(err)
            self.shopping()

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

    def open_app(self):
        """打开快手极速版APP"""
        print('正在打开快手极速版APP')
        self.adb_ins.open_app(Activity.HomeActivity)
        sleep(19)
        try:
            if self.uia_ins.click(ResourceID.close):
                self.uia_ins.xml = ''
            if self.uia_ins.click(ResourceID.iv_close_common_dialog, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
            if self.uia_ins.click(ResourceID.positive, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
            if self.uia_ins.click(ResourceID.click_double, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
            if self.uia_ins.click(ResourceID.tv_upgrade_now, xml=self.uia_ins.xml):
                self.uia_ins.xml = ''
                self.adb_ins.press_back_key()
            while not self.uia_ins.get_dict(ResourceID.red_packet_anim, xml=self.uia_ins.xml):
                if self.uia_ins.get_dict(ResourceID.gold_egg_anim, xml=self.uia_ins.xml):
                    break
                if Activity.HomeActivity not in self.adb_ins.get_current_focus():
                    self.reopen_app()
                    return
                if self.uia_ins.get_dict(ResourceID.item_title, xml=self.uia_ins.xml):
                    self.uia_ins.xml = ''
                    self.adb_ins.press_back_key()
                self.random_swipe(True)
                self.uia_ins.xml = ''
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            self.adb_ins.press_back_key()

    def exit_award_video_play_activity(self):
        """退出奖励视频播放活动页面

        :return: 正常关闭页面返回True，否则返回False
        """
        if Activity.AwardVideoPlayActivity not in self.adb_ins.get_current_focus():
            return False
        while not self.uia_ins.get_dict(resource_id=ResourceID.video_countdown, text='已成功领取奖励'):
            sleep(10)
        self.uia_ins.click(ResourceID.video_countdown_end_icon)
        try:
            self.uia_ins.click(ResourceID.award_video_close_dialog_abandon_button)
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
        return True

    def enter_wealth_interface(self, reopen=True, sleep_time=39):
        """进入财富界面

        param reopen: 是否需要重启快手极速版APP
        param sleep_time: 睡眠时间
        """
        if reopen:
            self.reopen_app()
        print('准备进入财富界面')
        try:
            if not self.uia_ins.click(ResourceID.red_packet_anim):
                self.uia_ins.click(ResourceID.gold_egg_anim, xml=self.uia_ins.xml)
            sleep(sleep_time)
            self.uia_ins.get_current_ui_hierarchy()
            day = datetime.now().day
            if not self.dbr.last_sign_in_day == day and self.uia_ins.\
                    click_by_screen_text('立即签到'):
                sleep(3)
                self.uia_ins.click_by_screen_text('看广告再得300金币')
                sleep(3)
                self.exit_award_video_play_activity()
                self.uia_ins.txt = ''
                self.dbu.update_last_sign_in_day(day)
                self.adb_ins.press_back_key()
            if Activity.KwaiYodaWebViewActivity in self.adb_ins.get_current_focus() and self.\
                    uia_ins.get_point_by_screen_text('任务中心', txt=self.uia_ins.txt):
                print('已进入财富界面')
            else:
                self.enter_wealth_interface()
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            if Activity.HomeActivity in self.adb_ins.get_current_focus():
                self.random_swipe()
                self.enter_wealth_interface(False)
            else:
                self.enter_wealth_interface()

    def open_treasure_box(self):
        """开宝箱得金币"""
        # 60*5, 60*9, 1200
        self.enter_wealth_interface()
        print('开宝箱')
        if self.no_treasure_box_flag:
            print('明天再来')
        elif self.uia_ins.get_point_by_screen_text('明天再来', txt=self.uia_ins.txt):
            self.no_treasure_box_flag = True
            print('明天再来')
        elif self.uia_ins.click_by_screen_text('开宝箱得金币', txt=self.uia_ins.txt):
            self.uia_ins.tap((530, 1330), 6)
            self.exit_award_video_play_activity()

    def view_ads(self):
        """看广告"""
        self.enter_wealth_interface()
        print('看广告')
        self.adb_ins.swipe(600, 1800, 600, 630)
        while self.uia_ins.click_by_screen_text(text='福利'):
            sleep(6)
            self.exit_award_video_play_activity()

    def exit_live(self):
        """退出直播页面"""
        print('退出直播页面')
        try:
            while Activity.PhotoDetailActivity in self.adb_ins.get_current_focus():
                self.adb_ins.press_back_key()
                sleep(3)
                if self.uia_ins.click(text='退出直播间'):
                    sleep(3)
            if Activity.AwardFeedFlowActivity in self.adb_ins.get_current_focus():
                self.adb_ins.press_back_key()
                sleep(3)
                return True
            return False
        except FileNotFoundError as err:
            print_err(err)
            return self.exit_live()

    def watch_live(self):
        """看直播"""
        self.enter_wealth_interface()
        print('看直播')
        self.adb_ins.swipe(600, 1800, 600, 230)
        while self.uia_ins.click_by_screen_text(text='领福利'):
            sleep(6)
            self.uia_ins.tap((240, 848))
            sleep(76)
            self.exit_live()

    def open_meal_allowance(self):
        """领饭补"""
        self.enter_wealth_interface()
        print('领饭补')
        self.adb_ins.swipe(600, 1800, 600, 800)
        self.uia_ins.click_by_screen_text('去领取')
        sleep(5)
        if self.uia_ins.click(text='领取饭补'):
            self.uia_ins.tap((530, 1220), 6)
            self.exit_award_video_play_activity()

    def open_exclusive_gold_coin_gift_pack(self):
        """领取专属金币礼包"""
        self.enter_wealth_interface()
        print('领取专属金币礼包')
        if not self.uia_ins.get_point_by_screen_text('专属金币礼包', txt=self.uia_ins.txt):
            print('该账号没有领取专属金币礼包的任务')
            return
        self.adb_ins.swipe(600, 1830, 600, 1750)
        if self.uia_ins.click_by_screen_text('领金币'):
            self.uia_ins.tap((530, 1200), 6)
            self.exit_award_video_play_activity()

    def update_wealth(self, reopen=True):
        """更新财富值

        param reopen: 是否需要重启快手极速版APP
        """
        print('更新财富值')
        self.enter_wealth_interface(reopen)
        self.uia_ins.tap((668, 360))
        sleep(9)
        try:
            gold_coins, cash_coupons = self.get_wealth()
            if gold_coins != self.dbr.gold_coins:
                self.dbu.update_gold_coins(gold_coins)
            if cash_coupons != self.dbr.cash_coupons:
                self.dbu.update_cash_coupons(cash_coupons)
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
        """把金币兑换钱

        :return: 兑换成功返回True，否则返回False
        """
        day = datetime.now().day
        if day == self.dbr.last_change_money_day:
            print('今天已经把金币兑换成钱过了，无需重复操作')
            return True
        self.enter_wealth_interface()
        print('正在把金币兑换钱')
        self.uia_ins.tap((866, 349), 6)
        self.uia_ins.get_current_ui_hierarchy()
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
        self.uia_ins.tap((536, 1706), 16)
        self.uia_ins.click(text='立即提现')
        if self.uia_ins.get_dict(ResourceID.pay_title_tv):
            self.dbu.update_last_change_money_day(day)
            return True
        return False

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
        is_same_video_flag = last_video_username == self.\
            last_video_username and last_video_description == self.\
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
            self.open_treasure_box()
            self.reopen_app()
        try:
            if datetime.now().hour > 5 and self.uia_ins.get_dict(ResourceID.red_packet_anim):
                if not self.uia_ins.get_dict(ResourceID.cycle_progress, xml=self.uia_ins.xml):
                    self.view_ads()
                    self.watch_live()
                    self.open_treasure_box()
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
                self.uia_ins.xml = ''
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

    # pylint: disable=too-many-arguments
    def random_swipe(
            self, init_rest_time=False, a_x=0, b_x=0, c_x=0, d_x=0, a_y=0, b_y=0, c_y=0, d_y=0):
        """随机滑动一段长度

        :param init_rest_time: 是否初始化剩余时间
        :param a_x: A点的X轴坐标
        :param b_x: B点的X轴坐标
        :param c_x: C点的X轴坐标
        :param d_x: D点的X轴坐标
        :param a_y: A点的Y轴坐标
        :param b_y: B点的Y轴坐标
        :param c_y: C点的Y轴坐标
        :param d_y: D点的Y轴坐标
        """
        super().random_swipe(360, 390, 360, 390, 1160, 1190, 260, 290, init_rest_time)

    def mainloop(self):
        """主循环"""
        while True:
            if datetime.now().day == self.start_day:
                self.watch_video()
            else:
                self.no_treasure_box_flag = False
                self.open_treasure_box()
                self.view_ads()
                break
            show_datetime('ksjsb.mainloop')
