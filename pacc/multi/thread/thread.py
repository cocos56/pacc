import threading
from ...tools import sleep

threadLock = threading.Lock()


class Thread:
    instances = []

    def __init__(self, function, args='', tag=''):
        self.function = function
        self.args = args
        self.tag = tag
        self.instances.append(self)

    def __del__(self):
        if self in self.instances:
            self.instances.remove(self)

    def runThread(self, delay=1):
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
