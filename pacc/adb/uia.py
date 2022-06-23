"""UI自动化测试类"""
from collections import OrderedDict
from html import unescape
from os import system, remove
from os.path import exists

import xmltodict

from ..config import Config
from ..mysql import RetrieveBaseInfo
from ..tools import createDir, prettyXML, getXML, sleep, findAllNumsWithRe, average, getTextsFromPic


class Node:
    """节点类"""
    def __init__(self, resource_id='', text='', content_desc='', bounds='', class_='', index=''):
        self.resource_id = resource_id
        self.text = text
        self.content_desc = content_desc
        self.bounds = bounds
        self.class_ = class_
        self.index = index


class UIAutomator:
    def __init__(self, deviceSN):
        self.device = RetrieveBaseInfo(deviceSN)
        self.cmd = 'adb -s %s ' % self.device.IP
        self.node = Node()
        self.xml = ''
        self.txt = ''
        self.dicts = []

    def getScreen(self):
        pngPath = 'CurrentUIHierarchy/%s.png' % self.device.SN
        system(self.cmd + 'exec-out screencap -p > %s' % pngPath)
        return pngPath

    def tap(self, cP, interval=1):
        x, y = cP
        print('正在让%s点击(%d,%d)' % (self.device.SN, x, y))
        system(self.cmd + 'shell input tap %d %d' % (x, y))
        sleep(interval, Config.debug, Config.debug)

    def clickByScreenTexts(self, texts, txt=''):
        self.txt = txt
        for text in texts:
            if self.clickByScreenText(text, self.txt):
                return True

    def clickByScreenText(self, text, txt=''):
        cP = self.getCPByScreenText(text, txt)
        if cP:
            print('检测到【%s】' % text)
            self.tap(cP)
            return True
        else:
            print('未找到【%s】' % text)

    def getCPByScreenText(self, text, txt=''):
        if txt:
            self.txt = txt
        else:
            self.txt = getTextsFromPic(self.getScreen())
        li = []
        for t in self.txt:
            if text in t[1]:
                li = t[0]
                break
        if not len(li) == 4:
            return
        return self.getCPFromTPs(li[0] + li[2])

    @classmethod
    def getCPFromTPs(cls, li):
        x1, y1, x2, y2 = li
        x = average(x1, x2)
        y = average(y1, y2)
        return x, y

    def clickByXMLTexts(self, texts, xml=''):
        self.xml = xml
        for text in texts:
            if self.click(text=text, xml=self.xml):
                return True

    def click(self, resource_id='', text='', content_desc='', xml='', bounds='', class_='',
              offset_x=0, offset_y=0):
        cP = self.getCP(resource_id, text, content_desc, xml, bounds, class_)
        if cP and text:
            print('检测到【%s】' % text)
        if not cP:
            return False
        x, y = cP
        cP = x+offset_x, y+offset_y
        self.tap(cP)
        return True

    def clickByBounds(self, bounds):
        cP = self.getCPFromTPs(findAllNumsWithRe(bounds))
        self.tap(cP)

    def getCP(self, resource_id='', text='', content_desc='', xml='', bounds='', class_=''):
        bounds = self.getBounds(resource_id, text, content_desc, xml, bounds, class_)
        if not bounds:
            return False
        return self.getCPFromTPs(findAllNumsWithRe(bounds))

    def getBounds(self, resource_id, text='', content_desc='', xml='', bounds='', class_=''):
        dic = self.getDict(resource_id, text, content_desc, xml, bounds, class_)
        if dic:
            return dic['@bounds']
        return False

    def getDictByXMLTexts(self, texts, xml=''):
        self.xml = xml
        for text in texts:
            dic = self.getDict(text=text, xml=self.xml)
            if dic:
                return dic

    def getDict(self, resource_id='', text='', content_desc='', xml='', bounds='', class_='',
                index=''):
        self.node = Node(resource_id, text, content_desc, bounds, class_, index)
        if xml:
            self.xml = xml
        else:
            self.xml = self.getCurrentUIHierarchy()
        dic = self.depthFirstSearch(xmltodict.parse(self.xml))
        if dic:
            dic.update({'@text': unescape(dic['@text'])})
        return dic

    def getDicts(self, resource_id='', text='', content_desc='', xml='', bounds=''):
        self.dicts = []
        self.node = Node(resource_id, text, content_desc, bounds)
        if xml:
            self.xml = xml
        else:
            self.xml = self.getCurrentUIHierarchy()
        self.depthFirstSearchDicts(xmltodict.parse(self.xml))
        return self.dicts

    def isTargetNode(self, dic):
        if type(dic) in (str, list):
            return False
        if '@resource-id' not in dic.keys():
            return False
        if self.node.index:
            if self.node.index == dic['@index']:
                if self.node.class_ and dic['@class'] == self.node.class_:
                    if self.node.bounds and self.isTargetBounds(self.node.bounds, dic['@bounds']):
                        if dic['@resource-id'] == self.node.resource_id:
                            return True
            return False
        elif self.node.resource_id:
            if dic['@resource-id'] == self.node.resource_id:
                if self.node.text:
                    if self.node.text in unescape(dic['@text']):
                        return True
                    return False
                elif self.node.content_desc:
                    if unescape(dic['@content-desc']) == self.node.content_desc:
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
        elif self.node.content_desc:
            if self.node.content_desc in unescape(dic['@content-desc']):
                return True
            return False
        elif self.node.class_:
            if dic['@class'] == self.node.class_:
                return True
            return False
        return False

    @classmethod
    def isTargetBounds(cls, targetBounds, srcBounds):
        x1, y1, x2, y2 = findAllNumsWithRe(targetBounds)
        x3, y3, x4, y4 = findAllNumsWithRe(srcBounds)
        return x1 in (-1, x3) and y1 in (-1, y3) and x2 in (-1, x4) and y2 in (-1, y4)

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

    def depthFirstSearchDicts(self, dic):
        if type(dic) == OrderedDict:
            if self.isTargetNode(dic):
                self.dicts.append(dic)
            for i in dic.keys():
                if self.isTargetNode(dic[i]):
                    self.dicts.append(dic[i])
                res = self.depthFirstSearchDicts(dic[i])
                if res:
                    return res
        elif type(dic) == list:
            for i in dic:
                res = self.depthFirstSearchDicts(i)
                if res:
                    self.dicts.append(res)

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
