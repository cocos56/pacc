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


class Retrieve:  # pylint: disable=too-few-public-methods
    """该类用于从MySQL数据库中查询数据"""

    # pylint: disable=too-many-arguments
    def query(self, field, table, aimed_field, value, database=MySQL):
        """查询函数：查询数据

        :param field: 待查询数据的字段名
        :param table: 待匹配的表名
        :param aimed_field: 待匹配的目标字段名
        :param value: 待匹配的值
        :param database: 待匹配的数据库名
        :return: 查询到的结果（单条）
        """
        res = database.query(
            f'select `{field}` from `{table}` where `{aimed_field}`={value}')
        database.commit()
        if len(res) == 1:
            return res[0]
        return res


class RetrieveMobile(Retrieve):  # pylint: disable=too-few-public-methods
    """该类用于从MySQL数据库中的mobile数据库中查询数据"""

    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备序列号
        """
        self.serial_num = serial_num

    # pylint: disable=too-many-arguments
    def query(self, field, table, aimed_field='SN', value='', database=Mobile):
        """查询函数：查询数据

        :param field: 待查询数据的字段名
        :param table: 待匹配的表名
        :param aimed_field: 待匹配的目标字段名
        :param value: 待匹配的值
        :param database: 待匹配的数据库名
        :return: 查询到的结果（单条）
        """
        return super().query(field, table, aimed_field, self.serial_num, database)


class RetrieveMobileInfoBase(RetrieveMobile):  # pylint: disable=too-few-public-methods
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

    # pylint: disable=too-many-arguments
    def query(self, field, table='mobile_info', aimed_field='SN', value='', database=Mobile):
        """查询函数：查询数据

        :param field: 待查询数据的字段名
        :param table: 待匹配的表名
        :param aimed_field: 待匹配的目标字段名
        :param value: 待匹配的值
        :param database: 待匹配的数据库名
        :return: 查询到的结果（单条）
        """
        return super().query(field, table)


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


# pylint: disable=too-many-instance-attributes, too-few-public-methods
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

    # pylint: disable=too-many-arguments
    def query(self, field, table='ksjsb', aimed_field='SN', value='', database=Mobile):
        """查询函数：查询数据

        :param field: 待查询数据的字段名
        :param table: 待匹配的表名
        :param aimed_field: 待匹配的目标字段名
        :param value: 待匹配的值
        :param database: 待匹配的数据库名
        :return: 查询到的结果（单条）
        """
        return super().query(field, table)


class RetrieveKsjsb(RetrieveKsjsbBase):
    """查询快手极速版数据类"""

    instances = {'003001002': RetrieveKsjsbBase('003001002')}

    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备序列号
        """
        super().__init__(serial_num)
        self.__class__.instances.update({self.serial_num: self})


class RetrieveIdleFishStaffBase(Retrieve):
    """该类用于为从account数据库中的idle_fish_staff表中查询数据提供基础支持"""
    def __init__(self, name):
        """构造函数

        :param name: 员工姓名
        """
        self.name = name

    # pylint: disable=too-many-arguments
    def query(self, field, table, aimed_field='name', value='', database=Account):
        """查询函数：查询数据

        :param database: 数据库名
        :param table: 表名
        :param field: 字段名
        :param aimed_field: 目标字段名
        :param value: 值
        :return: 查询到的结果（单条）
        """
        if not value:
            value = self.name
        return super().query(field, table, aimed_field, f"'{value}'", database)


# pylint: disable=too-many-public-methods
class RetrieveIdleFishStaff(RetrieveIdleFishStaffBase):
    """查询闲鱼员工类：该类用于从account数据库中的idle_fish_staff表中查询单项记录的某个字段数据"""
    # pylint: disable=too-many-arguments
    def query(
            self, field, table='idle_fish_staff', aimed_field='name', value='',
            database=Account):
        """查询函数：查询数据

        :param database: 数据库名
        :param table: 表名
        :param field: 字段名
        :param aimed_field: 目标字段名
        :param value: 值
        :return: 查询到的结果（单条）
        """
        return super().query(field, table)

    @property
    def remark(self):
        """从数据库中读取员工备注的信息"""
        return self.query('remark')

    @property
    def last_salary_date(self):
        """从数据库中读取上次发工资时的日期"""
        return self.query('last_salary_date')


class RetrieveIdleFishByConsigneeBase(Retrieve):
    """该类用于为从account数据库中的idle_fish表中通过收货人查询数据提供基础支持"""

    def __init__(self, last_buy_consignee):
        """构造函数

        :param last_buy_consignee: 上次购买时的收货人
        """
        self.last_buy_consignee = last_buy_consignee

    # pylint: disable=too-many-arguments
    def query(self, field, table, aimed_field='last_buy_consignee', value='', database=Account):
        """查询函数：查询数据

        :param database: 数据库名
        :param table: 表名
        :param field: 字段名
        :param aimed_field: 目标字段名
        :param value: 值
        :return: 查询到的结果（单条）
        """
        if not value:
            value = self.last_buy_consignee
        return super().query(field, table, aimed_field, f"'{value}'", database)


# pylint: disable=too-many-public-methods
class RetrieveIdleFishByConsignee(RetrieveIdleFishByConsigneeBase):
    """该类用于从account数据库中的idle_fish表中通过收货人查询单项记录的某个字段数据"""
    # pylint: disable=too-many-arguments
    def query(
            self, field, table='idle_fish', aimed_field='last_buy_consignee', value='',
            database=Account):
        """查询函数：查询数据

        :param database: 数据库名
        :param table: 表名
        :param field: 字段名
        :param aimed_field: 目标字段名
        :param value: 值
        :return: 查询到的结果（单条）
        """
        return super().query(field, table)

    @property
    def job_number(self):
        """从数据库中读取工号的信息"""
        job_number = self.query('Job_N')
        if not job_number:
            print(f'未找到上次购买时的收货人：{self.last_buy_consignee}所对应的工号，请确认')
            input()
            return False
        return job_number


class RetrieveIdleFishByUsernameBase(Retrieve):
    """该类用于为从account数据库中的idle_fish表中通过用户名查询数据提供基础支持"""

    def __init__(self, user_name):
        """构造函数

        :param user_name: 用户名
        """
        self.user_name = user_name

    # pylint: disable=too-many-arguments
    def query(self, field, table, aimed_field='user_name', value='', database=Account):
        """查询函数：查询数据

        :param database: 数据库名
        :param table: 表名
        :param field: 字段名
        :param aimed_field: 目标字段名
        :param value: 值
        :return: 查询到的结果（单条）
        """
        if not value:
            value = self.user_name
        return super().query(field, table, aimed_field, f"'{value}'", database)


# pylint: disable=too-many-public-methods
class RetrieveIdleFishByUsername(RetrieveIdleFishByUsernameBase):
    """通过用户名查询闲鱼数据类：该类用于从account数据库中的idle_fish表中通过用户名查询单项记录的某个字段数据"""
    # pylint: disable=too-many-arguments
    def query(
            self, field, table='idle_fish', aimed_field='user_name', value='',
            database=Account):
        """查询函数：查询数据

        :param database: 数据库名
        :param table: 表名
        :param field: 字段名
        :param aimed_field: 目标字段名
        :param value: 值
        :return: 查询到的结果（单条）
        """
        return super().query(field, table)

    @property
    def job_number(self):
        """从数据库中读取工号的信息"""
        job_number = self.query('Job_N')
        if not job_number:
            print(f'未找到用户名：{self.user_name}所对应的工号，请确认')
            return False
        return job_number


class RetrieveIdleFishBase(Retrieve):
    """该类用于为从account数据库中的idle_fish表中查询数据提供基础支持"""

    def __init__(self, job_number):
        """构造函数

        :param job_number: 工号
        """
        self.job_number = job_number

    # pylint: disable=too-many-arguments
    def query(self, field, table, aimed_field='Job_N', value='', database=Account):
        """查询函数：查询数据

        :param field: 待查询数据的字段名
        :param table: 待匹配的表名
        :param aimed_field: 待匹配的目标字段名
        :param value: 待匹配的值
        :param database: 待匹配的数据库名
        :return: 查询到的结果（单条）
        """
        return super().query(field, table, aimed_field, f"'{self.job_number}'", Account)


class RetrieveIdleFish(RetrieveIdleFishBase):  # pylint: disable=too-many-public-methods
    """该类用于从account数据库中的idle_fish表中查询单项记录的某个字段数据"""

    # pylint: disable=too-many-arguments
    def query(self, field, table='idle_fish', aimed_field='Job_N', value='', database=Account):
        """查询函数：查询数据

        :param field: 待查询数据的字段名
        :param table: 待匹配的表名
        :param aimed_field: 待匹配的目标字段名
        :param value: 待匹配的值
        :param database: 待匹配的数据库名
        :return: 查询到的结果（单条）
        """
        return super().query(field, table)

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
    def login_pw(self):
        """从数据库中读取闲鱼账号的登录密码"""
        return self.query('login_pw')

    @property
    def pay_pw(self):
        """从数据库中读取闲鱼账号的支付密码"""
        return self.query('pay_pw')

    @property
    def if_mn(self):
        """从数据库中读取闲鱼绑定的手机号（Idle Fish Mobile Number）"""
        return self.query('if_mn')

    @property
    def nickname(self):
        """从数据库中读取闲鱼账号的昵称"""
        return self.query('nickname')

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
        """从数据库中获取上次更新主机列表的日期"""
        return self.query('last_update_hosts_date')

    @property
    def last_update_version_date(self):
        """从数据库中获取上次更新版本号的日期"""
        return self.query('last_update_version_date')

    @property
    def top_up_mobile(self):
        """从数据库中读取是否执行薅羊毛赚话费的标志"""
        return self.query('top_up_mobile')

    @property
    def top_up_mobile_cnt(self):
        """执行薅羊毛赚话费任务成功的次数"""
        return self.query('top_up_mobile_cnt')

    @property
    def last_top_up_mobile_date(self):
        """从数据库中获取上次薅羊毛赚话费的日期"""
        return self.query('last_top_up_mobile_date')

    @property
    def login(self):
        """从数据库中读取是否需要登录的标志"""
        return self.query('login')

    @property
    def last_login_date(self):
        """从数据库中获取上次登录的日期"""
        return self.query('last_login_date')

    @property
    def last_login_ipv4_addr(self):
        """从数据库中获取上次登录的的公网IPv4地址"""
        return self.query('last_login_ipv4_addr')

    @property
    def buy(self):
        """从数据库中读取是否需要购买的标志"""
        return self.query('buy')

    @property
    def last_buy_date(self):
        """从数据库中读取上次购买的日期"""
        return self.query('last_buy_date')

    @property
    def last_buy_time(self):
        """从数据库中读取上次购买的时间"""
        return self.query('last_buy_time')

    @property
    def last_buy_coins(self):
        """从数据库中读取上次购买时所消耗的闲鱼币"""
        return self.query('last_buy_coins')

    @property
    def pay(self):
        """从数据库中读取是否需要获取好友代付二维码的标志"""
        return self.query('pay')

    @property
    def confirm(self):
        """从数据库中读取是否需要确认收货的标志"""
        return self.query('confirm')

    @property
    def last_confirm_date(self):
        """从数据库中读取上次确认收货的日期"""
        return self.query('last_confirm_date')

    @property
    def base_payee(self):
        """从数据库中读取基层收款人"""
        return self.query('base_payee')

    @property
    def middle_payee(self):
        """从数据库中读取中层收款人"""
        return self.query('middle_payee')


class RetrieveIdleFishRecords:
    """查询闲鱼所有（符合条件的）记录类：该类用于从account数据库中的idle_fish表中查询符合条件的所有记录"""

    @classmethod
    def query_all_create_records(cls, database=Account):
        """查询所有需要创建的记录函数

        :param database: 数据库名
        :return: 查询到的结果
        """
        cmd = 'select Job_N, role from `idle_fish` where `create`=1'
        print(cmd)
        res = database.query(cmd)
        if res:
            if isinstance(res[0], str):
                res = [res]
            else:
                res = list(res)
        print(res)
        return res

    @classmethod
    def query_payee_group_records(cls, group_by='base_payee', database=Account):
        """查询所有人员账号分组汇总后的记录函数

        :param group_by: 分组依据的字段名
        :param database: 数据库名
        :return: 查询到的结果
        """
        cmd = f'SELECT GROUP_CONCAT(Job_N SEPARATOR "||"), {group_by} FROM `idle_fish` ' \
              f'WHERE last_confirm_date = CURDATE() GROUP BY {group_by} ORDER BY `Job_N`;'
        # print(cmd)
        res = database.query(cmd)
        if res:
            if isinstance(res[0], str):
                res = [res]
            else:
                res = list(res)
        # print(res)
        return res

    @classmethod
    def query_base_payee_group_records(cls):
        """查询所有基层人员账号分组汇总后的记录函数

        :return: 查询到的结果
        """
        return cls.query_payee_group_records()

    @classmethod
    def query_middle_payee_group_records(cls):
        """查询所有中层人员账号分组汇总后的记录函数

        :return: 查询到的结果
        """
        return cls.query_payee_group_records('middle_payee')


class RetrieveDispatchRecords:
    """查询发货记录类：该类用于从record数据库中的record_dispatch表中查询符合条件的所有记录"""
    @classmethod
    def query_no_payee_records(cls, database=Record):
        """查询所有需要创建的记录函数

        :param database: 数据库名
        :return: 查询到的结果
        """
        cmd = 'select dispatch_date, Job_N, role, user_name, dispatch_consignee, base_payee, ' \
              'middle_payee from ' \
              '`record_dispatch` where confirm_date = CURDATE() ORDER BY Job_N'
        print(cmd)
        res = database.query(cmd)
        if res:
            if isinstance(res[0], str):
                res = [res]
            else:
                res = list(res)
        # print(res)
        return res


class RetrieveAccount(Retrieve):
    """该类用于从MySQL数据库中的account数据库中查询数据"""

    def __init__(self, username):
        """构造函数

        :param username: 用户名
        """
        self.username = username

    # pylint: disable=too-many-arguments
    def query(self, field, table, aimed_field='username', value='', database=Account):
        """查询函数：查询数据

        :param field: 待查询数据的字段名
        :param table: 待匹配的表名
        :param aimed_field: 待匹配的目标字段名
        :param value: 待匹配的值
        :param database: 待匹配的数据库名
        :return: 查询到的结果（单条）
        """
        return super().query(field, table, 'username', f"'{self.username}'", Account)


class RetrieveEmail(RetrieveAccount):
    """查询邮箱账号类"""

    def __init__(self, username):
        """构造函数

        :param username: 用户名
        """
        super().__init__(username)
        self.auth_code = self.query('auth_code')

    # pylint: disable=too-many-arguments
    def query(self, field, table='email', aimed_field='username', value='', database=Account):
        """查询函数：查询数据

        :param field: 待查询数据的字段名
        :param table: 待匹配的表名
        :param aimed_field: 待匹配的目标字段名
        :param value: 待匹配的值
        :param database: 待匹配的数据库名
        :return: 查询到的结果（单条）
        """
        return super().query(field, table)
