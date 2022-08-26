"""趣头条中央控制系统包的活动模块"""
ROOT = 'com.jifen.qukan/com.'


# pylint: disable=too-few-public-methods
class Activity:
    """趣头条中央控制系统模块的安卓活动名类"""
    MainActivity = f'{ROOT}jifen.qkbase.main.MainActivity'  # 主界面
    BdShellActivity = f'{ROOT}baidu.mobads.sdk.api.BdShellActivity'
    WebActivity = f'{ROOT}jifen.qkbase.web.WebActivity'
    # 奖励广告活动
    InciteADActivity = f'{ROOT}iclicash.advlib.ui.front.InciteADActivity'
    PortraitADActivity = f'{ROOT}qq.e.ads.PortraitADActivity'
    # 发现好货广告活动
    MobRewardVideoActivity = f'{ROOT}baidu.mobads.sdk.api.MobRewardVideoActivity'
    ADBrowser = f'{ROOT}iclicash.advlib.ui.front.ADBrowser'  # 广告浏览器
    KsRewardVideoActivity = f'{ROOT}kwad.sdk.api.proxy.app.KsRewardVideoActivity'
    AppActivity = f'{ROOT}baidu.mobads.sdk.api.AppActivity'  # 看5秒领金币
    # 【详情页】
    # 新闻详情
    NewsDetailNewActivity = f'{ROOT}jifen.qukan.content.newsdetail.news.NewsDetailNewActivity'
    # 视频详情
    VideoDetailsActivity = f'{ROOT}jifen.qukan.content.videodetail.VideoDetailsActivity'
