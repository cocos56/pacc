"""雷电9_咸鱼程序入口模块"""
# pylint: disable=unused-import
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish
from pacc.adb import LDConsole

Config.debug = True
Config.set_ld_work_path()
start_index, end_index = 1, LDConsole.get_last_device_num()
print(f'start_index={start_index}, end_index={end_index}')
# LDConsole.quit(97)
# IdleFish.backups(start_index, end_index)
IdleFish.check_version(start_index, end_index)
# IdleFish.check(start_index, end_index, 3)
# IdleFish.check_even_devices(159, end_index)
