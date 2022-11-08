"""雷电自动化测试模块"""
from html import unescape
from os import remove
from os.path import exists

import xmltodict

from .ld_base import LDBase
from .uia import Node
from ..base import sleep
from ..config import Config
from ..tools import create_dir, get_pretty_xml, get_xml, find_all_ints_with_re


class LDUIA(LDBase):
    """雷电模拟器UI自动化测试类"""
    def __init__(self, ld_index):
        """构造函数

       :param ld_index: 雷电模拟器的索引
        """
        super().__init__(ld_index)
        self.node = Node()
        self.xml = ''

    def tap(self, point, interval=1):
        """点击

        :param point: 点的x和y坐标
        :param interval: 停顿时间
        """
        x_coordinate, y_coordinate = point
        print(f'正在让编号为{self.ld_index}的模拟器点击({x_coordinate},{y_coordinate})')
        self.exe_cmd(f'shell input tap {x_coordinate} {y_coordinate}')
        sleep(interval, Config.debug, Config.debug)

    def get_screen(self):
        """获取屏幕（截屏）

        :return: 截图文件的路径
        """
        dir_name = 'CurrentUIHierarchy'
        create_dir(dir_name)
        png_path = f'{dir_name}/{self.ld_index}.png'
        self.exe_cmd(f'shell rm /sdcard/{self.ld_index}.png')
        self.exe_cmd(f'shell screencap -p /sdcard/{self.ld_index}.png')
        self.exe_cmd(f'pull /sdcard/{self.ld_index}.png CurrentUIHierarchy')
        sleep(1)
        return png_path

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

    # pylint: disable=too-many-return-statements,too-many-branches
    def is_target_node(self, dic, start_index=0):
        """通过字典信息判断是否是目标点

        :param dic: 待比对点的字典信息
        :param start_index: 多个匹配项符合条件时目标项的索引值
        :return: 比对成功返回True，否则返回False
        """
        if type(dic) in (str, list):
            return False
        if '@resource-id' not in dic.keys():
            return False
        if self.node.index:
            if self.node.index == dic['@index']:
                if self.node.resource_id and dic['@resource-id'] == self.node.resource_id:
                    return True
                if self.node.naf and '@NAF' in dic and self.node.naf == dic['@NAF']:
                    if self.node.start_count == start_index:
                        return True
                    self.node.start_count += 1
                    return False
                if self.node.text:
                    if self.node.text in unescape(dic['@text']):
                        return True
                    return False
                if self.node.class_ and dic['@class'] == self.node.class_:
                    if self.node.bounds and self.is_target_bounds(self.node.bounds, dic['@bounds']):
                        if dic['@resource-id'] == self.node.resource_id:
                            return True
                        return False
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
            if self.node.resource_id:
                return False
            if self.node.text in unescape(dic['@text']):
                if self.node.start_count == start_index:
                    return True
                self.node.start_count += 1
                return False
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

    def depth_first_search(self, dic, start_index=0):
        """通过深度优先来搜索目标对象

        :param dic: 待搜索对象的字典信息
        :param start_index: 多个匹配项符合条件时目标项的索引值
        :return: 搜索到返回目标对象，否则返回False
        """
        if isinstance(dic, dict):
            if self.is_target_node(dic, start_index):
                return dic
            for i in dic.keys():
                if self.is_target_node(dic[i], start_index):
                    return dic[i]
                res = self.depth_first_search(dic=dic[i], start_index=start_index)
                if res:
                    return res
        elif isinstance(dic, list):
            for i in dic:
                res = self.depth_first_search(dic=i, start_index=start_index)
                if res:
                    return res
        return False

    # pylint: disable=too-many-branches, too-many-arguments
    def get_dict(self, resource_id='', text='', content_desc='', xml='', bounds='', class_='',
                 index='', naf='', start_index=0):
        """获取目标对象的字典信息

        :param resource_id: 资源的身份码
        :param text: 文本
        :param content_desc: 描述
        :param xml: 目标用户界面上元素的层次布局信息
        :param bounds: 边界值（位于目标矩形的斜对角的两点坐标）
        :param class_: 类名
        :param index: 索引值
        :param naf: 可访问性不友好（Not Accessibility Friendly）
         We're looking for UI controls that are enabled, clickable but have no text nor
         content-description. Such controls configuration indicate an interactive control
         is present in the UI and is most likely not accessibility friendly. We refer to
         such controls here as NAF controls.
        :param start_index: 多个匹配项符合条件时目标项的索引值
        :return: 返回通过深度优先方式获取到的字典信息（若找不到目标则返回的字典信息的值为False）
        """
        self.node = Node(resource_id, text, content_desc, bounds, class_, index, naf, start_count=0)
        if xml:
            self.xml = xml
        else:
            self.xml = self.get_current_ui_hierarchy()
        dic = self.depth_first_search(xmltodict.parse(self.xml), start_index)
        if dic:
            dic.update({'@text': unescape(dic['@text'])})
        if text and start_index:
            if dic:
                print(f'检测到【text={text}, start_index={start_index}】')
            else:
                print(f'未找到【text={text}】, start_index={start_index}')
        elif resource_id and text:
            if dic:
                print(f'检测到【resource_id={resource_id}, text={text}】')
            else:
                print(f'未找到【resource_id={resource_id}, text={text}】')
        elif text:
            if dic:
                print(f'检测到【text={text}】')
            else:
                print(f'未找到【text={text}】')
        elif resource_id:
            if dic:
                print(f'检测到【resource_id={resource_id}】')
            else:
                print(f'未找到【resource_id={resource_id}】')
        elif class_:
            if dic:
                print(f'检测到【class_={class_}】')
            else:
                print(f'未找到【class_={class_}】')
        elif naf:
            if dic:
                print(f'检测到【naf={naf}】')
            else:
                print(f'未找到【naf={naf}】')
        return dic

    def get_current_ui_hierarchy(self):
        """获取当前用户界面上元素的层次布局信息

        :return: 正常情况下会返回当前的用户界面上的元素的层次布局信息所构成的xml字符串，如果遇到异常则不做处理直接传递
        """
        self.exe_cmd(f'shell rm /sdcard/window_dump.xml')
        self.exe_cmd(f'shell uiautomator dump /sdcard/window_dump.xml')
        dir_name = 'CurrentUIHierarchy'
        create_dir(dir_name)
        file_path = f"{dir_name}/{self.ld_index}.xml"
        print(file_path)
        if exists(file_path):
            remove(file_path)
        self.exe_cmd(f'pull /sdcard/window_dump.xml {file_path}')
        if Config.debug:
            return get_pretty_xml(file_path)
        return get_xml(file_path)
