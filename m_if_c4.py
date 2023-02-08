"""闲鱼程序入口C4_1模块"""
# pylint: disable=duplicate-code
from pacc.adb import LDConsole
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish

Config.debug = True
Config.set_ld_work_path()
start_index, end_index = 1, LDConsole.get_last_device_num()
print(f'start_index={start_index}, end_index={end_index}')
IdleFish.mainloop(start_index, end_index, 5, 210)
# IdleFish.first_buy(218, end_index)
# IdleFish.buy(246, 246)
