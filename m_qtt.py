"""快手极速版程序入口模块"""
from pacc.config import Config
from pacc.project import Qtt

Config.set_debug(True)
Qtt('003001001').mainloop()
# Qtt('003001001').exit_stub_standard_portrait_activity()
# Qtt('003001001').enter_task_interface()
# Qtt('003001001').change_money()
# Qtt('003001001').exit_stub_standard_portrait_activity()
# Qtt('003001001').sign_in()
# Qtt('003001001').watch_detail(False)
# Qtt('003001001').exit_incite_ad_activity()
