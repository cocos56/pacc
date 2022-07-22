"""MySQL数据库包的查模块"""
from .mysql import MySQL, Mobile, Account


# pylint: disable=too-few-public-methods
class Retrieve:
    """该类用于从MySQL数据库中查询数据"""

    # pylint: disable=too-many-arguments
    def query(self, table, field, aimed_field=1, value=1, database=MySQL):
        """查询函数：查询数据

        :param database: 数据库名
        :param table: 表名
        :param field: 字段名
        :param aimed_field: 目标字段名
        :param value: 值
        :return: 查询到的结果（单条）
        """
        res = database.query(
            f'select `{field}` from `{table}` where `{aimed_field}`={value}')
        if len(res) == 1:
            return res[0]
        return res


# pylint: disable=too-few-public-methods
class RetrieveMobile(Retrieve):
    """该类用于从MySQL数据库中的mobile数据库中查询数据"""

    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备序列号
        """
        self.serial_num = serial_num

    def query(self, table, field):
        """查询函数：查询数据

        :param table: 表名
        :param field: 字段名
        :return: 查询到的结果（单条）
        """
        return super().query(table, field, 'SN', self.serial_num, Mobile)


class RetrieveMobileInfo(RetrieveMobile):
    """查询手机信息类"""
    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备序列号
        """
        super().__init__(serial_num)
        self.ipv4_addr = self.query('IP')
        self.id_num = self.query('ID')
        self.model = self.query('Model')

    # pylint: disable=arguments-differ
    def query(self, field):
        """查询函数：查询数据

        :param field: 字段名
        :return: 查询到的结果（单条）
        """
        return super().query('mobile_info', field)


class RetrieveKSJSB(RetrieveMobile):
    """查询快手极速版数据类"""
    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备序列号
        """
        super().__init__(serial_num)
        self.gold_coins = self.query('goldCoins')
        self.cash_coupons = self.query('cashCoupons')

    # pylint: disable=arguments-differ
    def query(self, field):
        """查询函数：查询数据

        :param field: 字段名
        :return: 查询到的结果（单条）
        """
        return super().query('KSJSB', field)


class RetrieveAccount(Retrieve):
    """该类用于从MySQL数据库中的account数据库中查询数据"""

    def __init__(self, username):
        """构造函数

        :param username: 用户名
        """
        self.username = username

    # pylint: disable=arguments-differ
    def query(self, table, field):
        """查询函数：查询数据

        :param table: 表名
        :param field: 字段名
        :return: 查询到的结果（单条）
        """
        return super().query(table, field, 'username', f"'{self.username}'", Account)


class RetrieveEmail(RetrieveAccount):
    """查询邮箱账号类"""
    def __init__(self, username):
        """构造函数

        :param username: 用户名
        """
        super().__init__(username)
        self.auth_code = self.query('auth_code')

    # pylint: disable=arguments-differ
    def query(self, field):
        """查询函数：查询数据

        :param field: 字段名
        :return: 查询到的结果（单条）
        """
        return super().query('email', field)
