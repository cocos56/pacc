"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Ksjsb

Config.set_debug(True)
Ksjsb('002002001').mainloop()
# Ksjsb('002002001').get_daily_challenge_coins(True)
