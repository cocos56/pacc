"""闲鱼程序入口C5_1模块"""
# pylint: disable=duplicate-code
from pacc.adb import LDConsole
from pacc.config import Config
from pacc.ld_proj import IdleFish

Config.debug = True
Config.set_ld_work_path()
start_index, end_index = 1, LDConsole.get_last_device_num()
print(f'start_index={start_index}, end_index={end_index}')
IdleFish.mainloop(start_index, end_index, 5, 220)
# IdleFish.create(end_index)
# IdleFish.login(start_index, end_index)
# IdleFish.first_buy(start_index, 121)
# IdleFish.second_buy(start_index, 194)
# IdleFish.confirm(255, end_index)
# IdleFish.buy(start_index, end_index)
