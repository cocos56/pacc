"""雷电9_咸鱼程序入口模块"""
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish

Config.debug = True
Config.set_ld_work_path()
start_index, end_index = 130, 405
# IdleFish.check_version(start_index, end_index)
IdleFish.check(start_index, end_index)
IdleFish.mainloop(1, end_index, 5)
