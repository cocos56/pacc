"""闲鱼程序入口C2_3模块"""
from pacc.config import Config
from pacc.project import IdleFish


Config.set_debug(True)
IdleFish('001023001').run_task()
