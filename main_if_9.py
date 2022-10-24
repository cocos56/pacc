"""雷电9_咸鱼程序入口模块"""
from pacc.adb.ld_console import LDConsole
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish

Config.set_ld_work_path(r'F:\leidian\LDPlayer9')
LDConsole.quit_all()
IdleFish.mainloop(1, 10)
