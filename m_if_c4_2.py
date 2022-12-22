"""雷电9_咸鱼程序入口模块"""
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish
from pacc.adb import LDConsole

Config.debug = True
Config.set_ld_work_path()
start_index, end_index = 1, 176
LDConsole.quit(51, force_exe=True)
# IdleFish.backups(start_index, end_index)
# IdleFish.check_version(start_index, end_index)
# IdleFish.check(start_index, end_index, 5)
# IdleFish.check_even_devices(101, end_index)
