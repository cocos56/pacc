"""MySQL数据库包的查模块"""
from .mysql import query


class Retrieve:
    """MySQL数据库包的查模块的查类"""
    def __init__(self, device_sn):
        """构造函数：初始化安卓调试桥类的对象

        :param device_sn: 设备序列号
        """
        self.device_sn = device_sn

    def query(self, table, field):
        res = query('select `%s` from `%s` where `SN` = %s' % (field, table, self.device_sn))
        if len(res) == 1:
            res = res[0]
        return res


class RetrieveKSJSB(Retrieve):
    def __init__(self, SN):
        super(RetrieveKSJSB, self).__init__(SN)
        self.goldCoins = self.query('goldCoins')
        self.cashCoupons = self.query('cashCoupons')

    def query(self, field):
        return super(RetrieveKSJSB, self).query('KSJSB', field)


class RetrieveBaseInfo(Retrieve):
    def __init__(self, SN):
        super(RetrieveBaseInfo, self).__init__(SN)
        self.IP = self.query('IP')
        self.ID = self.query('ID')
        self.Model = self.query('Model')

    def query(self, field):
        return super(RetrieveBaseInfo, self).query('mobile_info', field)
