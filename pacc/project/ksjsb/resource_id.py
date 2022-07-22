"""快手极速版工程包的资源ID模块"""
ROOT = 'com.kuaishou.nebula:id/'


# pylint: disable=too-few-public-methods
class ResourceID:
    """快手极速版的安卓资源ID类"""
    award_title_prefix = f'{ROOT}award_title_prefix'  # 观看精彩直播，可领
    # 放弃奖励
    award_video_close_dialog_abandon_button = f'{ROOT}award_video_close_dialog_abandon_button'
    button2 = 'android:id/button2'  # 等待按钮（应用长时间无反应）
    animated_image = f'{ROOT}animated_image'  # 主界面左上方关闭奥运福娃按钮
    choose_tv = f'{ROOT}choose_tv'  # 请选择你要进行的操作（不感兴趣、关注）
    close = f'{ROOT}close'  # 关闭邀请新朋友（面对面邀请一个朋友赚51元）
    comment_header_close = f'{ROOT}comment_header_close'  # 关闭评论
    cycle_progress = f'{ROOT}cycle_progress'  # 金币进度
    dialog_close = f'{ROOT}dialog_close'  # 关闭电商购物优惠券
    description = f'{ROOT}description'  # 网络连接失败，请稍后重试
    left_btn = f'{ROOT}left_btn'  # 主界面左上角菜单项
    negative = 'com.kuaishou.nebula:id/negative'  # 忽略（打开推送通知，对方有更新时，第一时间获得提醒。）
    nick = f'{ROOT}nick'  # 看直播页面主播昵称
    red_packet_anim = f'{ROOT}red_packet_anim'  # 主界面右上方红包图标
    gold_egg_anim = f'{ROOT}gold_egg_anim'  # 金蛋
    iv_close_common_dialog = f'{ROOT}iv_close_common_dialog'  # 主界面右上方关闭奥运夺冠瞬间界面
    positive = f'{ROOT}positive'  # 主界面中间青少年模式，我知道了
    tab_text = f'{ROOT}tab_text'  # 详细信息/评论
    live_follow_guide_card_button = f'{ROOT}live_follow_guide_card_button'  # 立即关注（财富界面进入）
    live_exit_button = f'{ROOT}live_exit_button'  # 直接退出（直播）
    exit_btn = f'{ROOT}exit_btn'  # 退出（直播）
    live_simple_play_swipe_text = f'{ROOT}live_simple_play_swipe_text'  # 点击进入直播间
    open_long_atlas = f'{ROOT}open_long_atlas'  # 点击打开长图
    tv_upgrade_now = f'{ROOT}tv_upgrade_now'  # 免打扰升级
