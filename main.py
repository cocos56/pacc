"""程序入口模块"""
from pacc.adb import ADB, UIAutomator
from pacc.config import Config

Config.setDebug(True)
device_sn = '001001001'
adb_ins = ADB(device_sn)
uia_ins = UIAutomator(device_sn)
