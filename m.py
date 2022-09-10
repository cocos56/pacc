"""程序入口模块"""
# pylint: disable=unused-import
from datetime import datetime
from pacc.adb import ADB, UIAutomator
from pacc.base import print_err
from pacc.config import Config


Config.set_debug(True)
DEVICE_SN = '002002002'
adb_ins = ADB(DEVICE_SN)
# adb_ins.get_cpu_temperature()
# print(adb_ins.get_battery_temperature())
# adb_ins.get_current_focus()
uia_ins = UIAutomator(DEVICE_SN)
# print(adb_ins.is_awake())
# uia_ins.click(naf='true', index='2')
# uia_ins.click(naf='true', index='1', start_index=2)
print(uia_ins.get_dict(index='0', text='极速到账'))
# uia_ins.click_by_screen_text('关闭')
try:
    uia_ins.get_current_ui_hierarchy()
except FileNotFoundError as err:
    print_err(err)
