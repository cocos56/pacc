"""真机设备工程包的初始化模块"""
from .ksjsb.ksjsb import Ksjsb
from .pdd_video import PddVideo
from .qtt import Qtt
from .sd import SD
from .idle_fish import IdleFish

__all__ = [
    'SD',
    'Ksjsb',
    'Qtt',
    'PddVideo',
    'IdleFish'
]
