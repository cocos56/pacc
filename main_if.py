"""咸鱼程序入口模块"""
from pacc.ld_proj.idle_fish import IdleFish
from pacc.adb.ld_console import LDConsole

IdleFish(0)
LDConsole.quit_all()
IdleFish.mainloop(1, 64)
