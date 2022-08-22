"""配置模块"""
from enum import Enum


class Language(Enum):
    """语言枚举类"""
    CH = 'Chinese'
    EN = 'English'


class ServerStatus(Enum):
    """服务器状态枚举类"""
    FREE = 'Free'
    BUSY = 'Busy'


# pylint: disable=too-few-public-methods
class Config:
    """配置类"""
    debug = False

    @classmethod
    def set_debug(cls, debug):
        """设置是否为调试状态

        :param debug: 调试状态标志
        """
        cls.debug = debug
