"""雷电自动化测试模块"""
from os import remove
from os.path import exists

from .ld_base import LDBase
from .uia import Node
from ..base import sleep
from ..config import Config
from ..tools import create_dir, get_pretty_xml, get_xml


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

    # pylint: disable=too-many-branches
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
