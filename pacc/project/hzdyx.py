from .project import Project
from ..tools import sleep


class HZDYX(Project):
    """
    """
    scriptName = 'anze.nb.hzdyx/com.stardust.autojs.inrt.SplashActivity'
    programName = 'com.ruiqugames.chinesechar/com.ruiqugames.chinesechar.MainActivity'

    instances = []

    def __init__(self, deviceSN=0):
        if deviceSN:
            super(HZDYX, self).__init__(deviceSN)

    @classmethod
    def mainloop(cls):
        # cls.instances.append(HZDYX('201'))
        cls.instances.append(HZDYX('202'))
        while True:
            for i in cls.instances:
                if i.adbIns.rebootPerHour():
                    i.adbIns.start(cls.scriptName)
                    sleep(6)
                    if i.adbIns.device.Model == 'M2007J22C':
                        i.adbIns.tap(798, 2159)
                        i.adbIns.tap(287, 1492)
                    elif i.adbIns.device.Model == 'JAT-TL00':
                        i.adbIns.tap(161, 1084)
                if 'com.ruiqugames.chinesechar' not in i.adbIns.getCurrentFocus():
                    i.adbIns.start(cls.programName)
            sleep(1200)

