"""
拼多多商家版程序入口
"""
from pacc.project import PDDSJB
from pacc.config import Config

Config.setDebug(True)
PDDSJB('002001002').mainloop()
