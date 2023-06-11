"""配置模块"""
from enum import Enum
from os import chdir, getenv

LDC = 'ldconsole.exe '


class UnitPrice:
    """闲鱼币单价类"""
    base = 1.0
    middle = 0.5
    base_mid = base + middle

    @classmethod
    def get_base_mid_money(cls, base_mid_coins):
        """获取中基层鱼币所对应的的钱数

        :param base_mid_coins: 中基层的鱼币
        :return: 中基层鱼币所对应的的钱数
        """
        return base_mid_coins // 10000 * cls.base_mid

    @classmethod
    def get_base_money(cls, base_coins):
        """获取基层鱼币所对应的的钱数

        :param base_coins: 基层的鱼币
        :return: 基层鱼币所对应的的钱数
        """
        return base_coins // 10000 * cls.base

    @classmethod
    def get_middle_money(cls, middle_coins):
        """获取中层鱼币所对应的的钱数

        :param middle_coins: 中层的鱼币
        :return: 中层鱼币所对应的的钱数
        """
        return middle_coins // 10000 * cls.middle


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
    set_priority = False
    enable_being_open_num = True
    safety_verification_max_num = 1
    server_host = getenv('MySQL_Host')
    mysql_pw = getenv('MySQL_PW')
    aps_path = r'D:\if\aps'
    aps_network_path = fr'\\{server_host}\if\aps'
    ld_work_path = r'F:\leidian\LDPlayer9'

    @classmethod
    def set_debug(cls, debug: bool) -> None:
        """设置是否为调试状态

        :param debug: 调试状态标志
        """
        cls.debug = debug

    @classmethod
    def set_ld_work_path(cls, ld_work_path=r'F:\leidian\LDPlayer9') -> None:
        """设置雷电工作目录

        :param ld_work_path: 雷电模拟器的工作路径
        """
        cls.ld_work_path = ld_work_path
        chdir(cls.ld_work_path)
