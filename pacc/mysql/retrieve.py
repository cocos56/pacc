"""MySQL数据库包的查模块"""
from .mysql import MySQL, Mobile, Account


class RetrieveSD:
    """查询刷单数据类"""

    all_accounts = []
    all_names = []

    @classmethod
    def get_all_names(cls):
        """获取所有账号"""
        if cls.all_names:
            return cls.all_names
        for account in cls.query_all_names():
            cls.all_names.append(account[0])
        return cls.all_names

    @classmethod
    def get_all_accounts(cls):
        """获取所有账号"""
        if cls.all_accounts:
            return cls.all_accounts
        for account in cls.query_all_accounts():
            cls.all_accounts.append(account[0])
        return cls.all_accounts

    @classmethod
    def query_all_data(cls, field='account', database=Mobile):
        """查询函数：查询指定列的所有行数据

        :param field: 目标列的字段名
        :param database: 数据库名
        :return: 查询到的结果
        """
        res = database.query(
            f'select `{field}` from `sd`')
        if len(res) == 1:
            return res[0]
        return res

    @classmethod
    def query_all_accounts(cls):
        """查询函数：查询所有账号

        :return: 查询到的结果
        """
        return cls.query_all_data('account')

    @classmethod
    def query_all_names(cls):
        """查询函数：查询所有名字

        :return: 查询到的结果
        """
        return cls.query_all_data('name')


RetrieveSD.get_all_accounts()
RetrieveSD.get_all_names()


# pylint: disable=too-few-public-methods
class Retrieve:
    """该类用于从MySQL数据库中查询数据"""

    # pylint: disable=too-many-arguments
    def query(self, table, field, aimed_field, value, database=MySQL):
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

    # pylint: disable=arguments-differ
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


class RetrieveKsjsbBase(RetrieveMobile):
    """查询快手极速版数据类基类"""

    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备序列号
        """
        super().__init__(serial_num)
        self.gold_coins = self.query('gold_coins')
        self.cash_coupons = self.query('cash_coupons')
        self.last_sign_in_day = self.query('last_sign_in_day')
        self.last_change_money_day = self.query('last_change_money_day')
        self.last_view_ads_day = self.query('last_view_ads_day')
        self.last_watch_live_day = self.query('last_watch_live_day')

    # pylint: disable=arguments-differ
    def query(self, field):
        """查询函数：查询数据

        :param field: 字段名
        :return: 查询到的结果（单条）
        """
        return super().query('ksjsb', field)


class RetrieveKsjsb(RetrieveKsjsbBase):
    """查询快手极速版数据类"""

    instances = {'003001002': RetrieveKsjsbBase('003001002')}

    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备序列号
        """
        super().__init__(serial_num)
        self.__class__.instances.update({self.serial_num: self})


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
