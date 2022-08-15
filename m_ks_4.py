"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Ksjsb

Config.set_debug(True)
# Ksjsb('003001004').mainloop()
Ksjsb('003001004').get_double_bonus()
# Ksjsb('003001004').view_ads()
# Ksjsb('003001004').change_money()
# Ksjsb('003001004').update_wealth()
