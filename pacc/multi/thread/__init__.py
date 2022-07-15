"""多线程包的初始化模块"""
from .thread import runThreadsWithArgsList, runThreadsWithFunctions, threadLock, Thread

__all__ = [
    'runThreadsWithArgsList',
    'runThreadsWithFunctions',
    'threadLock',
    'Thread',
]
