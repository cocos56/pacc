"""闲鱼程序入口自动上新模块"""
from os import listdir, remove
from os.path import join

from pacc.adb import LDConsole
from pacc.base import sleep
from pacc.config import Config
from pacc.ld_proj.idle_fish import IdleFish


def get_acs():
    """获取所有支付宝的代付码

    :return: 所有支付宝的代付码
    """
    ap_li = []
    for i in listdir(r'\\10.1.1.2\acs')[::-1]:
        spli = i.split('.')
        if spli and spli[-1] == 'txt':
            ap_li.append(i)
    return ap_li


Config.debug = True
Config.set_ld_work_path()
time_cnt = 0
while True:
    acs = get_acs()
    print(acs)
    if acs:
        start_index, end_index = 1, LDConsole.get_last_device_num()
        IdleFish.create(end_index)
        IdleFish.login(start_index, end_index)
        time_cnt = 0
        for i in acs:
            print(i)
            remove(join(r'\\10.1.1.2\acs', i))
        continue
    print(f'time_cnt={time_cnt}')
    sleep(1)
    time_cnt += 1
