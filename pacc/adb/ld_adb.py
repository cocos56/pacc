"""雷电模拟器安卓调试桥模块"""
from .ld_base import LDBase
from ..base import sleep


class LDADB(LDBase):
    """雷电模拟器安卓调试桥类"""

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
