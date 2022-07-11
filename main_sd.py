"""淘宝/拼多多全自动远程刷单程序入口"""
from pacc.project import SD
from pacc.config import Config

Config.setDebug(True)
SD.mainloop([
    '001001001',
    '001001002',
    '001001003',
    '001001004',
    '001001005',
    '001001006',
    '001001007',
])
