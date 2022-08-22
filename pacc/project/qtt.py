"""趣头条中央控制系统模块"""
from random import randint
from .project import Project
from ..base import run_forever, sleep


# pylint: disable=too-few-public-methods
class Activity:
    """趣头条中央控制系统模块的安卓活动名类"""
    MainActivity = 'com.jifen.qukan/com.jifen.qkbase.main.MainActivity'  # 主界面
    # 奖励广告活动
    InciteADActivity = 'com.jifen.qukan/com.iclicash.advlib.ui.front.InciteADActivity'
    PortraitADActivity = 'com.jifen.qukan/com.qq.e.ads.PortraitADActivity'
    # 发现好货广告活动
    MobRewardVideoActivity = 'com.jifen.qukan/com.baidu.mobads.sdk.api.MobRewardVideoActivity'
    # 新闻详情
    NewsDetailNewActivity = \
        'com.jifen.qukan/com.jifen.qukan.content.newsdetail.news.NewsDetailNewActivity'
    ADBrowser = 'com.jifen.qukan/com.iclicash.advlib.ui.front.ADBrowser'


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

    def open_app(self):
        """打开趣头条APP"""
        print('正在打开快手极速版APP')
        self.adb_ins.open_app(Activity.MainActivity)
        sleep(16)

    def random_swipe(self, x_range=(360, 390), y_list=(1160, 1190, 260, 290)):
        """随机滑动一段长度

        :param x_range : x_min（A、C点的X轴坐标）与x_max（B、D点的X轴坐标）
        :param y_list: [A点的Y轴坐标，B点的Y轴坐标，C点的Y轴坐标，D点的Y轴坐标]
        """
        super().random_swipe(x_range, y_list)

    def exit_ad_activity(self):
        """推出广告活动页面"""
        current_focus = self.adb_ins.get_current_focus()
        if Activity.InciteADActivity in current_focus:
            self.exit_incite_ad_activity()
        elif Activity.PortraitADActivity in current_focus:
            self.exit_portrait_ad_activity()

    def exit_incite_ad_activity(self):
        """退出奖励广告活动页面"""
        while not self.uia_ins.get_dict(text='点击重播'):
            if self.uia_ins.get_dict(text='关闭', xml=self.uia_ins.xml):
                self.adb_ins.press_back_key()
            sleep(30)
        self.adb_ins.press_back_key()
        self.uia_ins.click(text='坚决放弃')

    def exit_portrait_ad_activity(self):
        """退出portrait广告活动页面"""
        if not self.uia_ins.click(index='1', class_='android.widget.ImageView'):
            self.uia_ins.click(index='2', class_='android.widget.ImageView', xml=self.uia_ins.xml)
        if Activity.PortraitADActivity in self.adb_ins.get_current_focus():
            return self.exit_portrait_ad_activity()

    def exit_mob_reward_video_activity(self):
        """退出发现好货广告活动页面"""

    def watch_news(self):
        """看新闻"""
        self.reopen_app()
        self.uia_ins.click(ResourceID.ap7)
        self.uia_ins.tap((831, 253), 6)
        self.adb_ins.press_back_key(6)
        if self.uia_ins.click(ResourceID.adh):
            sleep(6)
            if self.uia_ins.click(text='看视频再领'):
                sleep(6)
        else:
            self.uia_ins.click(ResourceID.b2d)
            self.uia_ins.click(ResourceID.bh4)

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
