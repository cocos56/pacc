from .mysql import query, commit


class Update:

    def __init__(self, SN):
        self.SN = SN

    def query(self, table, field, value):
        cmd = 'update `%s` set `%s` = "%s" where `SN` = "%s"' % (table, field, value, self.SN)
        print(cmd)
        res = query(cmd)
        commit()
        return res


class UpdateKSJSB(Update):

    def __init__(self, SN):
        super(UpdateKSJSB, self).__init__(SN)

    def query(self, field, value):
        return super(UpdateKSJSB, self).query('KSJSB', field, value)

    def updateGoldCoins(self, goldCoins):
        print(self.query('goldCoins', goldCoins))

    def updateCashCoupons(self, cashCoupons):
        print(self.query('cashCoupons', cashCoupons))


class UpdateBaseInfo(Update):

    def __init__(self, SN):
        super(UpdateBaseInfo, self).__init__(SN)

    def query(self, field, value):
        return super(UpdateBaseInfo, self).query('BaseInfo', field, value)

    def updateIP(self, ip):
        print(self.query('IP', ip))

    def updateModel(self, model):
        print(self.query('Model', model))
