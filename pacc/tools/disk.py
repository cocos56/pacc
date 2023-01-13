from psutil import disk_usage


def get_gbs(number_of_bytes: int) -> int:
    """获取GB数

    :param number_of_bytes: 字节数
    :return: GB数
    """
    return number_of_bytes//1024//1024//1024


class DiskUsage:
    """磁盘占用"""

    def __init__(self, path):
        """构造函数

        :param path: 目录，形如：E:
        """
        usage = disk_usage(path)
        self.total = get_gbs(usage.total)
        self.used = get_gbs(usage.used)
        self.free = get_gbs(usage.free)
        self.percent = usage.percent
