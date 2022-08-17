"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Ksjsb

Config.set_debug(True)
Ksjsb('003002001').mainloop()
# Ksjsb('003002001').buy_things_with_coins()
# Ksjsb('003002001').sign_in()
# Ksjsb('003002001').exit_award_video_play_activity()
# Ksjsb('003002001').get_daily_challenge_coins()
# Ksjsb('003002001').open_meal_allowance()
