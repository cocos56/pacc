"""MySQL数据库包的查模块"""
from .mysql import M


class Retrieve:
    """查类"""

    def __init__(self, sn):
        """构造函数：初始化查类的对象

        :param sn: 设备序列号
        """
        self.sn = sn

    def query(self, table, field):
        """查询函数：查询数据

        :param table: 表名
        :param field: 字段名
        :return: 查询到的结果（单条）
        """
        res = M.query('select `%s` from `%s` where `SN` = %s' % (field, table, self.sn))
        if len(res) == 1:
            res = res[0]
        return res


class RetrieveMobileInfo(Retrieve):
    """查询手机信息类"""
    def __init__(self, device_sn):
        """构造函数：初始化查类的对象

        :param device_sn: 设备序列号
        """
        super(RetrieveMobileInfo, self).__init__(device_sn)
        self.IP = self.query('IP')
        self.ID = self.query('ID')
        self.Model = self.query('Model')

    def query(self, field):
        """查询函数：查询数据

        :param field: 字段名
        :return: 查询到的结果（单条）
        """
        return super(RetrieveMobileInfo, self).query('mobile_info', field)


class RetrieveKSJSB(Retrieve):
    def __init__(self, SN):
        super(RetrieveKSJSB, self).__init__(SN)
        self.goldCoins = self.query('goldCoins')
        self.cashCoupons = self.query('cashCoupons')

    def query(self, field):
        return super(RetrieveKSJSB, self).query('KSJSB', field)
