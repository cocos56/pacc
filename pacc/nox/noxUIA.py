import xmltodict
from html import unescape
from collections import OrderedDict
import os
from pacc.tools import createDir, prettyXML, sleep, findAllNumsWithRe, average


class Node:
    def __init__(self, resourceID='', text='', contentDesc='', bounds='', Class='', index=''):
        self.resourceID = resourceID
        self.text = text
        self.contentDesc = contentDesc
        self.bounds = bounds
        self.Class = Class
        self.index = index


class NoxUIAutomator:

    def __init__(self, ip):
        self.ip = ip
        self.node = Node()
        self.xml = ''

    def getScreen(self):
        pngPath = 'CurrentUIHierarchy/%s.png' % self.ip.replace('127.0.0.1:', '')
        os.system('adb -s %s exec-out screencap -p > %s' % (self.ip, pngPath))
        return pngPath

    @classmethod
    def isTargetBounds(cls, targetBounds, srcBounds):
        x1, y1, x2, y2 = findAllNumsWithRe(targetBounds)
        x3, y3, x4, y4 = findAllNumsWithRe(srcBounds)
        return x1 in (-1, x3) and y1 in (-1, y3) and x2 in (-1, x4) and y2 in (-1, y4)

    def isTargetNode(self, dic):
        if type(dic) in (str, list):
            return False
        if '@resource-id' not in dic.keys():
            return False
        if self.node.index:
            if self.node.index == dic['@index']:
                if self.node.Class and dic['@class'] == self.node.Class:
                    if self.node.bounds and self.isTargetBounds(self.node.bounds, dic['@bounds']):
                        if dic['@resource-id'] == self.node.resourceID:
                            return True
            return False
        elif self.node.resourceID:
            if dic['@resource-id'] == self.node.resourceID:
                if self.node.text:
                    if self.node.text in unescape(dic['@text']):
                        return True
                    return False
                elif self.node.contentDesc:
                    if unescape(dic['@content-desc']) == self.node.contentDesc:
                        return True
                    return False
                return True
        elif self.node.text:
            if self.node.text in unescape(dic['@text']):
                return True
            return False
        elif self.node.bounds:
            if self.isTargetBounds(self.node.bounds, dic['@bounds']):
                return True
            return False
        elif self.node.contentDesc:
            if self.node.contentDesc in unescape(dic['@content-desc']):
                return True
            return False
        elif self.node.Class:
            if dic['@class'] == self.node.Class:
                return True
            return False
        return False

    def depthFirstSearch(self, dic):
        if type(dic) == OrderedDict:
            if self.isTargetNode(dic):
                return dic
            for i in dic.keys():
                if self.isTargetNode(dic[i]):
                    return dic[i]
                res = self.depthFirstSearch(dic[i])
                if res:
                    return res
        elif type(dic) == list:
            for i in dic:
                res = self.depthFirstSearch(i)
                if res:
                    return res

    def getDict(self, resourceID='', text='', contentDesc='', xml='', bounds='', Class='', index=''):
        self.node = Node(resourceID, text, contentDesc, bounds, Class, index)
        if xml:
            self.xml = xml
        else:
            self.xml = self.getCurrentUIHierarchy()
        dic = self.depthFirstSearch(xmltodict.parse(self.xml))
        if dic:
            dic.update({'@text': unescape(dic['@text'])})
        return dic

    def getBounds(self, resourceID, text='', contentDesc='', xml='', bounds='', Class=''):
        dic = self.getDict(resourceID, text, contentDesc, xml, bounds, Class)
        if dic:
            return dic['@bounds']
        return False

    @classmethod
    def getCPFromTPs(cls, li):
        x1, y1, x2, y2 = li
        x = average(x1, x2)
        y = average(y1, y2)
        return x, y

    def getCP(self, resourceID='', text='', contentDesc='', xml='', bounds='', Class=''):
        bounds = self.getBounds(resourceID, text, contentDesc, xml, bounds, Class)
        if not bounds:
            return False
        return self.getCPFromTPs(findAllNumsWithRe(bounds))

    def tap(self, cP, interval=1):
        x, y = cP
        print('正在让%s点击(%d,%d)' % (self.ip, x, y))
        os.system('adb -s %s shell input tap %d %d' % (self.ip, x, y))
        sleep(interval, False, False)

    def click(self, resourceID='', text='', contentDesc='', xml='', bounds='', Class='',
              offset_x=0, offset_y=0, interval=1):
        cP = self.getCP(resourceID, text, contentDesc, xml, bounds, Class)
        if cP and text:
            print('检测到【%s】' % text)
        if contentDesc:
            if cP:
                print('检测到【%s】' % contentDesc)
            else:
                print('未发现【%s】' % contentDesc)
        if not cP:
            return False
        x, y = cP
        cP = x+offset_x, y+offset_y
        self.tap(cP, interval)
        return True

    def getCurrentUIHierarchy(self):
        os.system('adb -s %s shell rm /sdcard/window_dump.xml' % self.ip)
        cmd = 'adb -s %s shell uiautomator dump /sdcard/window_dump.xml' % self.ip
        # print(cmd)
        os.system(cmd)
        dirName = 'CurrentUIHierarchy'
        createDir(dirName)
        filePath = '%s/%s.xml' % (dirName, self.ip.replace('127.0.0.1:', ''))
        print(filePath)
        if os.path.exists(filePath):
            os.remove(filePath)
        os.system('adb -s %s pull /sdcard/window_dump.xml %s' % (self.ip, filePath))
        return prettyXML(filePath)
