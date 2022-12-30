"""闲鱼程序入口C5_3模块"""
from pacc.adb import LDConsole
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish
from pacc import MySQLDump

Config.debug = True
Config.set_ld_work_path()
start_index, end_index = 1, LDConsole.get_last_device_num()
print(f'start_index={start_index}, end_index={end_index}')
IdleFish.backups(start_index, end_index)
MySQLDump.start()
# IdleFish.check_version(start_index, end_index, 5)
