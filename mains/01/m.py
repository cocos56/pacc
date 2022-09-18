"""程序入口模块"""
from pacc import get_version
from pacc.config import Config
from pacc.adb import ADB

get_version()
Config.set_debug(True)
DEVICE_SN = '001022001'
adb_ins = ADB(DEVICE_SN)
