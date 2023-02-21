"""闲鱼程序入口C4_1模块"""
# pylint: disable=duplicate-code
from pacc.adb import LDConsole
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish

Config.debug = True
Config.set_ld_work_path()
start_index, end_index = 1, LDConsole.get_last_device_num()
print(f'start_index={start_index}, end_index={end_index}')
# IdleFish.mainloop(start_index, end_index, 5, 220)
IdleFish.second_buy(247, end_index)
# IdleFish.first_buy(263, end_index)
# IdleFish.confirm(start_index, 160)
# IdleFish.buy(246, 246)
# IdleFish.create(end_index)
# IdleFish.login(start_index, end_index)
