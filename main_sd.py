"""淘宝/拼多多全自动远程刷单程序入口"""
from pacc.project import SD
from pacc.config import Config

Config.setDebug(True)
SD.mainloop(['001001001'])
