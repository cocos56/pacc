"""MySQL数据库包的增模块"""
from .mysql import Mobile, Record, Account


# pylint: disable=too-few-public-methods
class Create:
    """增类：往数据库中新增数据"""

    @classmethod
    def query(cls, table, fields, values, database=Mobile):
        """查询函数：新增数据

        :param table: 表名
        :param fields: 字段名
        :param values: 值
        :param database: 数据库名
        :return: 查询到的结果（单条）
        """
        cmd = f'insert into `{table}` %s values {str(values)}' % str(fields).replace("'", '`')
        print(cmd)
        res = database.query(cmd)
        database.commit()
        return res


# pylint: disable=too-many-instance-attributes
class CreateIdleFish(Create):
    """idle_fish表的增类：往数据库中的idle_fish表中新增数据"""

    # pylint: disable=too-many-arguments
    def __init__(self, job_number, role, reminder_threshold, user_name, login_pw, pay_pw):
        """构造函数：初始化增类的对象

        :param job_number: 工号
        :param role: 角色
        :param reminder_threshold: 提醒阈值
        :param user_name: 闲鱼账号的会员名
        :param login_pw: 闲鱼账号的登录密码
        :param pay_pw: 闲鱼账号所绑定支付宝账号的的支付密码
        """
        self.job_number = job_number
        if self.exist:
            print(f'记录job_number={self.job_number}已存在，无需重复创建')
            return
        self.query('idle_fish',
                   ('Job_N', 'role', 'RT', 'user_name', 'login_pw', 'pay_pw', 'create'),
                   (self.job_number, role, reminder_threshold, user_name, login_pw, pay_pw, 1))

    @classmethod
    def query(cls, table, fields, values, database=Account):
        """查询函数：新增数据

        :param table: 表名
        :param fields: 字段名
        :param values: 值
        :param database: 数据库名
        :return: 查询到的结果（单条）
        """
        return super().query(table, fields, values, database)

    @property
    def exist(self) -> bool:
        """创建只读属性exist，该属性用于判断是否在idle_fish表中是否存在指定工号的所对应的数据行

        :return: 若存在返回True，否则返回False
        """
        return Account.query(
            f'select 1 from `idle_fish` where `Job_N`="{self.job_number}" limit 1') == (1,)

    @classmethod
    def exist_record(cls, job_number) -> bool:
        """根据工号判断是否存在指定记录

        :param job_number: 工号
        :return: 若存在返回True，否则返回False
        """
        return Account.query(
            f'select 1 from `idle_fish` where `Job_N`="{job_number}" limit 1') == (1,)


# pylint: disable=too-many-instance-attributes
class CreateRecordIdleFish(Create):
    """record_idle_fish表的增类：往数据库中的record_idle_fish表中新增数据"""

    # pylint: disable=too-many-arguments
    def __init__(self, today, job_number, role, hosts, version, coins, user_name,
                 today_global_ipv4_addr):
        """构造函数：初始化增类的对象

        :param today: 今天的日期
        :param job_number: 工号
        :param role: 角色
        :param hosts: 主机列表
        :param version: 版本号
        :param coins: 闲鱼币
        :param user_name: 闲鱼账号的会员名
        :param today_global_ipv4_addr: 今日的公网IPv4地址
        """
        self.today = today
        self.job_number = job_number
        self.role = role
        self.hosts = hosts
        self.version = version
        self.coins = coins
        self.user_name = user_name
        self.today_global_ipv4_addr = today_global_ipv4_addr
        if self.exist:
            print(f'记录today={self.today}, job_number={self.job_number}已存在，无需重复创建')
            return
        self.query(
            'record_idle_fish',
            (
                'record_date', 'Job_N', 'role', 'hosts', 'version', 'coins',
                'user_name', 'today_global_ipv4_addr'),
            (
                str(self.today), self.job_number, self.role, self.hosts, self.version, self.coins,
                self.user_name, self.today_global_ipv4_addr)
        )

    @classmethod
    def query(cls, table, fields, values, database=Record):
        """查询函数：新增数据

        :param table: 表名
        :param fields: 字段名
        :param values: 值
        :param database: 数据库名
        :return: 查询到的结果（单条）
        """
        return super().query(table, fields, values, database)

    @property
    def exist(self):
        """创建只读属性exist，该属性用于判断是否存在快手极速版数据库中存在指定设备的数据"""
        return Record.query(
            f'select 1 from `record_idle_fish` where `record_date`="{self.today}" and `Job_N`='
            f'"{self.job_number}" limit 1'
        ) == (1,)


# pylint: disable=too-many-instance-attributes
class CreateRecordDispatch(Create):
    """record_dispatch表的增类：往数据库中的record_dispatch表中新增数据"""

    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(
            self, dispatch_date, job_number,
            dispatch_time, role,
            user_name, pay_pw,
            if_mn, buy_coins,
            buy_date, buy_time,
            dispatch_consignee, confirm_date,
            confirm_time, base_payee,
            middle_payee
    ):
        """构造函数：初始化增类的对象

        :param dispatch_date: 发货的日期
        :param job_number: 工号
        :param dispatch_time: 发货的时间
        :param role: 角色
        :param user_name: 闲鱼账号的会员名
        :param pay_pw: 支付密码
        :param if_mn: 闲鱼绑定的手机号
        :param buy_coins: 购买时所消耗的闲鱼币
        :param buy_date: 上次购买的日期
        :param buy_time: 上次购买的时间
        :param dispatch_consignee: 发货时的收货人
        :param confirm_date: 确认收货的日期
        :param confirm_time: 确认收货的时间
        :param base_payee: 基层收款人
        :param middle_payee: 中层收款人
        """
        self.dispatch_date = str(dispatch_date)
        self.job_number = job_number
        if self.exist:
            print(f'记录dispatch_date={self.dispatch_date}, '
                  f'job_number={self.job_number}已存在，无需重复创建')
            return
        self.dispatch_time = dispatch_time
        self.role = role
        self.user_name = user_name
        self.pay_pw = pay_pw
        self.buy_coins = buy_coins
        self.buy_date = str(buy_date)
        self.buy_time = str(buy_time)
        self.dispatch_consignee = dispatch_consignee
        self.confirm_date = str(confirm_date)
        self.confirm_time = confirm_time
        fields = [
                'dispatch_date', 'Job_N', 'dispatch_time', 'role', 'user_name',
                'pay_pw', 'buy_coins', 'buy_date', 'buy_time', 'dispatch_consignee',
                'confirm_date', 'confirm_time'
            ]
        values = [
                self.dispatch_date, self.job_number, self.dispatch_time, self.role, self.user_name,
                self.pay_pw, self.buy_coins, self.buy_date, self.buy_time, self.dispatch_consignee,
                self.confirm_date, self.confirm_time
            ]
        if if_mn:
            self.if_mn = if_mn
            fields.append('if_mn')
            values.append(self.if_mn)
        if base_payee:
            self.base_payee = base_payee
            fields.append('base_payee')
            values.append(self.base_payee)
        if middle_payee:
            self.middle_payee = middle_payee
            fields.append('middle_payee')
            values.append(self.middle_payee)
        self.query(table='record_dispatch', fields=tuple(fields), values=tuple(values))

    @classmethod
    def query(cls, table, fields, values, database=Record):
        """查询函数：新增数据

        :param table: 表名
        :param fields: 字段名
        :param values: 值
        :param database: 数据库名
        :return: 查询到的结果（单条）
        """
        return super().query(table, fields, values, database)

    @property
    def exist(self):
        """创建只读属性exist，该属性用于判断是否在record_dispatch表中存在指定的记录"""
        return Record.query(
            f'select 1 from `record_dispatch` where `dispatch_date`="{self.dispatch_date}" and '
            f'`Job_N`="{self.job_number}" limit 1'
        ) == (1,)


# pylint: disable=too-few-public-methods
class CreateMobile(Create):
    """增类：往数据库中新增数据"""

    def __init__(self, device_sn):
        """构造函数：初始化增类的对象

        :param device_sn: 设备序列号
        """
        self.device_sn = device_sn

    @classmethod
    def query(cls, table, fields, values, database=Mobile):
        """查询函数：新增数据

        :param table: 表名
        :param fields: 字段名
        :param values: 值
        :param database: 数据库名
        :return: 查询到的结果（单条）
        """
        return super().query(table, fields, values, database)


class CreateKSJSB(CreateMobile):
    """增类：往快手极速版数据库中新增数据"""

    def __init__(self, device_sn):
        """构造函数：初始化增类的对象

        :param device_sn: 设备序列号
        """
        super().__init__(device_sn)
        if self.exist:
            return
        self.query('ksjsb', ('SN', 'gold_coins', 'cash_coupons'), (device_sn, 0, 0))

    @property
    def exist(self):
        """创建只读属性exist，该属性用于判断是否存在快手极速版数据库中存在指定设备的数据"""
        return Mobile.query(f'select 1 from `ksjsb` where `SN` = {self.device_sn} limit 1') == (1,)
