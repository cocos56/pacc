"""MySQL数据库包的改模块"""
from .mysql import Mobile


class Update:
    """MySQL数据库包的改模块的改类"""

    def __init__(self, device_sn):
        """构造函数：初始化改类的对象

        :param device_sn: 设备序列号
        """
        self.device_sn = device_sn

    def query(self, table, field, value):
        """查询函数：修改数据

        :param table: 表名
        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :return: 修改的结果
        """
        cmd = 'update `%s` set `%s` = "%s" where `SN` = "%s"' % (table, field, value, self.device_sn)
        print(cmd)
        res = Mobile.query(cmd)
        Mobile.commit()
        return res


class UpdateBaseInfo(Update):

    def __init__(self, SN):
        super(UpdateBaseInfo, self).__init__(SN)

    def query(self, field, value):
        return super(UpdateBaseInfo, self).query('mobile_info', field, value)

    def updateIP(self, ip):
        print(self.query('IP', ip))

    def updateModel(self, model):
        print(self.query('Model', model))


class UpdateKSJSB(Update):

    def __init__(self, SN):
        super(UpdateKSJSB, self).__init__(SN)

    def query(self, field, value):
        return super(UpdateKSJSB, self).query('KSJSB', field, value)

    def updateGoldCoins(self, goldCoins):
        print(self.query('goldCoins', goldCoins))

    def updateCashCoupons(self, cashCoupons):
        print(self.query('cashCoupons', cashCoupons))
