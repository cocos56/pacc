"""多路并发的初始化模块"""
from .thread import runThreadsWithArgsList, runThreadsWithFunctions, threadLock

__all__ = [
    'runThreadsWithArgsList',
    'runThreadsWithFunctions',
    'threadLock'
]
