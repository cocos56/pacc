"""闲鱼程序入口C01_1模块"""
from pacc.config import Config
from pacc.project import IdleFish


Config.set_debug(True)
IdleFish('003001001').change_price()
# IdleFish('003001001').dispatch()
# IdleFish('003001001').rate()
