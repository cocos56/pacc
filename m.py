"""程序入口模块"""
# pylint: disable=unused-import
from datetime import datetime
from pacc.adb import ADB, UIAutomator
from pacc.base import print_err
from pacc.config import Config


Config.set_debug(True)
# print(False and not True or not False)
DEVICE_SN = '002004001'
adb_ins = ADB(DEVICE_SN)
uia_ins = UIAutomator(DEVICE_SN)
# uia_ins.click('com.jifen.qukan:id/a98')
# uia_ins.click(naf='true', index='1', start_index=2)
# print(uia_ins.get_dict('android:id/button2', '等待'))
# uia_ins.click_by_screen_text('关闭')
try:
    uia_ins.get_current_ui_hierarchy()
except FileNotFoundError as err:
    print_err(err)
