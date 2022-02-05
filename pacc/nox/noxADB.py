import os
from pacc.tools import findAllWithRe, sleep


def getOnlineDevices():
    res = os.popen('adb devices').read()
    res = findAllWithRe(res, r'(127.0.0.1:.+)\tdevice')
    return res


class NoxADB:

    def __init__(self, ip):
        self.ip = ip

    def start(self, Activity, wait=True):
        cmd = 'shell am start '
        if wait:
            cmd += '-W '
        cmd = "adb -s %s %s%s" % (self.ip, cmd, Activity)
        os.system(cmd)
        print(cmd)

    def inputText(self, text):
        cmd = 'adb -s %s shell input text "%s"' % (self.ip, text)
        print(cmd)
        os.system(cmd)

    def pressBackKey(self, sleepTime=1):
        self.pressKey('KEYCODE_BACK', sleepTime)

    def pressKey(self, keycode, sleepTime=1):
        print('正在让%s按%s' % (self.ip, keycode))
        os.system('adb -s %s shell input keyevent %s' % (self.ip, keycode))
        sleep(sleepTime, False, False)

    def getCurrentFocus(self):
        cmd = 'adb -s %s shell dumpsys window | findstr mCurrentFocus' % self.ip
        r = os.popen(cmd).read()[2:-2]
        # print(cmd)
        # print(r)
        return r
