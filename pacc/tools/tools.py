"""工具模块"""
import os
import warnings

from urlextract import URLExtract

extractor = URLExtract()
warnings.filterwarnings("ignore")


def system(cmd, is_print=True):
    """创建一个子进程在系统上执行命令行

    :param cmd: 待执行的命令
    :param is_print: 是否打印命令，默认会打印
    """
    if is_print:
        print(cmd)
    os.system(cmd)


def get_urls_from_string(string):
    """从字符串中获取所有链接

    :param string: 字符串
    :return: 字符串中所有的链接
    """
    return extractor.find_urls(string)


def average(*args):
    """获取平均值

    :param args: 参数列表
    :return: 参数列表里所有数字的算术平均值
    """
    return int(sum(args) / len(args))
