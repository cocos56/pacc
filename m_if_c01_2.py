"""闲鱼程序入口C01_2模块"""
from pacc.config import Config
from pacc.project import IdleFish


Config.set_debug(True)
IdleFish('003002001').pay()
