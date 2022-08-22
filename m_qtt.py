"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Qtt

Config.set_debug(True)
# Qtt('002004003').mainloop()
# Qtt('002004003').reopen_app()
# Qtt('002004003').watch_videos_to_make_money()
# Qtt('002004003').watch_little_videos()
# Qtt('002004003').watch_news()
# Qtt('002004003').exit_ad_activity()
# Qtt('002004003').exit_incite_ad_activity()
Qtt('002004003').exit_portrait_ad_activity()
