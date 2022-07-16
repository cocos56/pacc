"""文件模块"""
import os


class File:
    def __init__(self, filePath):
        fileAbsPath = os.path.abspath(filePath)
        dirPath, filePath = os.path.split(fileAbsPath)
        # D:\0\Desktop\度盘\2020年平顶山学院暑期实训《恶魔射手》
        # 9.9.注册页面搭建(Av711127967,P9).mp4
        fName, fExName = os.path.splitext(filePath)
        # 9.9.注册页面搭建(Av711127967,P9)
        # .mp4
        self.dirPathAndFName, fExName = os.path.splitext(fileAbsPath)
        # D:\0\Desktop\度盘\2020年平顶山学院暑期实训《恶魔射手》\9.9.注册页面搭建(Av711127967,P9)
        # .mp4
