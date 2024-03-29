"""MySQL数据库包的改模块"""
from datetime import date

from .mysql import Mobile, Account, Record
from .retrieve import RetrieveKsjsb, RetrieveMobileInfo


# pylint: disable=too-few-public-methods
class Update:
    """MySQL数据库包的改模块的改类"""

    def __init__(self, serial_num):
        """构造函数：初始化改类的对象

        :param serial_num: 设备序列号
        """
        self.serial_num = serial_num

    def query(self, field, value, table):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :param table: 表名
        :return: 修改的结果
        """
        cmd = f'update `{table}` set `{field}` = "{value}" where `SN` = "{self.serial_num}"'
        print(cmd)
        res = Mobile.query(cmd)
        Mobile.commit()
        return res


class UpdateMobileInfo(Update):
    """更改手机信息类"""

    def __init__(self, serial_num):
        """构造函数：初始化改类的对象

        :param serial_num: 设备序列号
        """
        super().__init__(serial_num)
        self.dbr = RetrieveMobileInfo.get_ins(serial_num)

    def query(self, field, value, table='mobile_info'):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :param table: 表名
        :return: 修改的结果
        """
        return super().query(field, value, table)

    def update_ipv4_addr(self, ipv4_addr):
        """更新手机的IPv4地址

        :param ipv4_addr: 新的IPv4地址
        """
        self.dbr.ipv4_addr = ipv4_addr
        print(self.query('IP', ipv4_addr))

    def update_model(self, model):
        """更新手机的型号

        :param model: 新的型号
        """
        self.dbr.model = model
        print(self.query('model', model))

    def update_last_reboot_date(self, last_reboot_date):
        """更新上次重启的日期

        :param last_reboot_date: 上次重启的日期
        """
        self.dbr.last_reboot_date = last_reboot_date
        print(self.query('last_reboot_date', last_reboot_date))


class UpdateKsjsb(Update):
    """更改快手极速版信息类"""

    def __init__(self, serial_num):
        """构造函数：初始化改类的对象

        :param serial_num: 设备序列号
        """
        super().__init__(serial_num)
        self.dbr = RetrieveKsjsb.instances.get(self.serial_num)

    def query(self, field, value, table='ksjsb'):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :param table: 表名
        :return: 修改的结果
        """
        return super().query(field, value, table)

    def update_gold_coins(self, gold_coins):
        """更新金币值

        :param gold_coins: 金币
        """
        self.dbr.gold_coins = gold_coins
        print(self.query('gold_coins', gold_coins))

    def update_cash_coupons(self, cash_coupons):
        """更新现金值

        :param cash_coupons: 现金
        """
        self.dbr.cash_coupons = cash_coupons
        print(self.query('cash_coupons', cash_coupons))

    def update_last_sign_in_date(self, last_sign_in_date):
        """更新上一次签完到的日期

        :param last_sign_in_date: 上一次签完到的日期
        """
        self.dbr.last_sign_in_date = last_sign_in_date
        print(self.query('last_sign_in_date', last_sign_in_date))

    def update_version_info(self, version_info):
        """更新版本信息

        :param version_info: 版本信息
        """
        self.dbr.version_info = version_info
        print(self.query('version_info', version_info))

    def update_last_double_bonus_date(self, last_double_bonus_date):
        """更新上一次点击翻倍的日期

        :param last_double_bonus_date: 上一次点击翻倍的日期
        """
        self.dbr.last_double_bonus_date = last_double_bonus_date
        print(self.query('last_double_bonus_date', last_double_bonus_date))

    def update_last_treasure_box_date(self, last_treasure_box_date):
        """更新上一次开完宝箱的日期

        :param last_treasure_box_date: 上一次开完宝箱的日期
        """
        self.dbr.last_treasure_box_date = last_treasure_box_date
        print(self.query('last_treasure_box_date', last_treasure_box_date))

    def update_last_view_ads_date(self, last_view_ads_date):
        """更新上一次看完广告的日期

        :param last_view_ads_date: 上一次看完广告的日期
        """
        self.dbr.last_view_ads_date = last_view_ads_date
        print(self.query('last_view_ads_date', last_view_ads_date))

    def update_last_watch_live_date(self, last_watch_live_date):
        """更新上一次看完直播的日期

        :param last_watch_live_date: 上一次看完直播的日期
        """
        self.dbr.last_watch_live_date = last_watch_live_date
        print(self.query('last_watch_live_date', last_watch_live_date))

    def update_last_shopping_date(self, last_shopping_date):
        """更新上一次逛完街的日期

        :param last_shopping_date: 上一次逛完街的日期
        """
        self.dbr.last_shopping_date = last_shopping_date
        print(self.query('last_shopping_date', last_shopping_date))

    def update_last_meal_allowance_datetime(self, last_meal_allowance_datetime):
        """更新上一次领完饭补的日期和时间

        :param last_meal_allowance_datetime: 上一次领完饭补的日期和时间
        """
        self.dbr.last_meal_allowance_datetime = last_meal_allowance_datetime
        print(self.query('last_meal_allowance_datetime', last_meal_allowance_datetime))

    def update_last_desktop_component_date(self, last_desktop_component_date):
        """更新上一次领完桌面组件奖励的日期

        param last_desktop_component_date: 上一次领完桌面组件奖励的日期
        """
        self.dbr.last_desktop_component_date = last_desktop_component_date
        print(self.query('last_desktop_component_date', last_desktop_component_date))

    def update_last_buy_things_date(self, last_buy_things_date):
        """更新上一次领完金币购划算内所有奖励的日期

        param last_buy_things_date: 上一次领完金币购划算内所有奖励的日期
        """
        self.dbr.last_buy_things_date = last_buy_things_date
        print(self.query('last_buy_things_date', last_buy_things_date))

    def update_last_change_money_date(self, last_change_money_date):
        """更新上一次把金币兑换钱的日期

        :param last_change_money_date: 上一次把金币兑换钱的日期
        """
        self.dbr.last_change_money_date = last_change_money_date
        print(self.query('last_change_money_date', last_change_money_date))

    def update_last_update_wealth_date(self, last_update_wealth_date):
        """更新上一次更新完财富值的日期

        :param last_update_wealth_date: 上一次更新完财富值的日期
        """
        self.dbr.last_update_wealth_date = last_update_wealth_date
        print(self.query('last_update_wealth_date', last_update_wealth_date))

    def update_last_watch_video_date(self, last_watch_video_date):
        """更新上一次看视频赚完金币的日期

        :param last_watch_video_date: 上一次看视频赚完金币的日期
        """
        self.dbr.last_watch_video_date = last_watch_video_date
        print(self.query('last_watch_video_date', last_watch_video_date))


class UpdateIdleFishBase:
    """该类用于为修改account数据库中的idle_fish表中的数据提供基础支持"""

    def __init__(self, job_number):
        """构造函数：初始化改类的对象

        :param job_number: 工号
        """
        self.job_number = job_number

    def query(self, field, value, table):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :param table: 表名
        :return: 修改的结果
        """
        cmd = f'update `{table}` set `{field}` = "{value}" where `Job_N` = "{self.job_number}"'
        print(cmd)
        res = Account.query(cmd)
        Account.commit()
        return res

    def query2(self, field, value, table):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :param table: 表名
        :return: 修改的结果
        """
        cmd = f'update `{table}` set `{field}` = {value} where `Job_N` = "{self.job_number}"'
        print(cmd)
        res = Account.query(cmd)
        Account.commit()
        return res


class UpdateIdleFish(UpdateIdleFishBase):  # pylint: disable=too-many-public-methods
    """该类用于修改account数据库中的idle_fish表中的数据"""

    def query(self, field, value, table='idle_fish'):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :param table: 表名
        :return: 修改的结果
        """
        return super().query(field, value, table)

    def query2(self, field, value, table='idle_fish'):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :param table: 表名
        :return: 修改的结果
        """
        return super().query2(field, value, table)

    def update_role(self, role: str) -> None:
        """更新设备在数据库中的角色值

        :param role: 最新的设备的角色值
        """
        print(self.query('role', role))

    def update_hosts(self, hosts: str) -> None:
        """更新设备在数据库中的主机列表值

        :param hosts: 最新的设备所在主机列表值
        """
        print(self.query('hosts', hosts))

    def update_version(self, version='NULL') -> None:
        """更新设备的版本号

        :param version: 新的版本号，version只能为字符串，且当version的值为NULL时会将数据库里的值置为空
        """
        if version != 'NULL':
            print(self.query('version', version))
        else:
            print(self.query2('version', version))

    def update_coins(self, coins: int) -> None:
        """更新设备的闲鱼币币值

        :param coins: 最新状态的闲鱼币币值
        """
        print(self.query('coins', coins))

    def update_reminder_threshold(self, reminder_threshold: int) -> None:
        """更新设备的提醒阈值

        :param reminder_threshold: 最新状态下的提醒阈值
        """
        print(self.query('RT', reminder_threshold))

    def update_if_mn(self, if_mn):
        """更新设备的闲鱼绑定的手机号（Idle Fish Mobile Number）

        :param if_mn: 新的闲鱼绑定的手机号（Idle Fish Mobile Number）
        """
        print(self.query('if_mn', if_mn))

    def update_nickname(self, nickname) -> None:
        """更新设备上闲鱼账号的昵称

        :param nickname: 闲鱼账号的新昵称
        """
        print(self.query('nickname', nickname))

    def update_last_update_nn_date(self, last_update_nn_date: date.today()) -> None:
        """更新设备的上次运行日期

        :param last_update_nn_date: 新的上次更新昵称的日期
        """
        print(self.query('last_update_nn_date', last_update_nn_date))

    def update_last_update_nn_time(self, last_update_nn_time: str) -> None:
        """更新设备的上次更新昵称的时间

        :param last_update_nn_time: 新上次更新昵称的时间
        """
        print(self.query('last_update_nn_time', last_update_nn_time))

    def update_last_run_date(self, last_run_date: date.today()) -> None:
        """更新设备的上次运行日期

        :param last_run_date: 新的上次运行日期
        """
        print(self.query('last_run_date', last_run_date))

    def update_last_run_time(self, last_run_time: str) -> None:
        """更新设备上次运行的时间

        :param last_run_time: 新上次运行的时间
        """
        print(self.query('last_run_time', last_run_time))

    def update_last_check_date(self, last_check_date: date.today()) -> None:
        """更新设备上次检查的日期

        :param last_check_date: 新上次检查的日期
        """
        print(self.query('last_check_date', last_check_date))

    def update_last_check_time(self, last_check_time: str) -> None:
        """更新设备上次检查的时间

        :param last_check_time: 新上次运行的时间
        """
        print(self.query('last_check_time', last_check_time))

    def update_last_bak_date(self, last_bak_date: date.today()) -> None:
        """更新设备的上次备份日期

        :param last_bak_date: 新的上次备份日期
        """
        print(self.query('last_bak_date', last_bak_date))

    def update_last_bak_time(self, last_bak_time: str) -> None:
        """更新设备上次备份的时间

        :param last_bak_time: 新的上次备份的时间
        """
        print(self.query('last_bak_time', last_bak_time))

    def update_today_global_ipv4_addr(self, today_global_ipv4_addr: str) -> None:
        """更新设备的本机今日公网IPv4地址

        :param today_global_ipv4_addr: 本机今日的公网IPv4地址
        """
        print(self.query('today_global_ipv4_addr', today_global_ipv4_addr))

    def update_last_update_ip_date(self, last_update_ip_date: date.today()) -> None:
        """更新设备上次更新本机公网IPv4地址的日期

        :param last_update_ip_date: 上次更新本机公网IPv4地址的日期
        """
        print(self.query('last_update_ip_date', last_update_ip_date))

    def update_last_update_hosts_date(self, last_update_hosts_date: date.today()):
        """更新设备在数据库中上次更新主机列表值的日期

        :param last_update_hosts_date: 上次更新主机列表值的日期
        """
        print(self.query('last_update_hosts_date', last_update_hosts_date))

    def update_last_update_version_date(self, last_update_version_date: date.today()):
        """更新设备在数据库中上次更新版本号的日期

        :param last_update_version_date: 上次更新版本号的日期
        """
        print(self.query('last_update_version_date', last_update_version_date))

    def update_login(self, login='NULL') -> None:
        """更新设备是否需要登录的标志

        :param login: 是否需要登录的标志，login只能为NULL或者1，其中NULL代表在线，1代表离线
        """
        print(self.query2('login', login))

    def update_last_login_date(self, last_login_date: date.today()):
        """更新设备在数据库中上次登录的日期

        :param last_login_date: 上次登录的日期
        """
        print(self.query('last_login_date', last_login_date))

    def update_last_login_ipv4_addr(self, last_login_ipv4_addr):
        """更新设备上次登录的公网IPv4地址

        :param last_login_ipv4_addr: 上次登录的公网IPv4地址
        """
        print(self.query('last_login_ipv4_addr', last_login_ipv4_addr))

    def update_create(self, create):
        """更新设备是否需要创建的标志

        :param create: 是否需要创建的标志
        """
        print(self.query2('create', create))

    def update_last_create_date(self, last_create_date: date.today()):
        """更新设备在数据库中上次创建的日期

        :param last_create_date: 上次创建的日期
        """
        print(self.query('last_create_date', last_create_date))

    def update_buy(self, buy='NULL') -> None:
        """更新设备是否需要购买的标志

        :param buy: 是否需要购买的标志，buy只能为NULL或者1，其中NULL代表无需购买，1代表需要购买
        """
        print(self.query2('buy', buy))

    def update_last_buy_date(self, last_buy_date: date.today()) -> None:
        """更新设备在数据库中上次购买的日期

        :param last_buy_date: 上次购买的日期
        """
        print(self.query('last_buy_date', last_buy_date))

    def update_last_buy_time(self, last_buy_time: str) -> None:
        """更新设备在数据库中上次购买的时间

        :param last_buy_time: 上次购买的时间
        """
        print(self.query('last_buy_time', last_buy_time))

    def update_last_buy_coins(self, last_buy_coins: int) -> None:
        """更新设备上次购买时所消耗的闲鱼币

        :param last_buy_coins: 上次购买时所消耗的闲鱼币
        """
        print(self.query('last_buy_coins', last_buy_coins))

    def update_last_buy_consignee(self, last_buy_consignee: str) -> None:
        """更新设备上次购买时的收货人

        :param last_buy_consignee: 上次购买时的收货人
        """
        print(self.query('last_buy_consignee', last_buy_consignee))

    def update_last_buy_order_num(self, last_buy_order_num: str) -> None:
        """更新设备上次购买时的订单编号

        :param last_buy_order_num: 上次购买时的订单编号
        """
        print(self.query('last_buy_order_num', last_buy_order_num))

    def update_last_change_price_date(self, last_change_price_date: date.today()) -> None:
        """更新设备上次改价的日期

        :param last_change_price_date: 上次改价的日期
        """
        print(self.query('last_change_price_date', last_change_price_date))

    def update_last_dispatch_date(self, last_dispatch_date: date.today()) -> None:
        """更新设备上次发货的日期

        :param last_dispatch_date: 上次发货的日期
        """
        print(self.query('last_dispatch_date', last_dispatch_date))

    def update_last_dispatch_time(self, last_dispatch_time: str) -> None:
        """更新设备上次发货的时间

        :param last_dispatch_time: 上次发货的时间
        """
        print(self.query('last_dispatch_time', last_dispatch_time))

    def update_confirm(self, confirm='NULL') -> None:
        """更新设备是否需要确认收货的标志

        :param confirm: 是否需要确认收货的标志，confirm只能为NULL或者1，其中NULL代表无需确认收货，1代表需要
        """
        print(self.query2('confirm', confirm))

    def update_last_confirm_date(self, last_confirm_date: date.today()) -> None:
        """更新设备在数据库中上次确认收货的日期

        :param last_confirm_date: 上次确认收货的日期
        """
        print(self.query('last_confirm_date', last_confirm_date))

    def update_last_hvc_date(self, last_hvc_date: date.today()) -> None:
        """更新设备在数据库中上次有码的日期

        :param last_hvc_date: 上次有码的日期
        """
        print(self.query('last_hvc_date', last_hvc_date))

    def update_last_nvc_date(self, last_nvc_date: date.today()) -> None:
        """更新设备在数据库中上次无码的日期

        :param last_nvc_date: 上次无码的日期
        """
        print(self.query('last_nvc_date', last_nvc_date))

    def update_last_top_up_mobile_date(self, last_top_up_mobile_date: date.today()):
        """更新设备在数据库中上次薅羊毛赚话费的日期

        :param last_top_up_mobile_date: 上次薅羊毛赚话费的日期
        """
        print(self.query('last_top_up_mobile_date', last_top_up_mobile_date))

    def update_top_up_mobile_cnt(self, top_up_mobile_cnt: int):
        """更新设备在数据库中执行薅羊毛赚话费任务成功的次数

        :param top_up_mobile_cnt: 执行薅羊毛赚话费任务成功的次数
        """
        print(self.query2('top_up_mobile_cnt', top_up_mobile_cnt))


class UpdateIdleFishStaffBase:
    """该类用于为修改account数据库中的idle_fish_staff表中的数据提供基础支持"""

    def __init__(self, name):
        """构造函数：初始化改类的对象

        :param name: 员工姓名
        """
        self.name = name

    def query(self, field, value, table):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :param table: 表名
        :return: 修改的结果
        """
        cmd = f'update `{table}` set `{field}` = "{value}" where `name` = "{self.name}"'
        print(cmd)
        res = Account.query(cmd)
        Account.commit()
        return res


class UpdateIdleFishStaff(UpdateIdleFishStaffBase):
    """该类用于修改account数据库中的idle_fish_staff表中的数据"""

    def query(self, field, value, table='idle_fish_staff'):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :param table: 表名
        :return: 修改的结果
        """
        return super().query(field, value, table)

    def update_last_salary_amount(self, last_salary_amount: float) -> None:
        """更新设备在数据库中上次发工资时的钱数

        :param last_salary_amount: 上次发工资时的钱数
        """
        print(self.query('last_salary_amount', last_salary_amount))

    def update_last_salary_date(self, last_salary_date: date) -> None:
        """更新设备在数据库中上次发工资时的日期

        :param last_salary_date: 上次发工资时的日期
        """
        print(self.query('last_salary_date', last_salary_date))

    def update_last_salary_time(self, last_salary_time: str) -> None:
        """更新设备在数据库中上次发工资时的时间

        :param last_salary_time: 上次发工资时的时间
        """
        print(self.query('last_salary_time', last_salary_time))

    def update_last_npps_amount(self, last_npps_amount: float) -> None:
        """更新设备在数据库中上次针对于没有支付密码的发工资时的钱数（NPPS：No Pay Password Salary）

        :param last_npps_amount: 上次针对于没有支付密码的发工资时的钱数（NPPS：No Pay Password Salary）
        """
        print(self.query('last_npps_amount', last_npps_amount))

    def update_last_npps_date(self, last_npps_date: date) -> None:
        """更新设备在数据库中上次针对于没有支付密码的发工资时的日期（NPPS：No Pay Password Salary）

        :param last_npps_date: 上次针对于没有支付密码的发工资时的日期（NPPS：No Pay Password Salary）
        """
        print(self.query('last_npps_date', last_npps_date))

    def update_last_npps_time(self, last_npps_time: str) -> None:
        """更新设备在数据库中上次针对于没有支付密码的发工资时的时间（NPPS：No Pay Password Salary）

        :param last_npps_time: 上次针对于没有支付密码的发工资时的时间（NPPS：No Pay Password Salary）
        """
        print(self.query('last_npps_time', last_npps_time))


class UpdateRecordDispatchBase:
    """该类用于为修改record数据库中的record_dispatch表中的数据提供基础支持"""

    def __init__(self, user_name):
        """构造函数：初始化改类的对象

        :param user_name: 用户名
        """
        self.user_name = user_name

    def query(self, field, value, table):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :param table: 表名
        :return: 修改的结果
        """
        cmd = f'update `{table}` set `{field}` = "{value}" where `user_name` = "{self.user_name}"' \
              f' and confirm_date = CURDATE()'
        print(cmd)
        res = Record.query(cmd)
        Record.commit()
        return res


class UpdateRecordDispatch(UpdateRecordDispatchBase):
    """更新发货记录类：该类用于修改record数据库中的record_dispatch表中的数据"""

    def query(self, field, value, table='record_dispatch'):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :param table: 表名
        :return: 修改的结果
        """
        return super().query(field, value, table)

    def update_role(self, role: str) -> None:
        """更新设备在数据库中的角色信息

        :param role: 新的角色信息
        """
        print(self.query('role', role))

    def update_job_number(self, job_number: str) -> None:
        """更新设备在数据库中的工号信息

        :param job_number: 新的工号信息
        """
        print(self.query('Job_N', job_number))

    def update_base_payee(self, base_payee: str) -> None:
        """更新设备在数据库中的基层收款人信息

        :param base_payee: 新的基层收款人
        """
        print(self.query('base_payee', base_payee))

    def update_middle_payee(self, middle_payee: str) -> None:
        """更新设备在数据库中的中层收款人信息

        :param middle_payee: 新的中层收款人信息
        """
        print(self.query('middle_payee', middle_payee))
