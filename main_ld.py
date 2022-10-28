"""雷电模拟器程序入口模块"""
from pacc.adb.ld_console import LDConsole
from pacc.config import Config
from pacc.ld_proj.ld_proj import LDProj

Config.set_ld_work_path(r'F:\leidian\LDPlayer9')
LDProj().get_status()
# LDConsole.quit(83)
LDConsole.is_running(83)
res = LDConsole.is_running(100)
print(res)
