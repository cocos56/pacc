"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Ksjsb

Config.set_debug(True)
Ksjsb('002002003').mainloop()
# Ksjsb('002002003').get_daily_challenge_coins(True, False)
Ksjsb('002002003').mainloop()
