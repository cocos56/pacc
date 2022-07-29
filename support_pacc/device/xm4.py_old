from ..multi import runThreadsWithArgsList, runThreadsWithFunctions
from ..project import KSJSB, DYJSB
from ..tools import sleep
from .device import Device


class XM4(Device):
    def __init__(self, SN):
        super(XM4, self).__init__()
        self.ksjsbIns = KSJSB(SN)
        self.dyjsbIns = DYJSB(SN)

    def mainloopOneByOne(self):
        while True:
            self.ksjsbIns.mainloop()
            self.dyjsbIns.mainloop()
            sleep(1200)

    @classmethod
    def mainloop(cls, devicesSN):
        runThreadsWithArgsList(cls, devicesSN)
        runThreadsWithFunctions([i.mainloopOneByOne for i in cls.instances])
