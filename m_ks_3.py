"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Ksjsb

Config.set_debug(True)
# Ksjsb('003001003').mainloop()
Ksjsb('003001003').get_flash_benefits()
# Ksjsb('003001003').update_wealth()
# Ksjsb('003001003').get_wealth()
