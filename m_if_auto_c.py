"""闲鱼程序入口自动上新模块"""
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish


Config.debug = True
Config.set_priority = True
Config.enable_being_open_num = False
Config.safety_verification_max_num = 15
Config.set_ld_work_path()
IdleFish.auto_create()
