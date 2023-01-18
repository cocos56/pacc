"""雷电模拟器安卓调试桥模块"""
from random import randint

from .ld_base import LDBase
from ..base import sleep, print_err
from ..tools import find_all_with_re


class LDADB(LDBase):
    """雷电模拟器安卓调试桥类"""

    def get_app_version_info(self, package_name):
        """获取指定APP的版本信息"""
        res = self.popen_run(f'shell pm dump {package_name}', ' | findstr versionName')
        try:
            res = find_all_with_re(res, 'versionName=(.+)\n')[0]
            # print(f'The version of {package_name} is {res}')
            return res
        except IndexError as err:
            print_err(err)
            return '0.0.0'

    def get_app_list(self):
        """获取已安装应用的列表"""
        res = self.popen_run('shell pm list package')
        print(res)

    def press_key(self, keycode, sleep_time=1):
        """按键

        :param keycode: 按键代码
        :param sleep_time: 休息时间
        """
        print(f'正在让{self.ld_index}按{keycode}')
        self.sys_run(f'shell input keyevent {keycode}')
        sleep(sleep_time, True, True)

    def press_back_key(self, sleep_time=1):
        """按返回键

        :param sleep_time: 休息时间
        """
        self.press_key('KEYCODE_BACK', sleep_time)

    def input_text(self, text):
        """输入文本

        :param text: 文本内容
        """
        self.popen_run(f'shell input text "{text}"')

    def get_current_focus(self):
        """获取当前界面的Activity

        :return: 当前界面的Activity
        """
        res = self.popen_run('shell dumpsys window windows', ' | findstr mCurrentFocus')[2:-2]
        print(res)
        return res

    def swipe(self, start_coordinate, end_coordinate, duration=-1):
        """滑动
        :param start_coordinate: 起点的坐标（x1, y1）
        :param end_coordinate: 终点的坐标（x2, y2）
        :param duration: the default duration value -1 means a random integer from 2500 to 2501
        """
        x1_coordinate, y1_coordinate = start_coordinate
        x2_coordinate, y2_coordinate = end_coordinate
        if duration == -1:
            duration = randint(2500, 2501)
        self.popen_run(f'shell input swipe {x1_coordinate} {y1_coordinate} {x2_coordinate} '
                       f'{y2_coordinate} {duration}')
