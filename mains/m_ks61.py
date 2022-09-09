"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Ksjsb

Config.set_debug(True)
# Ksjsb('002006001').mainloop()
Ksjsb('002006001').change_money()
