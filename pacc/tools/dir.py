"""文件夹模块"""
from os import mkdir
from os.path import exists
from shutil import rmtree


def create_dir(dir_path, remove_old_dir_flag=False):
    """创建文件夹

    :param dir_path: 文件夹路径
    :param remove_old_dir_flag: 是否移除旧文件夹标志，默认为否
    """
    if remove_old_dir_flag and exists(dir_path):
        rmtree(dir_path)
    if not exists(dir_path):
        mkdir(dir_path)
