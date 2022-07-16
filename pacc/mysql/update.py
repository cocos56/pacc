"""MySQL数据库包的改模块"""
from .mysql import Mobile


# pylint: disable=too-few-public-methods
class Update:
    """MySQL数据库包的改模块的改类"""

    def __init__(self, serial_num):
        """构造函数：初始化改类的对象

        :param serial_num: 设备序列号
        """
        self.serial_num = serial_num

    def query(self, table, field, value):
        """查询函数：修改数据

        :param table: 表名
        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :return: 修改的结果
        """
        cmd = f'update `{table}` set `{field}` = "{value}" where `SN` = "{self.serial_num}"'
        print(cmd)
        res = Mobile.query(cmd)
        Mobile.commit()
        return res


class UpdateMobileInfo(Update):
    """更改手机信息类"""

    def query(self, field, value):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :return: 修改的结果
        """
        return super().query('mobile_info', field, value)

    def update_ipv4_addr(self, ipv4_addr):
        """更新手机的IPv4地址

        :param ipv4_addr: 新的IPv4地址
        """
        print(self.query('IP', ipv4_addr))

    def update_model(self, model):
        """更新手机的型号

        :param model: 新的型号
        """
        print(self.query('Model', model))


class UpdateKSJSB(Update):
    """更改快手极速版信息类"""

    def query(self, field, value):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :return: 修改的结果
        """
        return super().query('KSJSB', field, value)

    def update_gold_coins(self, gold_coins):
        """更新金币值

        :param gold_coins: 金币
        """
        print(self.query('goldCoins', gold_coins))

    def update_cash_coupons(self, cash_coupons):
        """更新现金值

        :param cash_coupons: 现金
        """
        print(self.query('cashCoupons', cash_coupons))
