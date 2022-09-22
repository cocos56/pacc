"""程序入口模块"""
# pylint: disable=unused-import
from datetime import datetime
from pacc.adb import ADB, UIAutomator
from pacc.base import print_err
from pacc.config import Config


Config.set_debug(True)
# print(False and not True or not False)
DEVICE_SN = '002005001'
adb_ins = ADB(DEVICE_SN)
# adb_ins.get_cpu_temperature()
# print(adb_ins.get_battery_temperature())
# adb_ins.get_current_focus()
uia_ins = UIAutomator(DEVICE_SN)
info = uia_ins.get_dict('app')['node'][2]['node'][2]['node'][0]['node']
i1 = info[3]['@text']
print(i1)
print(info[4]['@text'][1:-1])
# print(uia_ins.get_dict('withdrawDialog')['node']['node']['node'][3]['@text'])
# print(adb_ins.is_awake())
# uia_ins.click('com.jifen.qukan:id/a8w')
# uia_ins.click(naf='true', index='1', start_index=2)
# print(uia_ins.get_dict('android:id/button2', '等待'))
# uia_ins.click_by_screen_text('关闭')
# try:
#     uia_ins.get_current_ui_hierarchy()
# except FileNotFoundError as err:
#     print_err(err)
