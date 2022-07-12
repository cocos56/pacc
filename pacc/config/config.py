"""配置模块"""


# pylint: disable=too-few-public-methods
class Config:
    """配置类"""
    debug = False

    @classmethod
    def set_debug(cls, debug):
        """设置是否为调试状态

        :param debug: 调试状态标志
        """
        cls.debug = debug
