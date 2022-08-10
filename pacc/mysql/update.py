"""MySQL数据库包的改模块"""
from datetime import datetime
from .mysql import Mobile
from .retrieve import RetrieveKsjsb


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
        print(self.query('IP', ipv4_addr))

    def update_model(self, model):
        """更新手机的型号

        :param model: 新的型号
        """
        print(self.query('Model', model))


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

    def update_last_treasure_box_datetime(self, last_treasure_box_datetime=datetime.now()):
        """更新上一次打开宝箱的日期和时间

        :param last_treasure_box_datetime: 上一次打开宝箱的日期和时间
        """
        self.dbr.last_treasure_box_datetime = last_treasure_box_datetime
        print(self.query('last_treasure_box_datetime', last_treasure_box_datetime))

    def update_last_sign_in_date(self, last_sign_in_date):
        """更新上一次签完到的日期

        :param last_sign_in_date: 上一次签完到的日期
        """
        self.dbr.last_sign_in_date = last_sign_in_date
        print(self.query('last_sign_in_date', last_sign_in_date))

    def update_last_change_money_date(self, last_change_money_date):
        """更新上一次把金币兑换钱的日期

        :param last_change_money_date: 上一次把金币兑换钱的日期
        """
        self.dbr.last_change_money_date = last_change_money_date
        print(self.query('last_change_money_date', last_change_money_date))

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

    def update_last_update_wealth_date(self, last_update_wealth_date):
        """更新上一次更新完财富值的日期

        :param last_update_wealth_date: 上一次更新完财富值的日期
        """
        self.dbr.last_update_wealth_date = last_update_wealth_date
        print(self.query('last_update_wealth_date', last_update_wealth_date))

    def update_last_meal_allowance_datetime(self, last_meal_allowance_datetime=datetime.now()):
        """更新上一次领完饭补的日期和时间

        :param last_meal_allowance_datetime: 上一次领完饭补的日期和时间
        """
        self.dbr.last_meal_allowance_datetime = last_meal_allowance_datetime
        print(self.query('last_meal_allowance_datetime', last_meal_allowance_datetime))

    def update_last_flash_benefits_date(self, last_flash_benefits_date):
        """更新上一次领完限时福利的日期

        param last_flash_benefits_date: 上一次领完限时福利的日期
        """
        self.dbr.last_flash_benefits_date = last_flash_benefits_date
        print(self.query('last_flash_benefits_date', last_flash_benefits_date))

    def update_last_desktop_component_date(self, last_desktop_component_date):
        """更新上一次领完桌面组件奖励的日期

        param last_desktop_component_date: 上一次领完桌面组件奖励的日期
        """
        self.dbr.last_desktop_component_date = last_desktop_component_date
        print(self.query('last_desktop_component_date', last_desktop_component_date))
