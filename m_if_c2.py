"""闲鱼程序入口C2_1模块"""
from pacc.config import Config
from pacc.project import IdleFish


Config.set_debug(True)
END_NUM = 9
IdleFish('002005001').change_price(END_NUM)
IdleFish('002005001').dispatch()
# IdleFish('002005001').rate()
# IdleFish('002005001').delete_error_rate_order()
