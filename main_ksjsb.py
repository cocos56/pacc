"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Ksjsb

Config.set_debug(True)
Ksjsb('003001002').mainloop()
# Ksjsb('003001002').read_novel()
