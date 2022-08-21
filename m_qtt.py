"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Qtt

Config.set_debug(True)
# Qtt('002004003').mainloop()
# Qtt('002004003').reopen_app()
Qtt('002004003').view_ads_video()
