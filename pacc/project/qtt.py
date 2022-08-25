"""趣头条中央控制系统模块"""
from datetime import datetime, timedelta
from random import randint

from .project import Project
from ..base import run_forever, sleep, print_err, show_datetime


# pylint: disable=too-few-public-methods
class Activity:
    """趣头条中央控制系统模块的安卓活动名类"""
    MainActivity = 'com.jifen.qukan/com.jifen.qkbase.main.MainActivity'  # 主界面
    # 奖励广告活动
    InciteADActivity = 'com.jifen.qukan/com.iclicash.advlib.ui.front.InciteADActivity'
    PortraitADActivity = 'com.jifen.qukan/com.qq.e.ads.PortraitADActivity'
    # 发现好货广告活动
    MobRewardVideoActivity = 'com.jifen.qukan/com.baidu.mobads.sdk.api.MobRewardVideoActivity'
    ADBrowser = 'com.jifen.qukan/com.iclicash.advlib.ui.front.ADBrowser'  # 广告浏览器
    KsRewardVideoActivity = 'com.jifen.qukan/com.kwad.sdk.api.proxy.app.KsRewardVideoActivity'
    AppActivity = 'com.jifen.qukan/com.baidu.mobads.sdk.api.AppActivity'  # 看5秒领金币
    # 【详情页】
    # 新闻详情
    NewsDetailNewActivity = \
        'com.jifen.qukan/com.jifen.qukan.content.newsdetail.news.NewsDetailNewActivity'
    # 视频详情
    VideoDetailsActivity = \
        'com.jifen.qukan/com.jifen.qukan.content.videodetail.VideoDetailsActivity'


# pylint: disable=too-few-public-methods
class ResourceID:
    """趣头条中央控制系统模块的安卓资源身份码类"""
    ch1 = "com.jifen.qukan:id/ch1"  # 看视频赚钱
    a0m = 'com.jifen.qukan:id/a0m'  # 看视频再领xx金币
    bh4 = 'com.jifen.qukan:id/bh4'  # 阅读奖励图标
    # 【头条界面】
    b2d = "com.jifen.qukan:id/b2d"  # 文章标题
    ap7 = "com.jifen.qukan:id/ap7"  # 关闭图标（恭喜你获得一个5400金币的问卷任务）
    adh = "com.jifen.qukan:id/adh"  # 领50金币


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
            self.uia_ins.click(ResourceID.ap7)
        except FileNotFoundError as err:
            print_err(err)
        if self.uia_ins.click_by_screen_text('领取'):
            if Activity.InciteADActivity in self.adb_ins.get_current_focus():
                self.adb_ins.press_back_key(6)
            else:
                sleep(6)
                if self.uia_ins.click_by_screen_text('再领'):
                    self.exit_ad_activity()

    def random_swipe(self, x_range=(360, 390), y_list=(1160, 1190, 260, 290)):
        """随机滑动一段长度

        :param x_range : x_min（A、C点的X轴坐标）与x_max（B、D点的X轴坐标）
        :param y_list: [A点的Y轴坐标，B点的Y轴坐标，C点的Y轴坐标，D点的Y轴坐标]
        """
        super().random_swipe(x_range, y_list)

    def exit_ad_activity(self):
        """退出广告活动页面"""
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
        sleep(6)

    def exit_ks_reward_video_activity(self):
        """退出快手激励视频活动页面"""
        self.uia_ins.click(naf='true', index='1')
        if Activity.KsRewardVideoActivity in self.adb_ins.get_current_focus():
            self.exit_ks_reward_video_activity()

    def exit_incite_ad_activity(self):
        """退出奖励广告活动页面"""
        while not self.uia_ins.get_dict(text='点击重播'):
            if self.uia_ins.get_dict(text='关闭', xml=self.uia_ins.xml):
                self.adb_ins.press_back_key()
            sleep(20)
        self.adb_ins.press_back_key()
        self.uia_ins.click(text='坚决放弃')

    def exit_portrait_ad_activity(self):
        """退出portrait广告活动页面"""
        try:
            if not self.uia_ins.click(naf='true', index='1'):
                if not self.uia_ins.click(index='1', class_='android.widget.ImageView'):
                    self.uia_ins.click(
                        index='2', class_='android.widget.ImageView', xml=self.uia_ins.xml)
            else:
                self.uia_ins.click(index='2', class_='android.widget.ImageView')
        except FileNotFoundError as err:
            print_err(err)
            if Activity.MainActivity not in self.adb_ins.get_current_focus():
                return self.exit_portrait_ad_activity()
        if Activity.PortraitADActivity in self.adb_ins.get_current_focus():
            return self.exit_portrait_ad_activity()
        return True

    def exit_mob_reward_video_activity(self):
        """退出发现好货广告活动页面"""
        try:
            self.uia_ins.click(index='2', class_='android.widget.ImageView')
        except FileNotFoundError as err:
            print_err(err)
            if Activity.MainActivity not in self.adb_ins.get_current_focus() and self.\
                    uia_ins.get_point_by_screen_text('立即下载'):
                self.uia_ins.tap((980, 106))
            return self.exit_mob_reward_video_activity()
        if Activity.MobRewardVideoActivity in self.adb_ins.get_current_focus():
            return self.exit_mob_reward_video_activity()
        return True

    def exit_ad_browser(self):
        """退出广告浏览器"""
        sleep(36)
        self.uia_ins.tap((584, 335), 16)
        if Activity.ADBrowser in self.adb_ins.get_current_focus():
            self.adb_ins.press_back_key(16)
        self.uia_ins.tap((584, 335), 16)
        if Activity.ADBrowser in self.adb_ins.get_current_focus():
            self.adb_ins.press_back_key(16)
        self.uia_ins.tap((584, 335), 16)
        if Activity.ADBrowser in self.adb_ins.get_current_focus():
            self.adb_ins.press_back_key(16)
        if Activity.ADBrowser in self.adb_ins.get_current_focus():
            self.uia_ins.click(text='关闭', index='2')

    def refresh_detail(self):
        """刷新详情页"""
        self.adb_ins.press_back_key()
        self.adb_ins.press_back_key(6)
        self.uia_ins.tap((300, 400), 6)

    def watch_news_detail(self):
        """进入新闻详情页"""
        if Activity.NewsDetailNewActivity in self.adb_ins.get_current_focus():
            self.refresh_detail()
        else:
            return
        cnt = 0
        while cnt < 30:
            self.adb_ins.swipe(536, 1100, 536, 1000)
            sleep(2)
            print(f'cnt={cnt}')
            cnt += 1
        if datetime.now()-self.last_loop_datetime > timedelta(minutes=20):
            print('进入新闻详情页超过20分钟，需要退出')
            return
        else:
            print(f'距离退出新闻详情页还剩：'
                  f'{self.last_loop_datetime+timedelta(minutes=20)-datetime.now()}')
        if Activity.NewsDetailNewActivity in self.adb_ins.get_current_focus() and not self.\
                uia_ins.get_dict(ResourceID.bh4):
            self.watch_news_detail()

    def watch_video_detail(self):
        """进入视频详情页"""
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
        else:
            print(f'距离退出视频详情页还剩：'
                  f'{self.last_loop_datetime+timedelta(minutes=20)-datetime.now()}')
        if Activity.VideoDetailsActivity:
            self.watch_video_detail()

    def watch_detail(self):
        """进入视频或者新闻详情页赚金币"""
        self.reopen_app()
        self.uia_ins.tap((693, 253), 6)
        self.adb_ins.press_back_key(6)
        try:
            if self.uia_ins.click(ResourceID.adh):
                self.exit_ad_activity()
                while self.uia_ins.click_by_screen_text('看视频再领'):
                    self.exit_ad_activity()
        except FileNotFoundError as err:
            print_err(err)
        self.uia_ins.tap((300, 400), 6)
        current_focus = self.adb_ins.get_current_focus()
        if Activity.NewsDetailNewActivity in current_focus:
            if self.uia_ins.click(ResourceID.bh4):
                while self.uia_ins.click_by_screen_text('看视频再领'):
                    self.exit_ad_activity()
            self.watch_news_detail()
        elif Activity.VideoDetailsActivity in current_focus:
            self.watch_video_detail()

    def get_coins_by_bxs(self):
        """通过bxs（看5秒领金币、看视频领金币）来获取金币"""
        if self.uia_ins.click_by_screen_text(text='看5秒领金币'):
            if Activity.AppActivity in self.adb_ins.get_current_focus():
                sleep(9)
                self.adb_ins.press_back_key(3)
            return True
        if self.uia_ins.click_by_screen_text(text='看视频领金币', txt=self.uia_ins.txt):
            self.exit_ad_activity()
            while self.uia_ins.click_by_screen_text('看视频再领'):
                self.exit_ad_activity()
            return True
        return False

    def watch_bxs(self):
        """观看bxs（看5秒领金币、看视频领金币）"""
        self.reopen_app()
        self.uia_ins.tap((757, 1836), 6)
        while self.get_coins_by_bxs():
            pass

    def watch_little_videos(self):
        """看小视频"""
        self.reopen_app()
        self.uia_ins.tap((539, 1836), 6)
        swipe_cnt = 0
        while True:
            swipe_cnt += 1
            self.random_swipe()
            sleep(randint(15, 18))
            print(f'swipe_cnt={swipe_cnt}')
            if swipe_cnt > 10:
                swipe_cnt = 0
                if self.uia_ins.click_by_screen_text('阅读奖励'):
                    input()

    def watch_videos_to_make_money(self):
        """看视频赚钱的方法"""
        self.reopen_app()
        self.uia_ins.tap((968, 1839), 6)
        self.uia_ins.click(ResourceID.ch1, '看视频赚钱')
        if Activity.InciteADActivity in self.adb_ins.get_current_focus():
            while not self.uia_ins.get_point_by_screen_text('已发放观看奖励'):
                sleep(30)
            self.adb_ins.press_back_key()
            self.uia_ins.click(text='坚决放弃')
        # while not self.uia_ins.secure_get_current_ui_hierarchy():
        #     sleep(30)

    @run_forever
    def mainloop(self):
        """趣头条中央控制系统类的主循环成员方法"""
        # while self.uia_ins.click_by_screen_text('看视频再领'):
        #     self.exit_ad_activity()
        self.watch_detail()
        self.watch_bxs()
        show_datetime('mainloop')
        self.last_loop_datetime = datetime.now()
