"""快手极速版模块"""
from datetime import datetime, timedelta
from random import randint
from xml.parsers.expat import ExpatError

from .activity import Activity
from .resource_id import ResourceID
from ..project import Project
from ...base import sleep, show_datetime, print_err, run_forever
from ...mysql import RetrieveKsjsb, UpdateKsjsb
from ...network import EMail


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

    def open_app(self):
        """打开快手极速版APP"""
        print('正在打开快手极速版APP')
        self.adb_ins.open_app(Activity.HomeActivity)
        sleep(120)

    def exit_award_video_play_activity(self):
        """退出奖励视频播放活动页面

        :return: 正常关闭页面返回True，否则返回False
        """
        if Activity.AwardVideoPlayActivity not in self.adb_ins.get_current_focus():
            return False
        try:
            while not self.uia_ins.get_dict(
                    resource_id=ResourceID.video_countdown, text='已成功领取奖励'):
                sleep(10)
        except FileNotFoundError as err:
            print_err(err)
            return self.exit_award_video_play_activity()
        self.uia_ins.click(ResourceID.video_countdown_end_icon)
        if Activity.AwardVideoPlayActivity in self.adb_ins.get_current_focus():
            if not self.uia_ins.click(ResourceID.award_video_close_dialog_abandon_button):
                if self.uia_ins.click(text='再看一个'):
                    return self.exit_award_video_play_activity()
        return True

    def enter_wealth_interface(self, reopen=True, sleep_time=50):
        """进入财富界面

        param reopen: 是否需要重启快手极速版APP
        param sleep_time: 睡眠时间
        """
        if reopen:
            self.reopen_app()
        print('准备进入财富界面')
        self.uia_ins.tap((90, 140), 15)
        try:
            if not self.uia_ins.click(ResourceID.red_packet_anim):
                self.uia_ins.click(ResourceID.gold_egg_anim, xml=self.uia_ins.xml)
            sleep(sleep_time)
            self.uia_ins.get_current_ui_hierarchy()
            day = datetime.now().day
            if not self.dbr.last_sign_in_day == day and self.uia_ins.\
                    click_by_screen_text('立即签到'):
                sleep(3)
                if self.uia_ins.click_by_screen_text('看广告再得'):
                    sleep(6)
                    self.exit_award_video_play_activity()
                    self.uia_ins.txt = ''
                elif self.uia_ins.click_by_screen_text(text='看直播再得', txt=self.uia_ins.txt):
                    sleep(96)
                    self.exit_live()
                    self.uia_ins.txt = ''
                sleep(6)
                self.dbu.update_last_sign_in_day(day)
                if self.uia_ins.click_by_screen_text('邀请好友赚更多'):
                    sleep(3)
                    self.adb_ins.press_back_key(3)
            if Activity.KwaiYodaWebViewActivity in self.adb_ins.get_current_focus() and self.\
                    uia_ins.get_point_by_screen_text('任务中心'):
                print('已进入财富界面')
            else:
                self.enter_wealth_interface()
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            self.enter_wealth_interface()

    def do_daily_task(self):
        """执行每日任务"""
        print('执行每日任务')
        self.get_double_bonus()
        self.change_money()
        # self.open_exclusive_gold_coin_gift_pack()
        self.get_flash_benefits()
        self.view_ads()
        self.shopping()
        self.watch_live()
        self.open_meal_allowance()
        self.open_treasure_box()
        self.update_wealth()

    def get_desktop_component_coin(self):
        """获取桌面组件奖励"""
        self.reopen_app()
        self.adb_ins.press_home_key(3)
        while self.uia_ins.click(ResourceID.tv_get_coin_left):
            sleep(3)
        sleep(16)

    def get_double_bonus(self):
        """点击翻倍：开启看视频奖励翻倍特权"""
        if self.start_day == self.dbr.last_double_bonus_day:
            print('今天已经点击翻倍了，无需重复操作')
            return
        self.enter_wealth_interface()
        print('开启看视频奖励翻倍特权')
        self.adb_ins.swipe(600, 1800, 600, 350)
        if self.uia_ins.click_by_screen_text('开启看视频奖励翻倍特权'):
            self.dbu.update_last_double_bonus_day(self.start_day)
            sleep(6)

    def open_treasure_box(self):
        """开宝箱得金币"""
        if self.start_day == self.dbr.last_treasure_box_day:
            print('今天已经开完宝箱了，无需重复操作')
            return
        self.enter_wealth_interface()
        print('开宝箱')
        if self.uia_ins.click_by_screen_text('开宝箱得金币', txt=self.uia_ins.txt):
            self.uia_ins.tap((530, 1330), 6)
            if Activity.LiveSlideActivity in self.adb_ins.get_current_focus():
                sleep(80)
                self.exit_live()
            else:
                self.exit_award_video_play_activity()
        elif self.uia_ins.get_point_by_screen_text('明日再来', txt=self.uia_ins.txt):
            print('今天已经开完宝箱了，请明日再来')
            self.dbu.update_last_treasure_box_day(self.start_day)

    def view_ads(self):
        """看广告视频得5000个金币"""
        if self.start_day == self.dbr.last_view_ads_day:
            print('今天已经看完广告了，无需重复操作')
            return
        self.enter_wealth_interface()
        print('看广告视频得5000金币')
        self.adb_ins.swipe(600, 1600, 600, 960)
        while not self.uia_ins.get_point_by_screen_text(text='领福利'):
            self.adb_ins.swipe(600, 1800, 600, 800)
        while self.uia_ins.click_by_screen_text(text='领福利'):
            sleep(6)
            if Activity.AwardVideoPlayActivity in self.adb_ins.get_current_focus():
                self.exit_award_video_play_activity()
            elif Activity.AwardFeedFlowActivity in self.adb_ins.get_current_focus():
                self.adb_ins.press_back_key(6)
                break
        if self.uia_ins.get_point_by_screen_text('5/5'):
            self.dbu.update_last_view_ads_day(self.start_day)
        elif self.uia_ins.get_point_by_screen_text('明天再来', txt=self.uia_ins.txt):
            self.dbu.update_last_view_ads_day(self.start_day)

    def exit_live(self, break_activity=Activity.KwaiYodaWebViewActivity):
        """退出直播页面

        :param break_activity : 跳出循环体的活动
        """
        print('退出直播页面')
        try:
            while True:
                self.adb_ins.press_back_key(9)
                if self.uia_ins.click_by_xml_texts(texts=['退出直播间', '退出']):
                    sleep(9)
                if break_activity in self.adb_ins.get_current_focus():
                    break
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            if break_activity not in self.adb_ins.get_current_focus():
                self.exit_live(break_activity)

    def watch_live(self):
        """看直播"""
        if self.start_day == self.dbr.last_watch_live_day:
            print('今天已经把直播看完了，无需重复操作')
            return
        self.enter_wealth_interface()
        print('看直播')
        while not self.uia_ins.get_point_by_screen_text(text='看直播得1.5万金币'):
            self.adb_ins.swipe(600, 1800, 600, 800)
        while self.uia_ins.click_by_screen_text(text='看直播得1.5万金币'):
            sleep(6)
            self.uia_ins.tap((240, 848), 96)
            self.exit_live(Activity.AwardFeedFlowActivity)
            if self.uia_ins.get_dict(ResourceID.progress_display)['@text'] == '10/10':
                self.dbu.update_last_watch_live_day(self.start_day)
                break
            self.adb_ins.press_back_key(3)

    def shopping(self):
        """去逛街"""
        if self.start_day == self.dbr.last_shopping_day:
            print('今天已经逛完街了，无需重复操作')
            return True
        self.enter_wealth_interface()
        print('去逛街')
        self.adb_ins.swipe(600, 1860, 600, 560)
        while not self.uia_ins.click_by_screen_text('去逛街'):
            self.adb_ins.swipe(600, 1860, 600, 660)
        sleep(6)
        if Activity.AdKwaiRnActivity not in self.adb_ins.get_current_focus():
            return self.shopping()
        while Activity.KwaiYodaWebViewActivity not in self.adb_ins.get_current_focus():
            countdown = 480
            while countdown:
                sleep(1)
                countdown -= 1
                print(countdown)
                self.adb_ins.swipe(536, 1100, 536, 1000)
                if Activity.AdKwaiRnActivity not in self.adb_ins.get_current_focus():
                    self.adb_ins.press_back_key()
            self.adb_ins.press_back_key(30)
            if Activity.KwaiYodaWebViewActivity not in self.adb_ins.get_current_focus():
                self.adb_ins.press_back_key(9)
        self.dbu.update_last_shopping_day(self.start_day)
        return True

    def open_meal_allowance(self):
        """领饭补"""
        hour = datetime.now().hour
        if hour in [0, 1, 2, 3, 4, 9, 10, 14, 15, 16, 20]:
            print('还没到饭点的，请到饭点的时候再来领饭补')
            return
        breakfast_hours = [5, 6, 7, 8]
        lunch_hours = [11, 12, 13]
        dinner_hours = [17, 18, 19]
        supper_hours = [21, 22, 23]
        if hour in breakfast_hours and self.dbr.last_meal_allowance_hour in breakfast_hours:
            print('已经领过早饭饭补了，无需重复操作')
            return
        if hour in lunch_hours and self.dbr.last_meal_allowance_hour in lunch_hours:
            print('已经领过午饭饭补了，无需重复操作')
            return
        if hour in dinner_hours and self.dbr.last_meal_allowance_hour in dinner_hours:
            print('已经领过晚饭饭补了，无需重复操作')
            return
        if hour in supper_hours and self.dbr.last_meal_allowance_hour in supper_hours:
            print('已经领过夜宵饭补了，无需重复操作')
            return
        self.enter_wealth_interface()
        print('领饭补')
        self.adb_ins.swipe(600, 1800, 600, 600)
        while not self.uia_ins.click_by_screen_text('到饭点领饭补'):
            self.adb_ins.swipe(600, 1860, 600, 660)
        sleep(6)
        try:
            if self.uia_ins.click(text='领取饭补'):
                sleep(3)
                self.uia_ins.tap((530, 1220), 6)
                self.exit_award_video_play_activity()
            self.dbu.update_last_meal_allowance_hour(hour)
        except FileNotFoundError as err:
            print_err(err)
            self.open_meal_allowance()

    def open_exclusive_gold_coin_gift_pack(self):
        """领取专属金币礼包"""
        if self.start_day == self.dbr.last_exclusive_gift_day:
            print('今天已经领完专属金币礼包了，无需重复操作')
            return
        self.enter_wealth_interface()
        print('领取专属金币礼包')
        self.adb_ins.swipe(600, 1830, 600, 1750)
        if self.uia_ins.click_by_screen_text('领金币'):
            self.uia_ins.tap((530, 1200), 6)
            self.exit_award_video_play_activity()
        self.dbu.update_last_exclusive_gift_day(self.start_day)

    def get_flash_benefits(self):
        """"领取限时福利：限时福利14天领14元"""
        if self.start_day == self.dbr.last_flash_benefits_day:
            print('今天已经领完限时福利了，无需重复操作')
            return
        self.enter_wealth_interface()
        if self.uia_ins.get_point_by_screen_text(text='点击领取今日红包', txt=self.uia_ins.txt):
            self.uia_ins.click_by_screen_text(text='立即领取', txt=self.uia_ins.txt)
        self.dbu.update_last_flash_benefits_day(self.start_day)

    def update_wealth(self):
        """更新财富值

        """
        if self.start_day == self.dbr.last_update_wealth_day:
            print('今天已经更新过财富值了，无需重复操作')
            return True
        self.enter_wealth_interface()
        print('更新财富值')
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
            return self.update_wealth()
        self.dbu.update_last_update_wealth_day(self.start_day)
        return True

    def get_wealth(self):
        """获取财富值"""
        print('正在获取财富值')
        dics = self.uia_ins.get_dict(index='0', text='我的收益')['node']
        # print(dics)
        # for i, v in enumerate(dics):
        #     print(i, v)
        gold_coins = dics[2]['@text']
        if 'w' in gold_coins:
            gold_coins = 10000 * float(gold_coins[:-3])
        else:
            gold_coins = float(gold_coins[:-2])
        cash_coupons = float(dics[6]['@text'][:-1])
        # print(f"gold_coins={gold_coins}, cash_coupons={cash_coupons}")
        return gold_coins, cash_coupons

    def change_money(self):
        """把金币兑换钱

        :return: 兑换成功返回True，否则返回False
        """
        if self.start_day == self.dbr.last_change_money_day:
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
        self.uia_ins.tap((536, 1706), 26)
        self.uia_ins.click(text='立即提现')
        sleep(3)
        if self.uia_ins.get_dict(text='去验证'):
            EMail(self.serial_num).send_need_verification_alarm()
            return False
        if self.uia_ins.get_dict(resource_id=ResourceID.pay_title_tv, text="提现结果"):
            self.dbu.update_last_change_money_day(self.start_day)
            return True
        return False

    def watch_video(self):
        """看视频"""
        if self.reopen_app_per_hour(False):
            self.adb_ins.keep_online()
            self.do_daily_task()
            self.reopen_app()
            self.uia_ins.tap((90, 140), 9)
            if datetime.now().hour > 5 and self.uia_ins.get_dict(ResourceID.red_packet_anim):
                if not self.uia_ins.get_dict(ResourceID.cycle_progress, xml=self.uia_ins.xml):
                    self.free_memory()
                    self.adb_ins.press_power_key()
                    self.start_day = (datetime.now() + timedelta(days=1)).day
                    return
            self.adb_ins.press_back_key()
        show_datetime('看视频')
        self.random_swipe()
        sleep(randint(15, 18))
        self.adb_ins.press_back_key()

    def random_swipe(self, x_range=(360, 390), y_list=(1160, 1190, 260, 290)):
        """随机滑动一段长度

        :param x_range : x_min（A、C点的X轴坐标）与x_max（B、D点的X轴坐标）
        :param y_list: [A点的Y轴坐标，B点的Y轴坐标，C点的Y轴坐标，D点的Y轴坐标]
        """
        super().random_swipe(x_range, y_list)

    @run_forever
    def mainloop(self):
        """主循环"""
        if datetime.now().day >= self.start_day:
            self.watch_video()
        else:
            sleep(3600)
