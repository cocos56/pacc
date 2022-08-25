"""程序入口模块"""
# pylint: disable=unused-import
from pacc.adb import ADB, UIAutomator
from pacc.base import print_err
from pacc.config import Config


Config.set_debug(True)
DEVICE_SN = '002004003'
adb_ins = ADB(DEVICE_SN)
uia_ins = UIAutomator(DEVICE_SN)
# uia_ins.click(text='看视频再领')
try:
    uia_ins.get_current_ui_hierarchy()
except FileNotFoundError as err:
    print_err(err)
