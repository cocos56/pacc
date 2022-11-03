"""配置模块"""
from enum import Enum
from os import chdir

LDC = 'ldconsole.exe '


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
    ld_work_path = r'F:\leidian\LDPlayer9'

    @classmethod
    def set_debug(cls, debug):
        """设置是否为调试状态

        :param debug: 调试状态标志
        """
        cls.debug = debug

    @classmethod
    def set_ld_work_path(cls, ld_work_path=r'F:\leidian\LDPlayer9'):
        """设置是否为调试状态

        :param ld_work_path: 雷电模拟器的工作路径
        """
        cls.ld_work_path = ld_work_path
        chdir(Config.ld_work_path)
