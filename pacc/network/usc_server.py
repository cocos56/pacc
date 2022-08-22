"""统一存储中心（Unified Storage Center, USC）服务器端模块"""
from enum import Enum


class ServerStatus(Enum):
    """服务器状态枚举类"""
    FREE = 'free'
    BUSY = 'busy'


# pylint: disable=too-few-public-methods
class USCServer:
    """统一存储中心服务器端类"""
