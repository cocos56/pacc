"""MySQL数据库包的增模块"""
from .mysql import M


class Create:
    def __init__(self, SN):
        self.SN = SN

    @classmethod
    def query(cls, table, fields, values):
        cmd = 'insert into `%s` %s values %s' % (table, str(fields).replace("'", '`'), str(values))
        print(cmd)
        res = M.query(cmd)
        M.commit()
        return res


class CreateKSJSB(Create):
    def __init__(self, SN):
        super(CreateKSJSB, self).__init__(SN)
        if self.exist:
            return
        self.query('KSJSB', ('SN', 'goldCoins', 'cashCoupons'), (SN, 0, 0))

    @property
    def exist(self): return M.query('select 1 from `KSJSB` where `SN` = %s limit 1' % self.SN) == (1,)
