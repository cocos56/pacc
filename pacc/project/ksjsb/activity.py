"""快手极速版工程包的活动模块"""
ROOT = 'com.kuaishou.nebula/com.'


# pylint: disable=too-few-public-methods
class Activity:
    """快手极速版活动名类"""
    AwardFeedFlowActivity = f'{ROOT}yxcorp.gifshow.ad.award.flow.AwardFeedFlowActivity'
    HomeActivity = f'{ROOT}yxcorp.gifshow.HomeActivity'  # 主界面
    PhotoDetailActivity = f'{ROOT}yxcorp.gifshow.detail.PhotoDetailActivity'  # 直播
    UserProfileActivity = f'{ROOT}yxcorp.gifshow.profile.activity.UserProfileActivity'  # 用户主页
    AdYodaActivity = f'{ROOT}yxcorp.gifshow.ad.webview.AdYodaActivity'  # 广告（看视频时出现）
    # 看广告界面（由财富界面转入）
    AwardVideoPlayActivity = f'{ROOT}yxcorp.gifshow.ad.award.AwardVideoPlayActivity'
    KwaiYodaWebViewActivity = f'{ROOT}yxcorp.gifshow.webview.KwaiYodaWebViewActivity'  # 财富界面
    TopicDetailActivity = f'{ROOT}yxcorp.plugin.tag.topic.TopicDetailActivity'  # 每日书单
    MiniAppActivity0 = f'{ROOT}mini.app.activity.MiniAppActivity0'  # 小程序
    KRT1Activity = f'{ROOT}kwai.frog.game.engine.adapter.engine.base.KRT1Activity'  # 拯救小金鱼游戏
    SearchActivity = 'com.android.quicksearchbox/com.android.quicksearchbox.SearchActivity'
