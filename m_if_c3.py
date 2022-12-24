"""咸鱼程序入口C3_1模块"""
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish

Config.debug = True
Config.set_ld_work_path()
start_index, end_index = 1, 415
# IdleFish.check_version(start_index, end_index)
IdleFish.check(224, end_index)
# IdleFish.check_odd_devices(97, end_index)
IdleFish.mainloop(1, end_index, 5)
