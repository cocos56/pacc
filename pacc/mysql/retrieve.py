"""MySQL数据库包的查模块"""
from .mysql import MySQL, Mobile, Account, Record


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
    def query_all_data(cls, field='account', database=Account):
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
        database.commit()
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


class RetrieveMobileInfoBase(RetrieveMobile):
    """查询手机信息类"""

    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备序列号
        """
        super().__init__(serial_num)
        self.id_num = self.query('ID')
        self.ipv4_addr = self.query('IP')
        self.model = self.query('model')
        self.last_reboot_date = self.query('last_reboot_date')

    # pylint: disable=arguments-differ
    def query(self, field):
        """查询函数：查询数据

        :param field: 字段名
        :return: 查询到的结果（单条）
        """
        return super().query('mobile_info', field)


class RetrieveMobileInfo(RetrieveMobileInfoBase):
    """查询手机信息类"""
    instances = {'003001001': RetrieveMobileInfoBase('003001001')}

    @classmethod
    def get_ins(cls, serial_num):
        """获取指定设备序列号所对应的单例对象

        :param serial_num: 设备序列号
        """
        if serial_num not in cls.instances:
            cls.instances.update({serial_num: cls(serial_num)})
        return cls.instances.get(serial_num)


# pylint: disable=too-many-instance-attributes
class RetrieveKsjsbBase(RetrieveMobile):
    """查询快手极速版数据类基类"""

    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备序列号
        """
        super().__init__(serial_num)
        self.gold_coins = self.query('gold_coins')
        self.cash_coupons = self.query('cash_coupons')
        self.last_sign_in_date = self.query('last_sign_in_date')
        self.version_info = self.query('version_info')
        self.last_double_bonus_date = self.query('last_double_bonus_date')
        self.last_treasure_box_date = self.query('last_treasure_box_date')
        self.last_view_ads_date = self.query('last_view_ads_date')
        self.last_watch_live_date = self.query('last_watch_live_date')
        self.last_shopping_date = self.query('last_shopping_date')
        self.last_meal_allowance_datetime = self.query('last_meal_allowance_datetime')
        self.last_desktop_component_date = self.query('last_desktop_component_date')
        self.last_buy_things_date = self.query('last_buy_things_date')
        self.last_change_money_date = self.query('last_change_money_date')
        self.last_update_wealth_date = self.query('last_update_wealth_date')
        self.last_watch_video_date = self.query('last_watch_video_date')

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


class RetrieveRecordIdleFishBase(Retrieve):
    """该类用于为从account数据库中的idle_fish表中查询数据提供基础支持"""

    def __init__(self, job_number, today):
        """构造函数

        :param job_number: 工号
        :param today: 今天的日期
        """
        self.job_number = job_number
        self.today = today

    # pylint: disable=arguments-differ
    def query(self, field, table):
        """查询函数：查询数据

        :param field: 字段名
        :param table: 表名
        :return: 查询到的结果（单条）
        """
        return super().query(table, field, 'Job_N', f"'{self.job_number}'", Record)


class RetrieveIdleFishBase(Retrieve):
    """该类用于为从account数据库中的idle_fish表中查询数据提供基础支持"""

    def __init__(self, job_number):
        """构造函数

        :param job_number: 工号
        """
        self.job_number = job_number

    # pylint: disable=arguments-differ
    def query(self, field, table):
        """查询函数：查询数据

        :param field: 字段名
        :param table: 表名
        :return: 查询到的结果（单条）
        """
        return super().query(table, field, 'Job_N', f"'{self.job_number}'", Account)


class RetrieveIdleFish(RetrieveIdleFishBase):
    """该类用于从account数据库中的idle_fish表中查询数据"""

    @property
    def role(self):
        """从数据库中读取角色的信息"""
        return self.query('role')

    @property
    def version(self):
        """从数据库中读取版本号的信息"""
        return self.query('version')

    @property
    def coins(self):
        """从数据库中读取闲鱼币币值"""
        return self.query('coins')

    @property
    def reminder_threshold(self):
        """从数据库中读取提醒阈值"""
        return self.query('RT')

    @property
    def user_name(self):
        """从数据库中读取闲鱼账号的会员名"""
        return self.query('user_name')

    @property
    def last_check_date(self):
        """从数据库中读取上次检查的日期"""
        return self.query('last_check_date')

    @property
    def last_run_date(self):
        """从数据库中读取上次运行的日期"""
        return self.query('last_run_date')

    @property
    def last_bak_date(self):
        """从数据库中读取上次备份的日期"""
        return self.query('last_bak_date')

    @property
    def today_global_ipv4_addr(self):
        """从数据库中读取本机今日的公网IPv4地址"""
        return self.query('today_global_ipv4_addr')

    @property
    def last_update_ip_date(self):
        """从数据库中获取上次更新本机公网IPv4地址的日期"""
        return self.query('last_update_ip_date')

    @property
    def hosts(self):
        """从数据库中读取主机列表的信息"""
        return self.query('hosts')

    @property
    def last_update_hosts_date(self):
        """从数据库中获取上次更新本机公网IPv4地址的日期"""
        return self.query('last_update_hosts_date')

    # pylint: disable=arguments-differ
    def query(self, field, table='idle_fish'):
        """查询函数：查询数据

        :param field: 字段名
        :param table: 表名
        :return: 查询到的结果（单条）
        """
        return super().query(field, table)


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
