"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Ksjsb

Config.set_debug(True)
Ksjsb('003001002').mainloop()
# Ksjsb('003001002').watch_live()
# Ksjsb('003001002').view_ads()
# Ksjsb('003001002').shopping()
# Ksjsb('003001002').get_double_bonus()
# Ksjsb('003001002').get_desktop_component_coin()
# Ksjsb('003001002').enter_wealth_interface()
