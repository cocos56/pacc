"""快手极速版程序入口模块"""
from pacc.project import KSJSB
from pacc.config import Config


Config.set_debug(True)
KSJSB('003001002').enter_wealth_interface()
# KSJSB('003001001').signIn()
# KSJSB('003001001').getWealth()
# KSJSB('003001002').getWealth()
# KSJSB('003001003').getWealth()
# KSJSB('003001004').getWealth()
# KSJSB('003001001').updateWealth()
# KSJSB('003001002').updateWealth()
# KSJSB('003001003').updateWealth()
# KSJSB('003001004').updateWealth()
# KSJSB('003001004').watchLive()
