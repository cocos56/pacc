"""程序入口模块"""
from pacc.adb import ADB, UIAutomator
from pacc.config import Config

Config.setDebug(True)
DEVICE_SN = '001001005'
adb_ins = ADB(DEVICE_SN)
uia_ins = UIAutomator(DEVICE_SN)
uia_ins.get_current_ui_hierarchy()
