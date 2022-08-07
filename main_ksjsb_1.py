"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Ksjsb

Config.set_debug(True)
Ksjsb('003001001').mainloop()
# Ksjsb('003001001').exit_live()
# Ksjsb('003001001').get_flash_benefits()
# Ksjsb('003001001').enter_wealth_interface()
# Ksjsb('003001001').get_double_bonus()
# Ksjsb('003001001').change_money()
# Ksjsb('003001001').open_exclusive_gold_coin_gift_pack()
# Ksjsb('003001001').view_ads()
# Ksjsb('003001001').watch_live()
# Ksjsb('003001001').open_meal_allowance()
# Ksjsb('003001001').open_treasure_box()
