"""雷电5_咸鱼程序入口模块"""
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish
from pacc.adb.ld_console import LDConsole

Config.debug = True
Config.set_ld_work_path()
IdleFish(0)
LDConsole.quit_all()
IdleFish.mainloop(1, 5)
