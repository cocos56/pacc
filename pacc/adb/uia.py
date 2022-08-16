"""UI自动化测试模块"""
from html import unescape
from os import system, remove
from os.path import exists

import xmltodict

from ..base import sleep, UCCClient, print_err
from ..config import Config
from ..mysql import RetrieveMobileInfo
from ..tools import create_dir, get_pretty_xml, get_xml, find_all_ints_with_re, average


# pylint: disable=too-few-public-methods
class Node:
    """节点类"""
    # pylint: disable=too-many-arguments
    def __init__(self, resource_id='', text='', content_desc='', bounds='', class_='', index=''):
        """构造函数

        :param resource_id: 资源的ID
        :param text: 文本
        :param content_desc: 描述
        :param bounds: 边界值（位于目标矩形的斜对角的两点坐标）
        :param class_: 类名
        :param index: 索引值
        """
        self.resource_id = resource_id
        self.text = text
        self.content_desc = content_desc
        self.bounds = bounds
        self.class_ = class_
        self.index = index


# pylint: disable=too-many-public-methods
class UIAutomator:
    """UI自动化测试类"""

    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备编号
        """
        self.dbr = RetrieveMobileInfo.get_ins(serial_num)
        self.cmd = f'adb -s {self.dbr.ipv4_addr} '
        self.node = Node()
        self.xml = ''
        self.txt = ''
        self.dicts = []

    def get_screen(self):
        """获取屏幕（截屏）"""
        png_path = f'CurrentUIHierarchy/{self.dbr.serial_num}.png'
        system(f'{self.cmd}exec-out screencap -p > {png_path}')
        return png_path

    def tap(self, point, interval=1):
        """点击

        :param point: 点的x和y坐标
        :param interval: 停顿时间
        """
        x_coordinate, y_coordinate = point
        print(f'正在让{self.dbr.serial_num}点击({x_coordinate},{y_coordinate})')
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

    def click_by_screen_text(self, text, txt='', start_index=0):
        """搜索并点击截屏上的文本

        :param text: 待点击的文本
        :param txt: 截屏上的所有文本
        :param start_index: 多个匹配项符合条件时目标项的索引值
        :return: 如果查找到文本，则立即点击并返回True，如果没有找到，则返回False
        """
        point = self.get_point_by_screen_text(text, txt, start_index)
        if point:
            self.tap(point)
            return True
        return False

    def get_texts_from_screen(self, show_all_texts=False):
        """从当前屏幕截图中获取所有文字"""
        self.txt = UCCClient.send(self.dbr.serial_num)
        if show_all_texts:
            print(self.txt)
        return self.txt

    def get_point_by_screen_text(self, text, txt='', start_index=0):
        """通过屏幕上的文字来获取坐标点

        :param text: 待点击的文本
        :param txt: 截屏上的所有文本及其坐标信息
        :param start_index: 多个匹配项符合条件时目标项的索引值
        :return: 如果查找到该文本，则返回该文本的中心点，如果没有找到，则返回False
        """
        if txt:
            self.txt = txt
        else:
            self.get_texts_from_screen()
        points_list = []
        count = 0
        for temp_txt in self.txt:
            if text in temp_txt[1]:
                if count == start_index:
                    points_list = temp_txt[0]
                    break
                count += 1
        if not len(points_list) == 4:
            print(f'未找到【{text}】')
            return False
        print(f'检测到【{text}】')
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
    def click(
            self, resource_id='', text='', content_desc='', xml='', bounds='', class_='', index='',
            offset_x=0, offset_y=0):
        """点击目标点

        :param resource_id: 资源的ID
        :param text: 文本
        :param content_desc: 描述
        :param xml: 目标用户界面上元素的层次布局信息
        :param bounds: 边界值（位于目标矩形的斜对角的两点坐标）
        :param class_: 类名
        :param index: 索引值
        :param offset_x: x轴坐标的偏移量
        :param offset_y: y轴坐标的偏移量
        :return: 找到后立即点击并返回True，未找到返回False
        """
        point = self.get_point(resource_id, text, content_desc, xml, bounds, class_, index)
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

    def get_point(
            self, resource_id='', text='', content_desc='', xml='', bounds='', class_='', index=''):
        """获取目标点的坐标

        :param resource_id: 资源的ID
        :param text: 文本
        :param content_desc: 描述
        :param xml: 目标用户界面上元素的层次布局信息
        :param bounds: 边界值（位于目标矩形的斜对角的两点坐标）
        :param class_: 类名
        :param index: 索引值
        :return: 找到后返回目标点的坐标，未找到返回False
        """
        bounds = self.get_bounds(resource_id, text, content_desc, xml, bounds, class_, index)
        if not bounds:
            return False
        return self.get_point_from_two_points(find_all_ints_with_re(bounds))

    def get_bounds(
            self, resource_id, text='', content_desc='', xml='', bounds='', class_='', index=''):
        """获取目标点所在的边界的斜对角两点的坐标

        :param resource_id: 资源的ID
        :param text: 文本
        :param content_desc: 描述
        :param xml: 目标用户界面上元素的层次布局信息
        :param bounds: 边界值（位于目标矩形的斜对角的两点坐标）
        :param class_: 类名
        :param index: 索引值
        :return: 找到后返回目边界的斜对角两点的坐标，未找到返回False
        """
        dic = self.get_dict(resource_id, text, content_desc, xml, bounds, class_, index)
        if dic:
            return dic['@bounds']
        return False

    def get_dict_by_xml_texts(self, texts, xml=''):
        """从层次布局信息中获取texts中某个text的字典信息

        :param texts: 由多个待搜索的文本构成的列表
        :param xml: 目标用户界面上元素的层次布局信息
        :return: 遍历文本列表，若找到一个符合条件的文本立即返回其所在的字典信息，遍历后均未找到返回False
        """
        self.xml = xml
        for text in texts:
            dic = self.get_dict(text=text, xml=self.xml)
            if dic:
                return dic
        return False

    def get_dict(
            self, resource_id='', text='', content_desc='', xml='', bounds='', class_='', index=''):
        """获取目标对象的字典信息

        :param resource_id: 资源的ID
        :param text: 文本
        :param content_desc: 描述
        :param xml: 目标用户界面上元素的层次布局信息
        :param bounds: 边界值（位于目标矩形的斜对角的两点坐标）
        :param class_: 类名
        :param index: 索引值
        :return: 返回通过深度优先方式获取到的字典信息（若找不到目标则返回的字典信息的值为False）
        """
        self.node = Node(resource_id, text, content_desc, bounds, class_, index)
        if xml:
            self.xml = xml
        else:
            self.xml = self.get_current_ui_hierarchy()
        dic = self.depth_first_search(xmltodict.parse(self.xml))
        if dic:
            dic.update({'@text': unescape(dic['@text'])})
        if text:
            if dic:
                print(f'检测到【{text}】')
            else:
                print(f'未找到【{text}】')
        elif resource_id:
            if dic:
                print(f'检测到【{resource_id}】')
            else:
                print(f'未找到【{resource_id}】')
        return dic

    def get_dicts(self, resource_id='', text='', content_desc='', xml='', bounds=''):
        """获取符合目标对象特征的多个字典信息

        :param resource_id: 资源的ID
        :param text: 文本
        :param content_desc: 描述
        :param xml: 目标用户界面上元素的层次布局信息
        :param bounds: 边界值（位于目标矩形的斜对角的两点坐标）
        :return: 返回通过深度优先方式获取到的所有字典信息（若找不到目标则返回的字典信息列表的值为[]）
        """
        self.dicts = []
        self.node = Node(resource_id, text, content_desc, bounds)
        if xml:
            self.xml = xml
        else:
            self.xml = self.get_current_ui_hierarchy()
        self.depth_first_search_dicts(xmltodict.parse(self.xml))
        return self.dicts

    # pylint: disable=too-many-return-statements,too-many-branches
    def is_target_node(self, dic):
        """通过字典信息判断是否是目标点

        :param dic: 待比对点的字典信息
        :return: 比对成功返回True，否则返回False
        """
        if type(dic) in (str, list):
            return False
        if '@resource-id' not in dic.keys():
            return False
        if self.node.index:
            if self.node.index == dic['@index']:
                if self.node.text and self.node.text in unescape(dic['@text']):
                    return True
                if self.node.class_ and dic['@class'] == self.node.class_:
                    if self.node.bounds and self.is_target_bounds(self.node.bounds, dic['@bounds']):
                        if dic['@resource-id'] == self.node.resource_id:
                            return True
            return False
        if self.node.resource_id:
            if dic['@resource-id'] == self.node.resource_id:
                if self.node.text:
                    if self.node.text in unescape(dic['@text']):
                        return True
                    return False
                if self.node.content_desc:
                    if unescape(dic['@content-desc']) == self.node.content_desc:
                        return True
                    return False
                return True
        if self.node.text:
            if self.node.text in unescape(dic['@text']):
                return True
            return False
        if self.node.bounds:
            if self.is_target_bounds(self.node.bounds, dic['@bounds']):
                return True
            return False
        if self.node.content_desc:
            if self.node.content_desc in unescape(dic['@content-desc']):
                return True
            return False
        if self.node.class_:
            if dic['@class'] == self.node.class_:
                return True
            return False
        return False

    @classmethod
    def is_target_bounds(cls, target_bounds, src_bounds):
        """判断源边界是否是目标边界

        :param target_bounds: 源边界
        :param src_bounds: 目标边界
        :return: 比对成功返回True，否则返回False
        """
        # pylint: disable=unbalanced-tuple-unpacking
        x1_value, y1_value, x2_value, y2_value = find_all_ints_with_re(target_bounds)
        x3_value, y3_value, x4_value, y4_value = find_all_ints_with_re(src_bounds)
        return x1_value in (-1, x3_value) and y1_value in (-1, y3_value) and x2_value in (
            -1, x4_value) and y2_value in (-1, y4_value)

    def depth_first_search(self, dic):
        """通过深度优先来搜索目标对象

        :param dic: 待搜索对象的字典信息
        :return: 搜索到返回目标对象，否则返回False
        """
        if isinstance(dic, dict):
            if self.is_target_node(dic):
                return dic
            for i in dic.keys():
                if self.is_target_node(dic[i]):
                    return dic[i]
                res = self.depth_first_search(dic[i])
                if res:
                    return res
        elif isinstance(dic, list):
            for i in dic:
                res = self.depth_first_search(i)
                if res:
                    return res
        return False

    def depth_first_search_dicts(self, dic):
        """通过深度优先来搜索目标字典所对应的对象

        :param dic: 待搜索对象的字典信息
        :return: 若搜索到，返回第一个匹配到的对象，否则返回False
        """
        if isinstance(dic, dict):
            if self.is_target_node(dic):
                self.dicts.append(dic)
            for i in dic.keys():
                if self.is_target_node(dic[i]):
                    self.dicts.append(dic[i])
                res = self.depth_first_search_dicts(dic[i])
                if res:
                    return res
        elif isinstance(dic, list):
            for i in dic:
                res = self.depth_first_search_dicts(i)
                if res:
                    self.dicts.append(res)
        return False

    def get_current_ui_hierarchy(self):
        """获取当前用户界面上元素的层次布局信息

        :return: 正常情况下会返回当前的用户界面上的元素的层次布局信息所构成的xml字符串，如果遇到异常则不做处理直接传递
        """
        system(f'{self.cmd}shell rm /sdcard/window_dump.xml')
        cmd = f'{self.cmd}shell uiautomator dump /sdcard/window_dump.xml'
        if Config.debug:
            print(cmd)
        system(cmd)
        dir_name = 'CurrentUIHierarchy'
        create_dir(dir_name)
        file_path = f'{dir_name}/{self.dbr.serial_num}.xml'
        print(file_path)
        if exists(file_path):
            remove(file_path)
        system(f'{self.cmd}pull /sdcard/window_dump.xml {file_path}')
        if Config.debug:
            return get_pretty_xml(file_path)
        return get_xml(file_path)

    def secure_get_current_ui_hierarchy(self):
        """安全地获取当前的用户界面上的元素的层次布局信息

        :return: 正常情况下会返回当前的用户界面上的元素的层次布局信息所构成的xml字符串，
                如果遇到异常则会捕捉处理并返回False
        """
        try:
            return self.get_current_ui_hierarchy()
        except FileNotFoundError as err:
            print_err(f'is_loading {err}')
            return False
