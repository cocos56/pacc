"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Ksjsb

Config.set_debug(True)
# Ksjsb('003001001').mainloop()
Ksjsb('003001001').reopen_app()
# Ksjsb('003001001').buy_things_with_coins()
# Ksjsb('003001001').get_daily_challenge_coins()
# Ksjsb('003001001').sign_in()
# Ksjsb('003001001').shopping()
# Ksjsb('003001001').open_meal_allowance()
# Ksjsb('003001001').change_money()
# Ksjsb('003001001').get_double_bonus()
# Ksjsb('003001001').update_wealth()
