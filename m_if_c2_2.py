"""闲鱼程序入口C2_2模块"""
from pacc.config import Config
from pacc.project import IdleFish


Config.set_debug(True)
IdleFish('001011001').pay()
