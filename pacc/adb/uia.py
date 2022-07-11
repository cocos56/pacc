"""UI自动化测试模块"""
from collections import OrderedDict
from html import unescape
from os import system, remove
from os.path import exists

import xmltodict

from ..config import Config
from ..mysql import RetrieveMobileInfo
from ..tools import create_dir, get_pretty_xml, get_xml, sleep, find_all_ints_with_re, average, \
    get_texts_from_pic


# pylint: disable=too-few-public-methods
class Node:
    """节点类"""

    # pylint: disable=too-many-arguments
    def __init__(self, resource_id='', text='', content_desc='', bounds='', class_='', index=''):
        self.resource_id = resource_id
        self.text = text
        self.content_desc = content_desc
        self.bounds = bounds
        self.class_ = class_
        self.index = index


class UIAutomator:
    """UI自动化测试类"""

    def __init__(self, device_sn):
        """构造函数

        :param device_sn: 设备编号
        """
        self.device = RetrieveMobileInfo(device_sn)
        self.cmd = f'adb -s {self.device.IP} '
        self.node = Node()
        self.xml = ''
        self.txt = ''
        self.dicts = []

    def get_screen(self):
        """获取屏幕（截屏）"""
        png_path = f'CurrentUIHierarchy/{self.device.sn}.png'
        system(f'{self.cmd}exec-out screencap -p > {png_path}')
        return png_path

    def tap(self, point, interval=1):
        """点击

        :param point: 点的x和y坐标
        :param interval: 停顿时间
        """
        x_coordinate, y_coordinate = point
        print(f'正在让{self.device.sn}点击({x_coordinate},{y_coordinate})')
        system(f'{self.cmd}shell input tap {x_coordinate} {y_coordinate}')
        sleep(interval, Config.debug, Config.debug)

    def click_by_screen_texts(self, texts, txt=''):
        """依次搜索并点击截屏上的多个文本

        :param texts: 多个文本
        :param txt: 截屏上的所有文本
        :return: 如果查找到一条文本，则立即点击并返回True，如果都没有找到，则返回False
        """
        self.txt = txt
        for text in texts:
            if self.click_by_screen_text(text, self.txt):
                return True
        return False

    def click_by_screen_text(self, text, txt=''):
        """搜索并点击截屏上的文本

        :param text: 待点击的文本
        :param txt: 截屏上的所有文本
        :return: 如果查找到文本，则立即点击并返回True，如果没有找到，则返回False
        """
        point = self.get_point_by_screen_text(text, txt)
        if point:
            print(f'检测到【{text}】')
            self.tap(point)
            return True
        print(f'未找到【{text}】')
        return False

    def get_point_by_screen_text(self, text, txt=''):
        """通过屏幕上的文字来获取坐标点

        :param text: 待点击的文本
        :param txt: 截屏上的所有文本及其坐标信息
        :return: 如果查找到该文本，则返回该文本的中心点，如果没有找到，则返回False
        """
        if txt:
            self.txt = txt
        else:
            self.txt = get_texts_from_pic(self.get_screen())
        points_list = []
        for temp_txt in self.txt:
            if text in temp_txt[1]:
                points_list = temp_txt[0]
                break
        if not len(points_list) == 4:
            return False
        return self.get_point_from_two_points(points_list[0] + points_list[2])

    @classmethod
    def get_point_from_two_points(cls, values_list):
        """从矩形对角的两点获取中心点的坐标

        :param values_list: 两点的坐标值构成的列表，应为：[x1, y1, x2, y2]
        :return: 中心点的坐标(x, y)
        """
        x1_value, y1_value, x2_value, y2_value = values_list
        x_coordinate = average(x1_value, x2_value)
        y_coordinate = average(y1_value, y2_value)
        return x_coordinate, y_coordinate

    def click_by_xml_texts(self, texts, xml=''):
        """通过用户界面上元素的层次布局信息里的文字来点击目标点

        :param texts: 多个目标文本构成的列表
        :param xml: 目标用户界面上元素的层次布局信息
        :return: 找到一个就立即点击并返回True，都未找到返回False
        """
        self.xml = xml
        for text in texts:
            if self.click(text=text, xml=self.xml):
                return True
        return False

    # pylint: disable=too-many-arguments
    def click(self, resource_id='', text='', content_desc='', xml='', bounds='', class_='',
              offset_x=0, offset_y=0):
        """点击目标点

        :param resource_id: 资源的ID
        :param text: 文本
        :param content_desc: 描述
        :param xml: 目标用户界面上元素的层次布局信息
        :param bounds: 边界值（位于目标矩形的斜对角的两点坐标）
        :param class_: 类名
        :param offset_x: x轴坐标的偏移量
        :param offset_y: y轴坐标的偏移量
        :return: 找到后立即点击并返回True，未找到返回False
        """
        point = self.get_point(resource_id, text, content_desc, xml, bounds, class_)
        if point and text:
            print(f'检测到【{text}】')
        if not point:
            return False
        x_coordinate, y_coordinate = point
        point = x_coordinate + offset_x, y_coordinate + offset_y
        self.tap(point)
        return True

    def click_by_bounds(self, bounds):
        """通过边界值来点击

        :param bounds: 边界值（位于目标矩形的斜对角的两点坐标）
        """
        point = self.get_point_from_two_points(find_all_ints_with_re(bounds))
        self.tap(point)

    def get_point(self, resource_id='', text='', content_desc='', xml='', bounds='', class_=''):
        bounds = self.get_bounds(resource_id, text, content_desc, xml, bounds, class_)
        if not bounds:
            return False
        return self.get_point_from_two_points(find_all_ints_with_re(bounds))

    def get_bounds(self, resource_id, text='', content_desc='', xml='', bounds='', class_=''):
        dic = self.get_dict(resource_id, text, content_desc, xml, bounds, class_)
        if dic:
            return dic['@bounds']
        return False

    def get_dict_by_xml_texts(self, texts, xml=''):
        self.xml = xml
        for text in texts:
            dic = self.get_dict(text=text, xml=self.xml)
            if dic:
                return dic

    def get_dict(self, resource_id='', text='', content_desc='', xml='', bounds='', class_='',
                 index=''):
        self.node = Node(resource_id, text, content_desc, bounds, class_, index)
        if xml:
            self.xml = xml
        else:
            self.xml = self.get_current_ui_hierarchy()
        dic = self.depth_first_search(xmltodict.parse(self.xml))
        if dic:
            dic.update({'@text': unescape(dic['@text'])})
        return dic

    def get_dicts(self, resource_id='', text='', content_desc='', xml='', bounds=''):
        self.dicts = []
        self.node = Node(resource_id, text, content_desc, bounds)
        if xml:
            self.xml = xml
        else:
            self.xml = self.get_current_ui_hierarchy()
        self.depth_first_search_dicts(xmltodict.parse(self.xml))
        return self.dicts

    def is_target_node(self, dic):
        if type(dic) in (str, list):
            return False
        if '@resource-id' not in dic.keys():
            return False
        if self.node.index:
            if self.node.index == dic['@index']:
                if self.node.class_ and dic['@class'] == self.node.class_:
                    if self.node.bounds and self.is_target_bounds(self.node.bounds, dic['@bounds']):
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
            if self.is_target_bounds(self.node.bounds, dic['@bounds']):
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
    def is_target_bounds(cls, targetBounds, srcBounds):
        x1, y1, x2, y2 = find_all_ints_with_re(targetBounds)
        x3, y3, x4, y4 = find_all_ints_with_re(srcBounds)
        return x1 in (-1, x3) and y1 in (-1, y3) and x2 in (-1, x4) and y2 in (-1, y4)

    def depth_first_search(self, dic):
        if type(dic) == dict:
            if self.is_target_node(dic):
                return dic
            for i in dic.keys():
                if self.is_target_node(dic[i]):
                    return dic[i]
                res = self.depth_first_search(dic[i])
                if res:
                    return res
        elif type(dic) == list:
            for i in dic:
                res = self.depth_first_search(i)
                if res:
                    return res

    def depth_first_search_dicts(self, dic):
        if type(dic) == OrderedDict:
            if self.is_target_node(dic):
                self.dicts.append(dic)
            for i in dic.keys():
                if self.is_target_node(dic[i]):
                    self.dicts.append(dic[i])
                res = self.depth_first_search_dicts(dic[i])
                if res:
                    return res
        elif type(dic) == list:
            for i in dic:
                res = self.depth_first_search_dicts(i)
                if res:
                    self.dicts.append(res)

    def get_current_ui_hierarchy(self):
        """获取当前的用户界面上的元素的层次布局信息"""
        system(f'{self.cmd}shell rm /sdcard/window_dump.xml')
        cmd = f'{self.cmd}shell uiautomator dump /sdcard/window_dump.xml'
        if Config.debug:
            print(cmd)
        system(cmd)
        dir_name = 'CurrentUIHierarchy'
        create_dir(dir_name)
        file_path = f'{dir_name}/{self.device.sn}.xml'
        print(file_path)
        if exists(file_path):
            remove(file_path)
        system(f'{self.cmd}pull /sdcard/window_dump.xml {file_path}')
        if Config.debug:
            return get_pretty_xml(file_path)
        return get_xml(file_path)
