"""程序入口模块"""
from pacc.adb import ADB, UIAutomator
from pacc.base import print_err
from pacc.config import Config
from pacc.tools import get_texts_from_pic

Config.set_debug(True)
DEVICE_SN = '003001002'
adb_ins = ADB(DEVICE_SN)
uia_ins = UIAutomator(DEVICE_SN)
# uia_ins.click('com.kuaishou.nebula:id/positive')
# uia_ins.click(text='领现金')
# adb_ins.swipe(500, 300, 500, 1700)
try:
    uia_ins.get_current_ui_hierarchy()
except FileNotFoundError as err:
    print_err(err)
    # txt = get_texts_from_pic(uia_ins.get_screen())
    # print(txt)
# adb_ins.swipe(500, 300, 500, 1700)
# adb_ins.swipe(500, 1530, 500, 500)
# EMail(DEVICE_SN).send_login_alarm()
