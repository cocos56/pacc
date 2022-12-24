"""雷电9_咸鱼程序入口模块"""
# pylint: disable=unused-import
from datetime import datetime

from pacc.adb import LDConsole
from pacc.adb.ld_base import LDBase
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish

Config.debug = True
Config.set_ld_work_path()
start_index, end_index = 1, 7
# LDConsole.quit(3)
# LDBase(3).timeout_monitoring(datetime.now())
IdleFish.backups(start_index, end_index)
# IdleFish.check_version(end_index, end_index, 1)
# IdleFish.check(start_index, end_index, 5)
# IdleFish.check_even_devices(101, end_index)
