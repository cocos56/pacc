"""统一计算中心（Unified Computing Center, UCC）服务器端程序入口"""
from pacc.config import Config
from pacc.network import UCCServer

Config.set_debug(True)
UCCServer.mainloop()
