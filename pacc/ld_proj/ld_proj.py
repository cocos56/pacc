"""雷电模拟器工程基类"""
import os

from ..config import Config


class LDProj:  # pylint: disable=too-few-public-methods
    """雷电模拟器的工程类"""
    def __init__(self):
        """构造函数"""
        os.chdir(Config.ld_work_path)

