"""雷电模拟器安卓调试桥模块"""
from .ld_base import LDBase
from ..base import sleep, print_err
from ..tools import find_all_with_re


class LDADB(LDBase):
    """雷电模拟器安卓调试桥类"""

    def get_app_version_info(self, package_name):
        """获取指定APP的版本信息"""
        res = self.exe_cmd(f'shell pm dump {package_name}', ' | findstr versionName', True)
        try:
            res = find_all_with_re(res, 'versionName=(.+)\n')[0]
            # print(f'The version of {package_name} is {res}')
            return res
        except IndexError as err:
            print_err(err)
            return '0.0.0'

    def get_app_list(self):
        """获取已安装应用的列表"""
        res = self.exe_cmd('shell pm list package', return_flag=True)
        print(res)

    def press_key(self, keycode, sleep_time=1):
        """按键

        :param keycode: 按键代码
        :param sleep_time: 休息时间
        """
        print(f'正在让{self.ld_index}按{keycode}')
        self.exe_cmd(f'shell input keyevent {keycode}')
        sleep(sleep_time, True, True)

    def press_back_key(self, sleep_time=1):
        """按返回键

        :param sleep_time: 休息时间
        """
        self.press_key('KEYCODE_BACK', sleep_time)

    def get_current_focus(self):
        """获取当前界面的Activity

        :return: 当前界面的Activity
        """
        res = self.exe_cmd('shell dumpsys window windows', ' | findstr mCurrentFocus', True)[2:-2]
        print(res)
        return res
