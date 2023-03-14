"""闲鱼程序入口C7_2模块"""
from pacc.adb import LDConsole
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish

Config.debug = True
Config.set_ld_work_path()
start_index, end_index = 1, LDConsole.get_last_device_num()
print(f'start_index={start_index}, end_index={end_index}')
# IdleFish.top_up_mobile(start_index, end_index)
# IdleFish.confirm(159, end_index)
IdleFish.check_after_run(start_index, 220)
# IdleFish.first_buy(start_index, end_index)
# IdleFish.create(end_index)
# IdleFish.login(start_index, end_index)
