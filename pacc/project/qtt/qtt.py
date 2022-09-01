"""趣头条中央控制系统模块"""
from datetime import datetime, timedelta
from random import randint
from xml.parsers.expat import ExpatError

from .activity import Activity
from .resource_id import ResourceID
from ..project import Project
from ...base import run_forever, sleep, print_err, show_datetime


class Qtt(Project):
    """趣头条中央控制系统类"""

    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备编号
        """
        super().__init__(serial_num)
        self.last_loop_datetime = datetime.now()

    def open_app(self):
        """打开趣头条APP"""
        print('正在打开快手极速版APP')
        self.adb_ins.open_app(Activity.MainActivity)
        sleep(16)
        try:
            if not self.uia_ins.click(ResourceID.ap7):
                self.uia_ins.click(ResourceID.aps, xml=self.uia_ins.xml)
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
        if self.uia_ins.click_by_screen_text('领取'):
            if Activity.InciteADActivity in self.adb_ins.get_current_focus():
                self.adb_ins.press_back_key(6)
            elif self.uia_ins.get_point_by_screen_text('我的金币'):
                self.uia_ins.tap((115, 1860), 6)
            else:
                sleep(6)
                click_cnt = 0
                while self.uia_ins.click_by_screen_text('再领'):
                    click_cnt += 1
                    sleep(6)
                    if Activity.InciteADActivity in self.adb_ins.get_current_focus():
                        self.adb_ins.press_back_key(9)
                        if self.uia_ins.secure_get_current_ui_hierarchy() and self.uia_ins.click(
                                text='有任务奖励未领取，是否继续？'):
                            self.adb_ins.press_back_key()
                        else:
                            self.uia_ins.click(text='继续观看', xml=self.uia_ins.xml)
                    self.exit_ad_activity()
                    if click_cnt >= 5:
                        break

    def random_swipe(self, x_range=(360, 390), y_list=(1160, 1190, 260, 290), duration=500):
        """随机滑动一段长度

        :param x_range : x_min（A、C点的X轴坐标）与x_max（B、D点的X轴坐标）
        :param y_list: [A点的Y轴坐标，B点的Y轴坐标，C点的Y轴坐标，D点的Y轴坐标]
        :param duration: the default duration value -1 means a random integer from 2500 to 2501
        """
        super().random_swipe(x_range, y_list, duration)

    def exit_ad_activity(self):
        """退出广告活动页面"""
        print('正在退出广告活动页面')
        sleep(6)
        current_focus = self.adb_ins.get_current_focus()
        if Activity.InciteADActivity in current_focus:
            self.exit_incite_ad_activity()
        elif Activity.PortraitADActivity in current_focus:
            self.exit_portrait_ad_activity()
        elif Activity.MobRewardVideoActivity in current_focus:
            self.exit_mob_reward_video_activity()
        elif Activity.ADBrowser in current_focus:
            self.exit_ad_browser()
        elif Activity.KsRewardVideoActivity in current_focus:
            self.exit_ks_reward_video_activity()
        elif Activity.Stub_Standard_Portrait_Activity in current_focus:
            self.exit_stub_standard_portrait_activity()
        sleep(6)

    def exit_stub_standard_portrait_activity(self):
        """退出stub_standard_portrait活动页面"""
        print('正在退出stub_standard_portrait活动页面')
        try:
            self.uia_ins.click('com.bykv.vk:id/tt_video_ad_close_layout')
        except FileNotFoundError as err:
            print_err(err)
            sleep(10)
            self.exit_stub_standard_portrait_activity()

    def exit_ks_reward_video_activity(self):
        """退出快手激励视频活动页面"""
        print('正在退出快手激励视频活动页面')
        self.uia_ins.click(naf='true', index='1')
        if Activity.KsRewardVideoActivity in self.adb_ins.get_current_focus():
            self.exit_ks_reward_video_activity()

    def exit_incite_ad_activity(self):
        """退出奖励广告活动页面"""
        print('正在退出奖励广告活动页面')
        try:
            while not self.uia_ins.get_dict(text='点击重播'):
                if self.uia_ins.get_dict(text='关闭', xml=self.uia_ins.xml) or self.uia_ins.get_dict(
                        text='安装并打开', xml=self.uia_ins.xml) or self.uia_ins.get_dict(
                        text='继续观看', xml=self.uia_ins.xml):
                    self.adb_ins.press_back_key()
                sleep(20)
            self.adb_ins.press_back_key()
            self.uia_ins.click(text='坚决放弃')
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            sleep(5)
            self.uia_ins.click_by_screen_text('关闭')
        current_focus = self.adb_ins.get_current_focus()
        if Activity.InciteADActivity in current_focus or Activity.ADBrowser in current_focus:
            self.exit_incite_ad_activity()

    def exit_portrait_ad_activity(self, err_cnt=0):
        """退出portrait广告活动页面"""
        print('正在退出portrait广告活动页面')
        try:
            if not self.uia_ins.click(naf='true', index='1'):
                if not self.uia_ins.click(
                        index='1', class_='android.widget.ImageView', xml=self.uia_ins.xml):
                    self.uia_ins.click(
                        index='2', class_='android.widget.ImageView', xml=self.uia_ins.xml)
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            sleep(10)
            if err_cnt > 6:
                self.uia_ins.tap((1016, 63), 6)
            if Activity.MainActivity not in self.adb_ins.get_current_focus():
                return self.exit_portrait_ad_activity(err_cnt+1)
        if Activity.PortraitADActivity in self.adb_ins.get_current_focus():
            return self.exit_portrait_ad_activity()
        return True

    def exit_mob_reward_video_activity(self):
        """退出发现好货广告活动页面"""
        print('正在退出发现好货广告活动页面')
        try:
            self.uia_ins.click(index='2', class_='android.widget.ImageView')
            while Activity.H5SearchPreLoadActivity in self.adb_ins.get_current_focus():
                self.adb_ins.press_back_key(6)
        except FileNotFoundError as err:
            print_err(err)
            sleep(20)
            if self.uia_ins.click_by_screen_text('跳过'):
                return True
            if Activity.MobRewardVideoActivity in self.adb_ins.get_current_focus():
                self.uia_ins.tap((991, 61))
            elif self.uia_ins.get_point_by_screen_text('立即下载', self.uia_ins.txt):
                self.uia_ins.tap((980, 106))
        if Activity.MobRewardVideoActivity in self.adb_ins.get_current_focus():
            return self.exit_mob_reward_video_activity()
        return True

    def exit_ad_browser(self):
        """退出广告浏览器"""
        print('正在退出广告浏览器')
        sleep(36)
        self.uia_ins.tap((584, 335), 16)
        if Activity.ADBrowser in self.adb_ins.get_current_focus():
            self.adb_ins.press_back_key(16)
        else:
            return True
        self.uia_ins.tap((584, 335), 16)
        if Activity.ADBrowser in self.adb_ins.get_current_focus():
            self.adb_ins.press_back_key(16)
        else:
            return True
        self.uia_ins.tap((584, 335), 16)
        if Activity.ADBrowser in self.adb_ins.get_current_focus():
            self.adb_ins.press_back_key(16)
        if Activity.ADBrowser in self.adb_ins.get_current_focus():
            self.uia_ins.click(text='关闭', index='2')
        return True

    def refresh_detail(self):
        """刷新详情页"""
        print('正在刷新详情页')
        self.adb_ins.press_back_key()
        self.adb_ins.press_back_key(6)
        self.uia_ins.tap((631, 633), 6)
        current_focus = self.adb_ins.get_current_focus()
        if Activity.AppDetailActivityInner in current_focus:
            self.adb_ins.press_back_key()
            self.adb_ins.press_back_key()
            self.adb_ins.press_back_key()
            return self.refresh_detail()
        elif Activity.PortraitADActivity in current_focus:
            return
        elif self.uia_ins.get_dict(text='安装并打开', index='0'):
            return self.refresh_detail()
        return True

    def watch_news_detail(self):
        """进入新闻详情页"""
        print('正在进入新闻详情页')
        if Activity.NewsDetailNewActivity in self.adb_ins.get_current_focus():
            self.refresh_detail()
        else:
            return
        if Activity.NewsDetailNewActivity not in self.adb_ins.get_current_focus():
            print('未检测到新闻详情页活动，需要退出')
            return
        cnt = 0
        while cnt < 30:
            self.adb_ins.swipe((536, 1100), (536, 1000), 500)
            sleep(2)
            print(f'cnt={cnt}')
            cnt += 1
        if datetime.now()-self.last_loop_datetime > timedelta(minutes=20):
            print('进入新闻详情页超过20分钟，需要退出')
            return
        print(f'距离退出新闻详情页还剩：{self.last_loop_datetime+timedelta(minutes=20)-datetime.now()}')
        if Activity.NewsDetailNewActivity in self.adb_ins.get_current_focus() and not self.\
                uia_ins.get_dict(ResourceID.bhs):
            self.watch_news_detail()

    def watch_video_detail(self):
        """进入视频详情页"""
        print('正在进入视频详情页')
        if Activity.VideoDetailsActivity in self.adb_ins.get_current_focus():
            self.refresh_detail()
        else:
            return
        cnt = 0
        while cnt < 60:
            sleep(2)
            print(f'cnt={cnt}')
            cnt += 1
        if datetime.now()-self.last_loop_datetime > timedelta(minutes=20):
            print('进入视频详情页超过20分钟，需要退出')
            return
        print(f'距离退出视频详情页还剩：{self.last_loop_datetime+timedelta(minutes=20)-datetime.now()}')
        if Activity.VideoDetailsActivity in self.adb_ins.get_current_focus():
            self.watch_video_detail()

    def watch_detail(self, reopen_flag=True):  # pylint: disable=too-many-branches
        """进入视频或者新闻详情页赚金币"""
        print('正在进入视频或者新闻详情页赚金币')
        if reopen_flag:
            self.reopen_app()
            self.uia_ins.tap((693, 253), 6)
            self.adb_ins.press_back_key(6)
        try:
            if self.uia_ins.click(ResourceID.ae3):  # 领50金币
                self.exit_ad_activity()
                while self.uia_ins.click_by_screen_text('看视频再领'):
                    self.exit_ad_activity()
            elif self.uia_ins.get_dict(ResourceID.ae6, xml=self.uia_ins.xml):  # 您已获得提取0.3元现金机会
                self.adb_ins.press_back_key()
        except FileNotFoundError as err:
            print_err(err)
        self.uia_ins.tap((631, 633), 6)
        current_focus = self.adb_ins.get_current_focus()
        if Activity.ADBrowser in current_focus or Activity.AppActivity in current_focus:
            return self.watch_detail()
        if Activity.VideoDetailsActivity in current_focus:
            self.watch_video_detail()
        try:
            while self.uia_ins.get_dict(text='安装并打开', index='0') or self.uia_ins.get_dict(
                    naf='true', index='1'):
                self.refresh_detail()
                current_focus = self.adb_ins.get_current_focus()
        except FileNotFoundError as err:
            print_err(err)
            return self.watch_detail()
        if Activity.NewsDetailNewActivity in current_focus:
            if self.uia_ins.click(ResourceID.bhs):
                while self.uia_ins.click_by_screen_text('看视频再领'):
                    self.exit_ad_activity()
        if Activity.NewsDetailNewActivity in self.adb_ins.get_current_focus() and self.uia_ins.\
                get_dict(ResourceID.a8h):
            self.watch_news_detail()
        return True

    def get_coins_by_bxs(self):
        """通过bxs（看5秒领金币、看视频领金币）来获取金币"""
        print('正在通过bxs（看5秒领金币、看视频领金币）来获取金币')
        if self.uia_ins.click_by_screen_text(text='看5秒领金币'):
            if Activity.AppActivity in self.adb_ins.get_current_focus():
                sleep(9)
                self.adb_ins.press_back_key(3)
            return True
        if self.uia_ins.click_by_screen_text(text='看视频领金币', txt=self.uia_ins.txt):
            self.exit_ad_activity()
            while self.uia_ins.click_by_screen_text('看视频再领'):
                if Activity.BdShellActivity in self.adb_ins.get_current_focus():
                    self.adb_ins.press_back_key(3)
                else:
                    self.exit_ad_activity()
            return True
        return False

    def enter_task_interface(self):
        """进入任务界面"""
        self.reopen_app()
        print('正在进入任务界面')
        self.uia_ins.tap((765, 1833), 6)
        try:
            if self.uia_ins.click(ResourceID.a6u, '签到领'):
                while self.uia_ins.click_by_screen_text(text='看视频再领'):
                    self.exit_ad_activity()
                self.uia_ins.click_by_screen_text(text='知道了')
        except FileNotFoundError as err:
            print_err(err)

    def watch_bxs(self):
        """观看bxs（看5秒领金币、看视频领金币）"""
        self.enter_task_interface()
        print('正在观看bxs（看5秒领金币、看视频领金币）')
        while self.get_coins_by_bxs():
            sleep(6)

    def change_money(self):
        """把金币换成钱"""
        self.reopen_app()
        self.uia_ins.tap((977, 1839), 6)
        print('正在把金币换成钱')
        self.uia_ins.click(ResourceID.be2)
        sleep(9)
        if Activity.MainActivity in self.adb_ins.get_current_focus():
            return self.change_money()
        if self.uia_ins.click(text='重试', index='2'):
            sleep(6)
        sleep(9)
        if self.uia_ins.get_dict('recommendNewProduct'):
            return self.change_money()
        price_number = self.uia_ins.get_dict('price_number').get('@text', '0')
        price_number = price_number.replace(',', '')
        price_number = int(price_number)
        print(price_number)
        if price_number > 50000:
            self.uia_ins.click(text='5元50000金币')
        elif price_number > 10000:
            self.uia_ins.click(text='1元10000金币')
        elif price_number > 1000:
            self.uia_ins.click(text='1000金币')
        self.uia_ins.click('alipay_quick')  # 立即提现
        if self.uia_ins.get_dict(text='提现成功，已到账'):
            print('提现成功，已到账')
            return True
        print('提现失败，可能由于签到时间不足')
        return False

    def watch_little_videos(self):
        """看小视频"""
        self.reopen_app()
        print('正在看小视频')
        self.uia_ins.tap((539, 1836), 6)
        swipe_cnt = 0
        start_datetime = datetime.now()
        while True:
            swipe_cnt += 1
            self.random_swipe()
            sleep(randint(60, 90))
            run_datetime = datetime.now()-start_datetime
            print(f'swipe_cnt={swipe_cnt} run_datetime={run_datetime}')
            if run_datetime > timedelta(minutes=20):
                break

    def watch_videos_to_make_money(self):
        """看视频赚钱的方法"""
        self.reopen_app()
        print('正在看视频赚钱的方法')
        self.uia_ins.tap((968, 1839), 6)
        self.uia_ins.click(ResourceID.ch1, '看视频赚钱')
        if Activity.InciteADActivity in self.adb_ins.get_current_focus():
            while not self.uia_ins.get_point_by_screen_text('已发放观看奖励'):
                sleep(30)
            self.adb_ins.press_back_key()
            self.uia_ins.click(text='坚决放弃')

    @run_forever
    def mainloop(self):
        """趣头条中央控制系统类的主循环成员方法"""
        self.watch_detail()
        self.watch_bxs()
        show_datetime('mainloop')
        self.last_loop_datetime = datetime.now()
