"""MySQL数据库包的查模块"""
from .mysql import Mobile


# pylint: disable=too-few-public-methods
class Retrieve:
    """查类"""

    def __init__(self, serial_number):
        """构造函数：初始化查类的对象

        :param serial_number: 设备序列号
        """
        self.serial_number = serial_number

    def query(self, table, field):
        """查询函数：查询数据

        :param table: 表名
        :param field: 字段名
        :return: 查询到的结果（单条）
        """
        res = Mobile.query(f'select `{field}` from `{table}` where `SN` = {self.serial_number}')
        if len(res) == 1:
            res = res[0]
        return res


class RetrieveMobileInfo(Retrieve):
    """查询手机信息类"""
    def __init__(self, serial_number):
        """构造函数：初始化查类的对象

        :param serial_number: 设备序列号
        """
        super().__init__(serial_number)
        self.ip = self.query('IP')
        self.id = self.query('ID')
        self.model = self.query('Model')

    # pylint: disable=arguments-differ
    def query(self, field):
        """查询函数：查询数据

        :param field: 字段名
        :return: 查询到的结果（单条）
        """
        return super().query('mobile_info', field)


class RetrieveKSJSB(Retrieve):
    """查询快手极速版数据类"""
    def __init__(self, serial_number):
        """构造函数：初始化查类的对象

        :param serial_number: 设备序列号
        """
        super().__init__(serial_number)
        self.gold_coins = self.query('goldCoins')
        self.cash_coupons = self.query('cashCoupons')

    # pylint: disable=arguments-differ
    def query(self, field):
        """查询函数：查询数据

        :param field: 字段名
        :return: 查询到的结果（单条）
        """
        return super().query('KSJSB', field)
