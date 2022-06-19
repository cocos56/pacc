"""
小米4程序入口
"""
from pacc.config import Config
from pacc.device import XM4


Config.setDebug(True)
XM4.mainloop([
    '003001001',
])
