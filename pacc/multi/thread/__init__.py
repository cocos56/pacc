"""多线程包的初始化模块"""
from .thread import run_threads_with_args_list, run_threads_with_functions, threadLock, Thread

__all__ = [
    'run_threads_with_args_list',
    'run_threads_with_functions',
    'threadLock',
    'Thread',
]
