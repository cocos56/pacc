"""程序入口模块"""
# pylint: disable=unused-import
from pacc import get_version
from pacc.adb import ADB, UIAutomator
from pacc.base import print_err
from pacc.config import Config
from pacc.project.ksjsb.resource_id import ResourceID
from pacc.project.ksjsb.mainloop import KsjsbMainloop

# KsjsbMainloop.run()
# get_version()

Config.set_debug(True)
DEVICE_SN = '003001003'
adb_ins = ADB(DEVICE_SN)
uia_ins = UIAutomator(DEVICE_SN)
# uia_ins.click(ResourceID.retry_btn)
# uia_ins.get_texts_from_screen(True)
# adb_ins.get_cpu_temperature()
try:
    uia_ins.get_current_ui_hierarchy()
except FileNotFoundError as err:
    print_err(err)
