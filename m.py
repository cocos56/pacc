"""程序入口模块"""
# pylint: disable=unused-import
from pacc.adb import ADB, UIAutomator
from pacc.base import print_err
from pacc.config import Config


Config.set_debug(True)
DEVICE_SN = '003001001'
adb_ins = ADB(DEVICE_SN)
# adb_ins.get_app_list()
# adb_ins.press_app_switch_key()
uia_ins = UIAutomator(DEVICE_SN)
# uia_ins.click(text='重试', index='2')
# uia_ins.click_by_screen_text('关闭')
try:
    uia_ins.get_current_ui_hierarchy()
except FileNotFoundError as err:
    print_err(err)
