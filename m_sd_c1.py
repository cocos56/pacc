"""淘宝/拼多多全自动远程刷单程序入口C1模块"""
from pacc.project import SD
from pacc.config import Config

Config.set_debug(True)
SD.mainloop([
    '001001001',  # 陈晓航
    '001001002',  # 蒋山林
    '001001003',  # 陈嘉乐
    '001001004',  # 王德成
])
