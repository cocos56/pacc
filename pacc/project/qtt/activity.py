"""趣头条中央控制系统包的活动模块"""
ROOT = 'com.jifen.qukan/com.'


# pylint: disable=too-few-public-methods
class Activity:
    """趣头条中央控制系统模块的安卓活动名类"""
    # 【主界面】
    MainActivity = f'{ROOT}jifen.qkbase.main.MainActivity'

    # 【搜索界面】由主界面转入
    H5SearchPreLoadActivity = f'{ROOT}jifen.qukan.content.search.H5SearchPreLoadActivity'

    # 【直播界面】由主界面转入
    VideoLiveAutoLoadActivity = f'{ROOT}jifen.qukan.content.newslist.video.' \
                                f'VideoLiveAutoLoadActivity'

    #  【小米商店应用详情】由主界面的新闻标题中的广告标题转入
    AppDetailActivityInner = 'com.xiaomi.market/com.xiaomi.market.ui.detail.AppDetailActivityInner'

    #  【提现兑换界面】
    WebActivity = f'{ROOT}jifen.qkbase.web.WebActivity'

    BdShellActivity = f'{ROOT}baidu.mobads.sdk.api.BdShellActivity'
    # 奖励广告活动
    InciteADActivity = f'{ROOT}iclicash.advlib.ui.front.InciteADActivity'
    PortraitADActivity = f'{ROOT}qq.e.ads.PortraitADActivity'
    # 发现好货广告活动
    MobRewardVideoActivity = f'{ROOT}baidu.mobads.sdk.api.MobRewardVideoActivity'
    ADBrowser = f'{ROOT}iclicash.advlib.ui.front.ADBrowser'  # 广告浏览器
    KsRewardVideoActivity = f'{ROOT}kwad.sdk.api.proxy.app.KsRewardVideoActivity'
    AppActivity = f'{ROOT}baidu.mobads.sdk.api.AppActivity'  # 看5秒领金币
    Stub_Standard_Portrait_Activity = f'{ROOT}bykv.vk.openvk.stub.activity.' \
                                      f'Stub_Standard_Portrait_Activity'
    # 【详情页】
    # 新闻详情
    NewsDetailNewActivity = f'{ROOT}jifen.qukan.content.newsdetail.news.NewsDetailNewActivity'
    # 视频详情
    VideoDetailsActivity = f'{ROOT}jifen.qukan.content.videodetail.VideoDetailsActivity'
