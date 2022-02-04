from .mysql import query


class Retrieve:
    def __init__(self, SN):
        self.SN = SN

    def query(self, table, field):
        res = query('select `%s` from `%s` where `SN` = %s' % (field, table, self.SN))
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
        return super(RetrieveBaseInfo, self).query('BaseInfo', field)
