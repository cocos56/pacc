from ..multi import runThreadsWithArgsList, runThreadsWithFunctions
from ..tools import sleep
from .device import Device


class XM5(Device):
    def __init__(self, SN):
        super(XM5, self).__init__()

    def mainloopOneByOne(self):
        while True:
            self.hyIns.mainloop()
            sleep(600)

    @classmethod
    def mainloop(cls, devicesSN):
        runThreadsWithArgsList(cls, devicesSN)
        runThreadsWithFunctions([i.mainloopOneByOne for i in cls.instances])
