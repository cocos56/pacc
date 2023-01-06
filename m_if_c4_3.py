"""闲鱼程序入口C4_3模块"""
# pylint: disable=duplicate-code
from pacc.adb import LDConsole
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish

Config.debug = True
Config.set_ld_work_path()
start_index, end_index = 1, LDConsole.get_last_device_num()
print(f'start_index={start_index}, end_index={end_index}')
IdleFish.backups(start_index, end_index)
IdleFish.check_version(start_index, end_index)
IdleFish.update_ip(start_index, end_index)
