from ..tools import sleep
from .project import Project

root = 'com.ss.android.ugc.aweme/'


class ContentDesc:
    WonTheLuckyBag = '恭喜抽中福袋'


class Activity:
    SplashActivity = root + 'com.ss.android.ugc.aweme.splash.SplashActivity'  # 抖音程序入口
    LivePlayActivity = root + 'com.ss.android.ugc.aweme.live.LivePlayActivity'  # 直播
    FollowRelationTabActivity = root + 'com.ss.android.ugc.aweme.following.ui.FollowRelationTabActivity'  # 关注列表


class ResourceID:
    tv_cancel = 'com.ss.android.ugc.aweme:id/tv_cancel'  # （暂时不要）发现通讯录好友
    c_w = 'com.ss.android.ugc.aweme:id/c=w'  # 个人资料页关注数量（点击我之后）
    fi5 = 'com.ss.android.ugc.aweme:id/fi5'  # 个人资料页头像（点击正在直播之后）


class DYFD(Project):
    def __init__(self, deviceSN):
        super(DYFD, self).__init__(deviceSN)

    def enterLiveRoom(self):
        self.reopenApp()
        self.getLiveRoom()

    def getLiveRoom(self):
        try:
            while not self.uIAIns.click(text='正在直播'):
                self.randomSwipe()
            self.uIAIns.click(ResourceID.fi5)
        except FileNotFoundError:
            self.getLiveRoom()

    def randomSwipe(self):
        super(DYFD, self).randomSwipe(639, 666, 639, 666, 1689, 1699, 609, 619, True)

    def openApp(self):
        super(DYFD, self).openApp(Activity.SplashActivity)
        sleep(20)
        try:
            self.uIAIns.click(ResourceID.tv_cancel)
        except FileNotFoundError as e:
            print(e)
        self.uIAIns.tap([966, 1836], 3)
        try:
            if not self.uIAIns.click(ResourceID.c_w):
                self.reopenApp()
        except FileNotFoundError as e:
            print(e)
            self.reopenApp()
