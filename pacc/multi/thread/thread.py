"""多线程模块"""
import threading
from ...tools import sleep

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
            t = threading.Thread(target=self.function, args=self.args)
        else:
            t = threading.Thread(target=self.function)
        t.start()
        return t

    # def runThreads(self):
    #     threads = []
    #     for args in argsList:
    #         t = runThread(function, (args,))
    #         threads.append(t)
    #     for t in threads:
    #         t.join()


def runThreadsWithFunctions(functions, timeout=None):
    threads = []

    for function in functions:
        t = runThread(function)
        threads.append(t)
    for t in threads:
        t.join(timeout)


def runThreadsWithArgsList(function, argsList):
    threads = []
    for args in argsList:
        t = runThread(function, (args,))
        threads.append(t)
    for t in threads:
        t.join()


def runThread(function, args=(), delay=1):
    sleep(delay, False, False)
    if args:
        t = threading.Thread(target=function, args=args)
    else:
        t = threading.Thread(target=function)
    t.start()
    return t
