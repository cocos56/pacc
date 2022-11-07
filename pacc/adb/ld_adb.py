"""雷电模拟器安卓调试桥模块"""
from .ld_base import LDBase


class LDADB(LDBase):
    """雷电模拟器安卓调试桥类"""

    def get_current_focus(self):
        """获取当前界面的Activity

        :return: 当前界面的Activity
        """
        res = self.exe_cmd('shell dumpsys window windows', ' | findstr mCurrentFocus', True)[2:-2]
        print(res)
        return res
