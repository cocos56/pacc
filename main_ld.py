"""雷电模拟器程序入口模块"""
from pacc.adb.ld_console import LDConsole
from pacc.config import Config

Config.set_ld_work_path()
# LDConsole.list()
r = LDConsole(1).is_exist()
print(r)
