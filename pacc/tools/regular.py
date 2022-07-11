"""正则模块"""
from re import compile


def find_all_with_re(data, pattern):
    """寻找所有符合条件的数据

    :param data: 待搜索的数据
    :param pattern: 正则表达式
    :return: 所有符合条件的数据
    """
    return compile(pattern).findall(data)


def find_all_ints_with_re(data):
    """寻找所有符合条件的整数

    :param data: 待搜索的数据
    :return: 数据中的所有整数
    """
    r = find_all_with_re(data, r'\-?\d+')
    res = []
    for i in r:
        res.append(int(i))
    return res
