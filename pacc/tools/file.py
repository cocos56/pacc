"""文件模块"""
import os


# pylint: disable=too-few-public-methods
class File:
    """文件类"""
    def __init__(self, path):
        """构造函数

        :param path: 文件的路径
        """
        abspath = os.path.abspath(path)
        # pylint: disable=unused-variable
        dir_path, file_path = os.path.split(abspath)
        # D:\0\Desktop\度盘\2020年平顶山学院暑期实训《恶魔射手》
        # 9.9.注册页面搭建(Av711127967,P9).mp4
        # pylint: disable=unused-variable
        f_name, f_ext_name = os.path.splitext(file_path)
        # 9.9.注册页面搭建(Av711127967,P9)
        # .mp4
        # pylint: disable=unused-variable
        self.dir_path_and_file_name, file_ext_name = os.path.splitext(abspath)
        # D:\0\Desktop\度盘\2020年平顶山学院暑期实训《恶魔射手》\9.9.注册页面搭建(Av711127967,P9)
        # .mp4
