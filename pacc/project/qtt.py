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
    # 新闻详情
    NewsDetailNewActivity = \
        'com.jifen.qukan/com.jifen.qukan.content.newsdetail.news.NewsDetailNewActivity'


# pylint: disable=too-few-public-methods
class ResourceID:
    """趣头条中央控制系统模块的安卓资源身份码类"""
    ch1 = "com.jifen.qukan:id/ch1"  # 看视频赚钱
    a0m = 'com.jifen.qukan:id/a0m'  # 看视频再领xx金币
    bh4 = 'com.jifen.qukan:id/bh4'  # 阅读奖励图标


class Qtt(Project):
    """趣头条中央控制系统类"""

    def open_app(self):
        """打开趣头条APP"""
        print('正在打开快手极速版APP')
        self.adb_ins.open_app(Activity.MainActivity)
        sleep(9)

    def random_swipe(self, x_range=(360, 390), y_list=(1160, 1190, 260, 290)):
        """随机滑动一段长度

        :param x_range : x_min（A、C点的X轴坐标）与x_max（B、D点的X轴坐标）
        :param y_list: [A点的Y轴坐标，B点的Y轴坐标，C点的Y轴坐标，D点的Y轴坐标]
        """
        super().random_swipe(x_range, y_list)

    def exit_incite_ad_activity(self):
        """退出奖励广告活动页面"""
        while not self.uia_ins.get_dict(text='点击重播'):
            sleep(30)
        self.adb_ins.press_back_key()
        self.uia_ins.click(text='坚决放弃')

    def exit_portrait_ad_activity(self):
        """退出portrait广告活动页面"""
        self.uia_ins.click(index='1', class_='android.widget.ImageView')

    def watch_news(self):
        """看新闻"""
        self.reopen_app()

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
