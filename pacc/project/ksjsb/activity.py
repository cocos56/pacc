"""快手极速版工程包的活动模块"""
ROOT = 'com.kuaishou.nebula/com.'


# pylint: disable=too-few-public-methods
class Activity:
    """快手极速版活动名类"""
    # 【搜索界面】由桌面组件转入
    SearchActivity = f'{ROOT}yxcorp.plugin.search.SearchActivity'

    #  【看视频界面（主界面）】
    HomeActivity = f'{ROOT}yxcorp.gifshow.HomeActivity'  # 主界面

    #  【登录界面】由主界面转入
    PhoneLoginActivity = f'{ROOT}yxcorp.login.userlogin.activity.PhoneLoginActivity'

    #  【财富界面】
    KwaiYodaWebViewActivity = f'{ROOT}yxcorp.gifshow.webview.KwaiYodaWebViewActivity'  # 财富界面

    # 【看广告界面】由财富界面->开宝箱转入
    AwardVideoPlayActivity = f'{ROOT}yxcorp.gifshow.ad.neo.video.award.AwardVideoPlayActivity'

    # 【看直播领金币界面】由财富界面->领福利转入
    #  看直播领金币
    AwardFeedFlowActivity = f'{ROOT}yxcorp.gifshow.ad.award.flow.AwardFeedFlowActivity'

    # 【直播界面】由财富界面->领福利->看直播领金币界面转入
    PhotoDetailActivity = f'{ROOT}yxcorp.gifshow.detail.PhotoDetailActivity'  # 直播

    # 【逛街界面】由财富界面->去逛街转入
    AdKwaiRnActivity = f'{ROOT}yxcorp.gifshow.ad.rn.AdKwaiRnActivity'

    # 【选择使用的应用界面】提现时会让分享，多开应用时会出现让选择应用的情况
    ResolverActivity = 'android/com.android.internal.app.ResolverActivity'

    LiveSlideActivity = f'{ROOT}kuaishou.live.core.basic.activity.LiveSlideActivity'  # 游戏直播
    UserProfileActivity = f'{ROOT}yxcorp.gifshow.profile.activity.UserProfileActivity'  # 用户主页
    AdYodaActivity = f'{ROOT}yxcorp.gifshow.ad.webview.AdYodaActivity'  # 广告（看视频时出现）
    TopicDetailActivity = f'{ROOT}yxcorp.plugin.tag.topic.TopicDetailActivity'  # 每日书单
    MiniAppActivity0 = f'{ROOT}mini.app.activity.MiniAppActivity0'  # 小程序
    KRT1Activity = f'{ROOT}kwai.frog.game.engine.adapter.engine.base.KRT1Activity'  # 拯救小金鱼游戏
