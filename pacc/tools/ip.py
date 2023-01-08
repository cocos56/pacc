"""IP地址模块"""
# pylint: disable=redefined-builtin
from datetime import datetime
from random import randint

import requests
from requests.exceptions import ReadTimeout, ConnectionError

from ..base import print_err


def get_global_ipv4_addr():
    """获取本机公网IPv4地址

    :return: 本机的公网IPv4地址，形如：120.219.74.14
    """
    try:
        ipv4_addr = requests.get('https://checkip.amazonaws.com', timeout=26).text.strip()
    except (ReadTimeout, ConnectionError) as err:
        print_err(err)
        return get_global_ipv4_addr()
    return ipv4_addr


def get_global_ipv4_addr_2():
    """获取本机公网IPv4地址

    :return: 本机的公网IPv4地址，形如：120.219.74.14
    """
    servers = ['http://icanhazip.com', 'https://checkip.amazonaws.com', 'https://ident.me']
    random_server_index = randint(0, len(servers)-1)
    try:
        start_datetime = datetime.now()
        ipv4_addr = requests.get(servers[random_server_index], timeout=9).text.strip()
    except ReadTimeout as err:
        print_err(err)
        return get_global_ipv4_addr()
    print(servers[random_server_index], [ipv4_addr])
    print(datetime.now() - start_datetime)
    return ipv4_addr


def get_global_ipv4_addr_and_location():
    """获取本机公网IPv4地址及其相对应的位置信息（精确到市）

    :return: 本机的公网IPv4地址及其相对应的位置信息（精确到市），
        形如：当前 IP：120.219.74.14  来自于：中国 河南 周口  移动
    """
    ipv4_addr_and_location = requests.get('http://myip.ipip.net', timeout=5).text.strip()
    # print([ipv4_addr_and_location])
    return ipv4_addr_and_location
