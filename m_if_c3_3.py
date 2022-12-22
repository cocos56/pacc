"""咸鱼程序入口C3_3模块"""
# pylint: disable=unused-import
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish
from pacc.adb import LDConsole

Config.debug = True
Config.set_ld_work_path()
start_index, end_index = 1, 415
# IdleFish.check_version(start_index, end_index)
IdleFish.check(380, end_index, 1)
# IdleFish.check_even_devices(start_index, end_index)
# IdleFish.backups(start_index, end_index, 'D:/ldbks')
# LDConsole.quit(264)
