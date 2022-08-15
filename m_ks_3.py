"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Ksjsb

Config.set_debug(True)
# Ksjsb('003001003').mainloop()
Ksjsb('003001003').get_double_bonus()
# Ksjsb('003001003').adb_ins.keep_online()
# Ksjsb('003001003').open_meal_allowance()
# Ksjsb('003001003').get_daily_challenge_coins()
# Ksjsb('003001003').change_money()
