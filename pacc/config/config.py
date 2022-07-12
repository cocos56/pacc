"""配置模块"""


class Config:
    """配置类"""
    debug = False

    @classmethod
    def set_debug(cls, debug):
        cls.debug = debug
