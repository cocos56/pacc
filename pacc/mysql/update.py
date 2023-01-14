"""MySQL数据库包的改模块"""
from datetime import date

from .mysql import Mobile, Account
from .retrieve import RetrieveKsjsb, RetrieveMobileInfo


# pylint: disable=too-few-public-methods
class Update:
    """MySQL数据库包的改模块的改类"""

    def __init__(self, serial_num):
        """构造函数：初始化改类的对象

        :param serial_num: 设备序列号
        """
        self.serial_num = serial_num

    def query(self, table, field, value):
        """查询函数：修改数据

        :param table: 表名
        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
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

    # pylint: disable=arguments-differ
    def query(self, field, value):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :return: 修改的结果
        """
        return super().query('mobile_info', field, value)

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

    # pylint: disable=arguments-differ
    def query(self, field, value):
        """查询函数：修改数据

        :param field: 字段名
        :param value: 新值（用于替换原有的旧值）
        :return: 修改的结果
        """
        return super().query('ksjsb', field, value)

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


class UpdateIdleFish(UpdateIdleFishBase):
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

    def update_version(self, version):
        """更新设备的版本号

        :param version: 新的版本号
        """
        print(self.query('version', version))

    def update_coins(self, coins: int):
        """更新设备的闲鱼币币值

        :param coins: 新的闲鱼币币值
        """
        print(self.query('coins', coins))

    def update_if_mn(self, if_mn):
        """更新设备的闲鱼绑定的手机号（Idle Fish Mobile Number）

        :param if_mn: 新的闲鱼绑定的手机号（Idle Fish Mobile Number）
        """
        print(self.query('if_mn', if_mn))

    def update_last_check_date(self, last_check_date: date.today()):
        """更新设备的上次检查日期

        :param last_check_date: 新的上次检查日期
        """
        print(self.query('last_check_date', last_check_date))

    def update_last_run_date(self, last_run_date: date.today()):
        """更新设备的上次运行日期

        :param last_run_date: 新的上次运行日期
        """
        print(self.query('last_run_date', last_run_date))

    def update_last_bak_date(self, last_bak_date):
        """更新设备的上次备份日期

        :param last_bak_date: 新的上次备份日期
        """
        print(self.query('last_bak_date', last_bak_date))

    def update_today_global_ipv4_addr(self, today_global_ipv4_addr):
        """更新设备的本机今日公网IPv4地址

        :param today_global_ipv4_addr: 本机今日的公网IPv4地址
        """
        print(self.query('today_global_ipv4_addr', today_global_ipv4_addr))

    def update_last_update_ip_date(self, last_update_ip_date):
        """更新设备上次更新本机公网IPv4地址的日期

        :param last_update_ip_date: 上次更新本机公网IPv4地址的日期
        """
        print(self.query('last_update_ip_date', last_update_ip_date))

    def update_hosts(self, hosts):
        """更新设备在数据库中的主机列表值

        :param hosts: 最新的设备所在主机列表值
        """
        print(self.query('hosts', hosts))

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

    def update_last_top_up_mobile_date(self, last_top_up_mobile_date: date.today()):
        """更新设备在数据库中上次薅羊毛赚话费的日期

        :param last_top_up_mobile_date: 上次薅羊毛赚话费的日期
        """
        print(self.query('last_top_up_mobile_date', last_top_up_mobile_date))

    def update_login(self, login):
        """更新设备是否需要登录的标志

        :param login: 是否需要登录的标志
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
