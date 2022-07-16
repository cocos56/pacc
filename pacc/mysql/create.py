"""MySQL数据库包的增模块"""
from .mysql import Mobile


# pylint: disable=too-few-public-methods
class Create:
    """增类：往数据库中新增数据"""

    def __init__(self, device_sn):
        """构造函数：初始化增类的对象

        :param device_sn: 设备序列号
        """
        self.device_sn = device_sn

    @classmethod
    def query(cls, table, fields, values):
        """查询函数：新增数据

        :param table: 表名
        :param fields: 字段名
        :param values: 值
        :return: 查询到的结果（单条）
        """
        cmd = f'insert into `{table}` %s values {str(values)}' % str(fields).replace("'", '`')
        print(cmd)
        res = Mobile.query(cmd)
        Mobile.commit()
        return res


class CreateKSJSB(Create):
    """增类：往快手极速版数据库中新增数据"""
    def __init__(self, device_sn):
        """构造函数：初始化增类的对象

        :param device_sn: 设备序列号
        """
        super().__init__(device_sn)
        if self.exist:
            return
        self.query('KSJSB', ('SN', 'goldCoins', 'cashCoupons'), (device_sn, 0, 0))

    @property
    def exist(self):
        """创建只读属性exist，该属性用于判断是否存在快手极速版数据库中存在指定设备的数据"""
        return Mobile.query(f'select 1 from `KSJSB` where `SN` = {self.device_sn} limit 1') == (1,)
