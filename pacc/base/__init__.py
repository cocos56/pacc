"""基础包的初始化模块"""
from .decorator import run_forever
from .dt import show_datetime
from .print import print_err
from .sleep import sleep
from .ucc_client import UCCClient

__all__ = [
    'run_forever',
    'show_datetime',
    'print_err',
    'sleep',
    'UCCClient',
]
