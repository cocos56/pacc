class NoxUIAutomator:
    def __init__(self):
        pass

    def getCurrentUIHierarchy(self, pretty=False):
        system(self.cmd + 'shell rm /sdcard/window_dump.xml')
        cmd = self.cmd + 'shell uiautomator dump /sdcard/window_dump.xml'
        if Config.debug:
            print(cmd)
        system(cmd)
        dirName = 'CurrentUIHierarchy'
        createDir(dirName)
        filePath = '%s/%s.xml' % (dirName, self.device.SN)
        print(filePath)
        if exists(filePath):
            remove(filePath)
        system('%spull /sdcard/window_dump.xml %s' % (self.cmd, filePath))
        if pretty:
            return prettyXML(filePath)
        return getXML(filePath)