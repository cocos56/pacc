"""基础包的初始化模块"""
from .client import UCCClient
from .decorator import run_forever
from .dt import show_datetime
from .print import print_err
from .sleep import sleep

__all__ = [
    'UCCClient',
    'run_forever',
    'sleep',
    'print_err',
    'show_datetime',
]
