"""雷电模拟器程序入口模块"""
from pacc.adb.ld_console import LDConsole
from pacc.config import Config

Config.set_ld_work_path()
# LDConsole.quit(83)
LDConsole.is_running(83)
res = LDConsole.is_running(100)
print(res)
print(1 + 1 >= 2)
