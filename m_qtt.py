"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Qtt

Config.set_debug(True)
Qtt('003001001').mainloop()
# Qtt('003001001').exit_incite_ad_activity()
