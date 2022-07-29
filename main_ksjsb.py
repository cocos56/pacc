"""快手极速版程序入口模块"""
from pacc.project import KSJSB
from pacc.config import Config


Config.set_debug(True)
KSJSB('003001002').mainloop()
# KSJSB('003001002').open_app()
# KSJSB('003001002').open_treasure_box()
# KSJSB('003001002').change_money()
# KSJSB('003001002').enter_wealth_interface()
# KSJSB('003001002').update_wealth()
# KSJSB('003001002').get_wealth()
