"""多线程模块"""
import threading
from ...base import sleep

threadLock = threading.Lock()


class Thread:
    """多线程类"""
    instances = []

    def __init__(self, function, args=''):
        """构造函数：初始化多线程类的对象

        :param function: 函数
        :param args: 不定参数
        """
        self.function = function
        self.args = args
        self.instances.append(self)

    def __del__(self):
        """构造函数：销毁多线程类的对象"""
        if self in self.instances:
            self.instances.remove(self)

    def run_thread(self, delay=1):
        """运行线程

        :param delay: 延迟执行
        :return : 线程对象
        """
        sleep(delay, False, False)
        if self.args:
            thread = threading.Thread(target=self.function, args=self.args)
        else:
            thread = threading.Thread(target=self.function)
        thread.start()
        return thread

    # def runThreads(self):
    #     threads = []
    #     for args in argsList:
    #         t = runThread(function, (args,))
    #         threads.append(t)
    #     for t in threads:
    #         t.join()


def run_thread(function, args=(), delay=1):
    """开启一个线程

    :param function: 方法
    :param args: 不定参数
    :param delay: 延迟执行时间（秒）
    :return : 线程对象
    """
    sleep(delay, False, False)
    if args:
        thread = threading.Thread(target=function, args=args)
    else:
        thread = threading.Thread(target=function)
    thread.start()
    return thread


def run_threads_with_args_list(function, args_list):
    """使用多个不定参数构成的列表开启多个线程

    :param function: 方法
    :param args_list: 不定参数构成的列表
    """
    threads = []
    for args in args_list:
        thread = run_thread(function, (args,))
        threads.append(thread)
    for thread in threads:
        thread.join()


def run_threads_with_functions(functions, timeout=None):
    """使用多个函数构成的列表开启多个线程

    :param functions: 多个函数构成的列表
    :param timeout: 延迟执行时间（秒）
    """
    threads = []

    for function in functions:
        thread = run_thread(function)
        threads.append(thread)
    for thread in threads:
        thread.join(timeout)
