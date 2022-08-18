"""快手极速版模块"""
from datetime import datetime, timedelta, date
from random import randint
from xml.parsers.expat import ExpatError

from .activity import Activity
from .resource_id import ResourceID
from ..project import Project
from ...base import sleep, show_datetime, print_err, run_forever
from ...mysql import RetrieveKsjsb, UpdateKsjsb
from ...tools import EMail, find_all_ints_with_re


# pylint: disable=too-many-public-methods
class Ksjsb(Project):
    """快手极速版类"""

    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备编号
        """
        super().__init__(serial_num)
        self.last_loop_datetime = datetime.now() - timedelta(minutes=30)
        self.view_ads_cnt = 0
        self.dbr = RetrieveKsjsb(serial_num)
        self.dbu = UpdateKsjsb(serial_num)

    def is_loading(self, retry_cnt=0):
        """判断打开快手极速版APP时是否正在加载资源

        :return: 正在加载资源返回True，否则返回False
        """
        print(f'is_loading retry_cnt={retry_cnt}')
        try:
            if self.uia_ins.get_dict(ResourceID.password_login_title):
                self.adb_ins.press_back_key()
                self.uia_ins.click(ResourceID.switch_login_way)
                EMail(self.serial_num).send_login_alarm()
                print('请手动输入密码后再继续向下执行程序')
                input()
        except (FileNotFoundError, ExpatError) as err:
            print_err(f'is_loading {err}')
            self.adb_ins.press_back_key(12)
            self.uia_ins.tap((90, 140), 12)
            return True
        if retry_cnt >= 3:
            self.adb_ins.press_back_key(9)
            return False
        return self.is_loading(retry_cnt=retry_cnt+1)

    def open_app(self):
        """打开快手极速版APP"""
        print('正在打开快手极速版APP')
        self.adb_ins.open_app(Activity.HomeActivity)
        sleep(6)
        self.uia_ins.tap((90, 140), 12)
        while self.is_loading():
            pass

    def exit_award_video_play_activity(self, retry_cnt=0):
        """退出奖励视频播放活动页面

        :param retry_cnt: 出现异常后的重试次数
        :return: 正常关闭页面返回True，否则返回False
        """
        if Activity.AwardVideoPlayActivity not in self.adb_ins.get_current_focus():
            return False
        try:
            self.uia_ins.get_current_ui_hierarchy()
            while not self.uia_ins.get_dict(
                    resource_id=ResourceID.video_countdown, text='已成功领取奖励'):
                self.uia_ins.click(resource_id=ResourceID.retry_btn, xml=self.uia_ins.xml)
                sleep(10)
        except FileNotFoundError as err:
            print_err(err)
            if retry_cnt > 2 or self.uia_ins.get_point_by_screen_text(text='成功领取奖励'):
                self.adb_ins.press_back_key(6)
            else:
                sleep(30)
                print(f'retry_cnt={retry_cnt}')
                return self.exit_award_video_play_activity(retry_cnt=retry_cnt + 1)
            if Activity.KwaiYodaWebViewActivity in self.adb_ins.get_current_focus():
                return True
        try:
            self.uia_ins.click(ResourceID.video_countdown_end_icon)
        except FileNotFoundError as err:
            print_err(err)
            self.adb_ins.press_back_key(6)
        if Activity.AwardVideoPlayActivity in self.adb_ins.get_current_focus():
            if not self.uia_ins.click(ResourceID.award_video_close_dialog_abandon_button):
                if self.uia_ins.click(text='再看一个'):
                    return self.exit_award_video_play_activity()
        return True

    def enter_wealth_interface(self, reopen=True, sleep_time=50):
        """进入财富界面

        :param reopen: 是否需要重启快手极速版APP
        :param sleep_time: 睡眠时间
        """
        if reopen:
            self.reopen_app()
        print('准备进入财富界面')
        self.uia_ins.tap((90, 140), 12)
        try:
            if not self.uia_ins.click(ResourceID.red_packet_anim) and not self.uia_ins.click(
                    ResourceID.gold_egg_anim, xml=self.uia_ins.xml):
                self.uia_ins.click(ResourceID.title, '去赚钱', xml=self.uia_ins.xml)
            if 'MI 4' in self.adb_ins.dbr.model:
                sleep(sleep_time)
                self.uia_ins.get_current_ui_hierarchy()
            else:
                sleep(sleep_time - 30)
            if self.dbr.last_sign_in_date != date.today() and self.uia_ins. \
                    click_by_screen_text('立即签到'):
                sleep(3)
                if self.uia_ins.click_by_screen_text('看广告再得'):
                    sleep(6)
                    self.exit_award_video_play_activity()
                    self.uia_ins.txt = ''
                elif self.uia_ins.click_by_screen_text(text='直播再', txt=self.uia_ins.txt):
                    sleep(96)
                    self.exit_live()
                sleep(6)
                if self.uia_ins.click_by_screen_text('邀请好友赚更多'):
                    sleep(3)
                    self.adb_ins.press_back_key(3)
                    self.dbu.update_last_sign_in_date(date.today())
                self.uia_ins.txt = ''
            elif self.uia_ins.click_by_screen_text(text='继续邀请赚'):
                sleep(6)
                self.adb_ins.press_back_key(6)
                self.uia_ins.txt = ''
            if Activity.KwaiYodaWebViewActivity in self.adb_ins.get_current_focus() and self. \
                    uia_ins.get_point_by_screen_text(text='任务中心', txt=self.uia_ins.txt):
                print('已进入财富界面')
            else:
                print('未成功进入财富界面')
                self.enter_wealth_interface()
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            self.enter_wealth_interface()

    def sign_in(self):
        """签到领金币

        :return: 正常签到或者已经签到返回True，否则返回False
        """
        if date.today() == self.dbr.last_sign_in_date:
            print('今天已经签过到了，无需重复操作')
            return True
        self.enter_wealth_interface()
        self.adb_ins.swipe(600, 1860, 600, 60)
        not_cnt = 0
        while not self.uia_ins.click_by_screen_text('签到领金币'):
            self.adb_ins.swipe(600, 1860, 600, 660)
            not_cnt += 1
            if not_cnt >= 6:
                print('检测到本次操作时滑动距离过长，取消向下继续滑动并重新从头开始执行签到领金币的操作步骤')
                return self.sign_in()
        sleep(9)
        if self.uia_ins.click_by_screen_text('看广告再得'):
            sleep(6)
            self.exit_award_video_play_activity()
            self.uia_ins.txt = ''
        elif self.uia_ins.click_by_screen_text(text='直播再', txt=self.uia_ins.txt):  # 532, 1367
            sleep(96)
            self.exit_live()
        sleep(6)
        if self.uia_ins.get_point_by_screen_text('邀请好友赚更多'):  # 532, 1367
            self.dbu.update_last_sign_in_date(date.today())
            return True
        return False

    def get_double_bonus(self):
        """点击翻倍：开启看视频奖励翻倍特权

        :return: 成功点击翻倍或者已经点击翻倍返回True，否则返回False
        """
        if date.today() == self.dbr.last_double_bonus_date:
            print('今天已经点击翻倍了，无需重复操作')
            return True
        self.enter_wealth_interface()
        print('开启看视频奖励翻倍特权')
        self.adb_ins.swipe(600, 1860, 600, 60)
        not_cnt = 0
        while not self.uia_ins.get_point_by_screen_text('开启看视频奖励翻倍特权'):
            self.adb_ins.swipe(600, 1860, 600, 660)
            not_cnt += 1
            if not_cnt >= 6:
                print('检测到本次操作时滑动距离过长，取消向下继续滑动并重新从头开始执行点击翻倍的操作步骤')
                return self.get_double_bonus()
        if self.uia_ins.click_by_screen_text(text='开启看视频奖励翻倍特权', txt=self.uia_ins.txt):
            self.dbu.update_last_double_bonus_date(date.today())
            sleep(6)
            return True
        return False

    def open_treasure_box(self):
        """开宝箱得金币

        :return: 正常开宝箱、已经开过或开完宝箱返回True
        """
        if date.today() == self.dbr.last_treasure_box_date:
            print('今天已经把宝箱开完了，无需重复操作')
            return True
        self.enter_wealth_interface()
        print('开宝箱')
        if self.uia_ins.click_by_screen_text('开宝箱得金币', txt=self.uia_ins.txt):
            sleep(3)
            self.uia_ins.tap((530, 1330), 12)
            while 'mCurrentFocus=null' in self.adb_ins.get_current_focus():
                sleep(3)
            current_focus = self.adb_ins.get_current_focus()
            if Activity.LiveSlideActivity in self.adb_ins.get_current_focus():
                sleep(80)
                self.exit_live()
            elif Activity.KwaiYodaWebViewActivity in current_focus:
                return self.open_treasure_box()
            else:
                self.exit_award_video_play_activity()
        elif self.uia_ins.get_point_by_screen_text('明日再来', txt=self.uia_ins.txt):
            print('今天已经开完宝箱了，请明日再来')
            self.dbu.update_last_treasure_box_date(date.today())
        return True

    def view_ads(self):
        """看广告视频得5000个金币

        :return: 成功获得或者已经获得返回True，否则返回False
        """
        if date.today() == self.dbr.last_view_ads_date:
            print('今天已经看完广告了，无需重复操作')
            return True
        self.enter_wealth_interface()
        print('看广告视频得5000金币')
        self.adb_ins.swipe(600, 1600, 600, 960)
        not_cnt = 0
        while not self.uia_ins.get_point_by_screen_text(text='看视频得5000金币'):
            self.adb_ins.swipe(600, 1800, 600, 800)
            not_cnt += 1
            if not_cnt >= 6:
                print('检测到本次操作时滑动距离过长，取消向下继续滑动并重新从头开始执行看广告视频得金币的操作步骤')
                return self.view_ads()
        while self.uia_ins.click_by_screen_text(text='看视频得5000金币'):
            sleep(12)
            if Activity.AwardVideoPlayActivity in self.adb_ins.get_current_focus():
                self.exit_award_video_play_activity()
                self.view_ads_cnt = 0
            elif Activity.KwaiYodaWebViewActivity in self.adb_ins.get_current_focus():
                break
        if Activity.KwaiYodaWebViewActivity in self.adb_ins.get_current_focus():
            print(f'view_ads_cnt={self.view_ads_cnt}')
            if self.view_ads_cnt > 2:
                self.view_ads_cnt = 0
                self.dbu.update_last_view_ads_date(date.today())
                return True
            else:
                self.view_ads_cnt += 1
        return False

    def exit_live(self, break_activity=Activity.KwaiYodaWebViewActivity):
        """退出直播页面

        :param break_activity : 跳出循环体的活动
        """
        print('退出直播页面')
        try:
            while True:
                self.adb_ins.press_back_key(18)
                if self.uia_ins.click_by_xml_texts(texts=['退出直播间', '退出']):
                    sleep(18)
                current_focus = self.adb_ins.get_current_focus()
                if break_activity in self.adb_ins.get_current_focus():
                    break
                if Activity.KwaiYodaWebViewActivity in current_focus:
                    break
                if Activity.HomeActivity in current_focus:
                    break
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            current_focus = self.adb_ins.get_current_focus()
            if break_activity in current_focus:
                pass
            elif Activity.KwaiYodaWebViewActivity in current_focus:
                pass
            else:
                self.exit_live(break_activity)

    def watch_live(self):
        """看直播"""
        if date.today() == self.dbr.last_watch_live_date:
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
            sleep(6)
            if Activity.AwardFeedFlowActivity in self.adb_ins.get_current_focus():
                progress = find_all_ints_with_re(self.uia_ins.get_dict(
                    ResourceID.progress_display)['@text'])
                if progress[0] == progress[1]:
                    self.dbu.update_last_watch_live_date(date.today())
                    break
                self.adb_ins.press_back_key(3)

    # pylint: disable=too-many-return-statements
    def shopping(self):
        """去逛街

        :return: 今天成功逛完街或者已经逛完街返回True，无法确定是否成功逛完则返回False
        """
        if date.today() == self.dbr.last_shopping_date:
            print('今天已经逛完街了，无需重复操作')
            return True
        self.enter_wealth_interface()
        print('去逛街')
        self.adb_ins.swipe(600, 1860, 600, 560)
        not_cnt = 0
        while not self.uia_ins.click_by_screen_text('逛街领金币'):
            self.adb_ins.swipe(600, 1860, 600, 660)
            not_cnt += 1
            if not_cnt >= 6:
                print('检测到本次操作时滑动距离过长，取消向下继续滑动并重新从头开始执行去逛街的操作步骤')
                return self.shopping()
        sleep(12)
        current_focus = self.adb_ins.get_current_focus()
        if Activity.KwaiYodaWebViewActivity in current_focus:
            self.dbu.update_last_shopping_date(date.today())
            return True
        if Activity.AdKwaiRnActivity not in self.adb_ins.get_current_focus():
            return self.shopping()
        break_while = False
        while Activity.KwaiYodaWebViewActivity not in self.adb_ins.get_current_focus():
            countdown = 699
            while countdown:
                sleep(1)
                countdown -= 1
                print(countdown)
                self.adb_ins.swipe(536, 1100, 536, 1000)
                current_focus = self.adb_ins.get_current_focus()
                if Activity.KwaiYodaWebViewActivity in current_focus:
                    break_while = True
                    break
                if Activity.HomeActivity in current_focus:
                    return False
                if Activity.AdKwaiRnActivity not in current_focus:
                    self.adb_ins.press_back_key(9)
            self.adb_ins.press_back_key(60)
            if Activity.KwaiYodaWebViewActivity not in self.adb_ins.get_current_focus():
                self.adb_ins.press_back_key(60)
        if break_while:
            return False
        self.dbu.update_last_shopping_date(date.today())
        return True

    # pylint: disable=too-many-return-statements
    def open_meal_allowance(self):
        """领饭补

        :return: 成功领取或者已经领取返回True，否则返回False
        """
        hour = datetime.now().hour
        if hour in [0, 1, 2, 3, 4, 9, 10, 14, 15, 16, 20]:
            print('还没到饭点的，请到饭点的时候再来领饭补')
            return True
        breakfast_hours = [5, 6, 7, 8]
        lunch_hours = [11, 12, 13]
        dinner_hours = [17, 18, 19]
        supper_hours = [21, 22, 23]
        if not self.dbr.last_meal_allowance_datetime or date.today() > date.fromisoformat(str(
                self.dbr.last_meal_allowance_datetime)[:10]):
            self.dbu.update_last_meal_allowance_datetime(datetime.now() - timedelta(
                hours=datetime.now().hour))
        if hour in breakfast_hours and self.dbr.last_meal_allowance_datetime. \
                hour in breakfast_hours:
            print('已经领过早饭饭补了，无需重复操作')
            return True
        if hour in lunch_hours and self.dbr.last_meal_allowance_datetime.hour in lunch_hours:
            print('已经领过午饭饭补了，无需重复操作')
            return True
        if hour in dinner_hours and self.dbr.last_meal_allowance_datetime.hour in dinner_hours:
            print('已经领过晚饭饭补了，无需重复操作')
            return True
        if hour in supper_hours and self.dbr.last_meal_allowance_datetime.hour in supper_hours:
            print('已经领过夜宵饭补了，无需重复操作')
            return True
        self.enter_wealth_interface()
        print('领饭补')
        self.adb_ins.swipe(600, 1800, 600, 600)
        not_cnt = 0
        while not self.uia_ins.click_by_screen_text('到饭点领饭补'):
            self.adb_ins.swipe(600, 1860, 600, 660)
            not_cnt += 1
            if not_cnt >= 6:
                print('检测到本次操作时滑动距离过长，取消向下继续滑动并重新从头开始执行领饭补的操作步骤')
                return self.open_meal_allowance()
        sleep(30)
        if self.uia_ins.click_by_screen_text(text='领取饭补'):
            sleep(6)
            self.uia_ins.tap((530, 1220), 12)
            self.exit_award_video_play_activity()
            sleep(6)
        if not self.uia_ins.get_point_by_screen_text('点击立得'):
            self.dbu.update_last_meal_allowance_datetime(datetime.now())
            return True
        return False

    def get_flash_benefits(self):
        """"领取限时福利：限时福利14天领"""
        if date.today() == self.dbr.last_flash_benefits_date:
            print('今天已经领完限时福利了，无需重复操作')
            return
        self.enter_wealth_interface()
        print('领取限时福利')
        if not self.uia_ins.get_point_by_screen_text(text='限时福利14天领', txt=self.uia_ins.txt):
            self.dbu.update_last_flash_benefits_date(date.today())
            return
        if self.uia_ins.click_by_screen_text(text='立即领取', txt=self.uia_ins.txt):
            sleep(12)
            self.dbu.update_last_flash_benefits_date(date.today())

    def get_desktop_component_coin(self):
        """获取桌面组件奖励"""
        if date.today() == self.dbr.last_desktop_component_date:
            print('今天已经领完桌面组件奖励了，无需重复操作')
            return
        self.reopen_app()
        print('获取桌面组件奖励')
        self.adb_ins.press_home_key(3)
        try:
            enter_while = False
            while self.uia_ins.click(ResourceID.tv_get_coin_left):
                sleep(3)
                enter_while = True
            if enter_while:
                print('成功检测到并领取桌面组件奖励')
                sleep(16)
                self.dbu.update_last_desktop_component_date(date.today())
            else:
                print('没有找到桌面组件奖励')
        except FileNotFoundError as err:
            print_err(err)
            return

    def buy_things_with_coins(self):
        """获取金币购划算页面内的所有奖励

        :return: 成功获取或者已经获取返回True，否则返回False
        """
        if date.today() == self.dbr.last_buy_things_date:
            print('今天已经领完金币购划算页面内的所有奖励了，无需重复操作')
            return True
        self.enter_wealth_interface()
        print('金币购划算')
        self.uia_ins.click_by_screen_text('金币购划算')
        sleep(20)
        self.uia_ins.tap((991, 378), 6)
        if self.uia_ins.click_by_screen_text(text='去签到'):  # 明日再来
            sleep(3)
        while self.uia_ins.click_by_screen_text(text='领福利'):  # 已完成
            sleep(6)
            if Activity.AwardFeedFlowActivity in self.adb_ins.get_current_focus():
                self.uia_ins.tap((240, 848), 96)
                self.exit_live(Activity.AwardFeedFlowActivity)
                self.adb_ins.press_back_key(9)
        if self.uia_ins.click_by_screen_text('去逛街'):  # 已领取
            countdown = 699
            while countdown:
                sleep(1)
                countdown -= 1
                print(countdown)
                self.adb_ins.swipe(536, 1100, 536, 1000)
                current_focus = self.adb_ins.get_current_focus()
                if Activity.KwaiYodaWebViewActivity in current_focus:
                    break
                if Activity.HomeActivity in current_focus:
                    return False
                if Activity.AdKwaiRnActivity not in current_focus:
                    self.adb_ins.press_back_key(9)
            self.adb_ins.press_back_key(30)
        if self.uia_ins.get_point_by_screen_text('明日再来') and self.uia_ins.\
                get_point_by_screen_text(text='已完成', txt=self.uia_ins.txt) and self.uia_ins.\
                get_point_by_screen_text(text='已领取', txt=self.uia_ins.txt):
            self.dbu.update_last_buy_things_date(date.today())
            return True
        return False

    def change_money(self):
        """把金币兑换钱

        :return: 兑换成功返回True，否则返回False
        """
        if date.today() == self.dbr.last_change_money_date:
            print('今天已经把金币兑换成钱过了，无需重复操作')
            return True
        self.enter_wealth_interface()
        print('正在把金币兑换钱')
        self.uia_ins.tap((866, 349), 12)
        self.uia_ins.get_current_ui_hierarchy()
        webview_dic = self.uia_ins.get_dict(class_=ResourceID.WebView)
        cash = float(webview_dic['node'][0]['node'][1]['@text'])
        dics = webview_dic['node'][1]['node']
        for dic in dics[4:0:-1]:
            dic = dic['node']
            if isinstance(dic, list):
                dic = dic[0]
            money = float(dic['@text'][:-1])
            if cash >= money:
                print(money)
                self.uia_ins.click_by_bounds(dic['@bounds'])
                break
        self.uia_ins.click(text='立即兑换', xml=self.uia_ins.xml)
        self.uia_ins.tap((536, 1706), 26)
        self.uia_ins.click(text='立即提现')
        sleep(6)
        try:
            if self.uia_ins.get_dict(text='去验证'):
                EMail(self.serial_num).send_need_verification_alarm()
                input('提现时需要验证才能继续，请手动处理')
                return False
            if self.uia_ins.get_dict(resource_id=ResourceID.pay_title_tv, text="提现结果"):
                self.dbu.update_last_change_money_date(date.today())
                return True
            return False
        except FileNotFoundError as err:
            print_err(err)
            return self.change_money()

    def get_daily_challenge_coins(self):
        """领取每日挑战奖励"""
        if date.today() == self.dbr.last_daily_challenge_date:
            print('今天已经领过每日挑战奖励了，无需重复操作')
            return True
        self.enter_wealth_interface()
        print('领取每日挑战奖励')
        self.adb_ins.swipe(600, 1800, 600, 390)
        while self.uia_ins.click_by_screen_text(text='点击领取', start_index=1):
            sleep(6)
        self.dbu.update_last_daily_challenge_date(date.today())

    def get_wealth(self):
        """获取财富值"""
        print('正在获取财富值')
        self.uia_ins.click_by_screen_text('抵用金明细')
        dics = self.uia_ins.get_dict(index='0', text='我的收益')['node']
        gold_coins = dics[2]['@text']
        if 'w' in gold_coins:
            gold_coins = 10000 * float(gold_coins[:-3])
        else:
            gold_coins = float(gold_coins[:-2])
        cash_coupons = float(dics[6]['@text'][:-1])
        return gold_coins, cash_coupons

    def update_wealth(self):
        """更新财富值"""
        if date.today() == self.dbr.last_update_wealth_date:
            print('今天已经更新过财富值了，无需重复操作')
            return True
        self.enter_wealth_interface()
        print('更新财富值')
        self.uia_ins.tap((186, 360), 9)
        self.uia_ins.get_current_ui_hierarchy()
        gold_coins, cash_coupons = self.get_wealth()
        if gold_coins != self.dbr.gold_coins:
            self.dbu.update_gold_coins(gold_coins)
        if cash_coupons != self.dbr.cash_coupons:
            self.dbu.update_cash_coupons(cash_coupons)
        self.dbu.update_last_update_wealth_date(date.today())
        return True

    def random_swipe(self, x_range=(360, 390), y_list=(1160, 1190, 260, 290)):
        """随机滑动一段长度

        :param x_range : x_min（A、C点的X轴坐标）与x_max（B、D点的X轴坐标）
        :param y_list: [A点的Y轴坐标，B点的Y轴坐标，C点的Y轴坐标，D点的Y轴坐标]
        """
        super().random_swipe(x_range, y_list)

    def watch_video(self):
        """看视频赚金币

        :return: 今天已经看视频赚完金币了返回True，否则返回False
        """
        if date.today() <= self.dbr.last_watch_video_date:
            print('今天已经看视频赚完金币了，无需重复操作')
            return False
        print(f'距离下一轮任务轮询还剩'
              f'{self.last_loop_datetime - datetime.now() + timedelta(minutes=20)}')
        self.random_swipe()
        print(f'当前活动为：{self.adb_ins.get_current_focus()}')
        print(f'当前的CPU温度为：{self.adb_ins.get_cpu_temperature()}摄氏度')
        sleep(randint(15, 18))
        self.adb_ins.press_back_key()
        return True

    def is_done_watching_video(self, retest_cnt=0, reopen_flag=True):
        """判断今天是否看完了视频，即看视频是否还有奖励

        :param retest_cnt : 重新检测是看完的次数
        :param reopen_flag : 是否需要重新打开
        :return: 多次检测结果均是看完了视频才返回True，否则返回False
        """
        if reopen_flag:
            self.reopen_app()
            self.uia_ins.tap((90, 140), 9)
        while not self.uia_ins.secure_get_current_ui_hierarchy():
            sleep(10)
        try:
            if self.uia_ins.get_dict(ResourceID.red_packet_anim) and not self.uia_ins.get_dict(
                    ResourceID.cycle_progress, xml=self.uia_ins.xml):
                print(f'retest_cnt={retest_cnt}')
                if retest_cnt > 2:
                    return True
                return self.is_done_watching_video(retest_cnt=retest_cnt+1)
        except FileNotFoundError as err:
            print_err(f'is_done_watching_video {err}')
            sleep(10)
            return self.is_done_watching_video(retest_cnt=retest_cnt, reopen_flag=False)
        return False

    @run_forever
    def mainloop(self):
        """主循环"""
        if datetime.now() - self.last_loop_datetime > timedelta(minutes=20):
            self.adb_ins.reboot_per_day()
            self.get_double_bonus()
            self.sign_in()
            self.open_treasure_box()
            self.view_ads()
            self.watch_live()
            self.shopping()
            self.open_meal_allowance()
            self.get_flash_benefits()
            self.get_desktop_component_coin()
            self.buy_things_with_coins()
            if datetime.now().hour > 5:
                self.change_money()
                self.get_daily_challenge_coins()
                self.update_wealth()
                if not self.dbr.last_watch_video_date:
                    self.dbu.update_last_watch_video_date(date.min)
                if date.today() > self.dbr.last_watch_video_date:
                    if self.is_done_watching_video():
                        self.dbu.update_last_watch_video_date(date.today())
                    else:
                        self.adb_ins.press_back_key()
            self.last_loop_datetime = datetime.now()
        if not self.watch_video():
            self.free_memory()
            sleep(1200)
        show_datetime('看视频')
