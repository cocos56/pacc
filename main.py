"""程序入口模块"""
from pacc.adb import ADB, UIAutomator
# pylint: disable=unused-import
from pacc.base import print_err
from pacc.config import Config
from pacc.project.ksjsb.resource_id import ResourceID

Config.set_debug(True)
DEVICE_SN = '003001002'
adb_ins = ADB(DEVICE_SN)
uia_ins = UIAutomator(DEVICE_SN)
# dic = uia_ins.get_dict('android:id/message')['@text']
# print(dic)
uia_ins.click(ResourceID.award_video_close_dialog_abandon_button)
# uia_ins.click(text='领现金')
# adb_ins.swipe(500, 300, 500, 1700)
# try:
#     uia_ins.get_current_ui_hierarchy()
# except FileNotFoundError as err:
#     print_err(err)
# adb_ins.swipe(500, 300, 500, 1700)
# adb_ins.swipe(500, 1530, 500, 500)
