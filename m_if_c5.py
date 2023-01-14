"""闲鱼程序入口C5_1模块"""
from pacc.adb import LDConsole
from pacc.config import Config
from pacc.ld_proj import IdleFish, IdleFish2

Config.debug = True
Config.set_ld_work_path()
start_index, end_index = 1, LDConsole.get_last_device_num()
print(f'start_index={start_index}, end_index={end_index}')
IdleFish.mainloop(start_index, end_index, 5)
IdleFish2.mainloop(start_index, end_index, 5)
