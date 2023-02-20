"""闲鱼中控模块"""
from os import listdir, remove
from os.path import join
from random import randint
from xml.parsers.expat import ExpatError

from .project import Project
from ..base import sleep, print_err

ROOT = 'com.taobao.idlefish/com.taobao.idlefish.maincontainer.activity.'


class Activity:  # pylint: disable=too-few-public-methods
    """闲鱼中控模块的安卓活动名类"""
    MainActivity = f'{ROOT}MainActivity'  # 主界面


class ResourceID:  # pylint: disable=too-few-public-methods
    """闲鱼中控模块的安卓资源ID类"""
    tab_title = 'com.taobao.idlefish:id/tab_title'
    btn_transfer = 'com.taobao.idlefish:id/btn_transfer'
    publish_rate = 'com.taobao.idlefish:id/publish_rate'
    right_btn = 'com.taobao.idlefish:id/right_btn'


def get_random_aps():
    """获取所有支付宝的代付码

    :return: 所有支付宝的代付码
    """
    ap_li = []
    for i in listdir(r'D:\aps')[::-1]:
        spli = i.split('.')
        if spli and spli[-1] == 'png':
            ap_li.append(i)
    return ap_li


class IdleFish(Project):
    """闲鱼中控类"""

    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备编号
        """
        super().__init__(serial_num)
        self.walked_li = []

    def get_random_ap(self, random_err=0):
        """随机获取一个支付宝的代付码

        :param random_err: 错误的数量
        :return: 当代付码存在时会尽可能地随机返回一个未曾遍历过的代付码，当代付码不存在时直接返回False
        """
        ap_li = get_random_aps()
        if ap_li:
            random_ap = ap_li[randint(0, len(ap_li) - 1)]
            if len(ap_li) <= len(self.walked_li):
                self.walked_li = []
            if random_err > 10 or random_ap not in self.walked_li:
                self.walked_li.append(random_ap)
                return random_ap
            return self.get_random_ap(random_err+1)
        return None

    def open_app(self):
        """打开闲鱼APP"""
        self.free_memory()
        self.adb_ins.open_app(Activity.MainActivity)
        sleep(5)

    def pay(self):
        """付款"""
        time_cnt = 0
        while True:
            random_ap = self.get_random_ap()
            if not random_ap:
                print(f'time_cnt={time_cnt}')
                sleep(10)
                time_cnt += 10
                continue
            alipay_code = join(r'D:\aps', random_ap)
            print(alipay_code)
            print(self.walked_li)
            self.adb_ins.push_pic(alipay_code)
            self.free_memory()
            self.uia_ins.click(text='支付宝', interval=15)
            try:
                self.uia_ins.click(text='扫一扫')
            except (FileNotFoundError, ExpatError) as err:
                print_err(err)
                continue
            self.uia_ins.tap((939, 1399))
            self.uia_ins.click('com.alipay.mobile.beephoto:id/iv_photo')
            self.uia_ins.click('com.alipay.mobile.beephoto:id/bt_finish', interval=12)
            try:
                if not self.uia_ins.click(text='确认付款', index='8', interval=2) and not self.\
                        uia_ins.click(text='确认付款', index='9', xml=self.uia_ins.xml, interval=2):
                    if self.uia_ins.get_dict(text='已支付', xml=self.uia_ins.xml):
                        remove(alipay_code)
                        continue
                self.uia_ins.click(text='继续支付', interval=3)
                if not self.uia_ins.click(text='确认交易'):
                    continue
            except FileNotFoundError as err:
                print_err(err)
                continue
            self.uia_ins.click('com.alipay.mobile.antui:id/au_num_1', interval=0.01)
            for i in '39499':
                self.uia_ins.click(f'com.alipay.mobile.antui:id/au_num_{i}',
                                   xml=self.uia_ins.xml, interval=0.01)
            sleep(5)
            if self.uia_ins.get_dict(text='代付成功'):
                remove(alipay_code)

    def change_price(self, dispatch=True):
        """改价"""
        success_cnt = 0
        time_cnt = 0
        while True:
            print(f'success_cnt={success_cnt}, time_cnt={time_cnt}')
            random_aps = get_random_aps()
            print(f'random_aps={random_aps}')
            if not random_aps:
                time_cnt += 1
                sleep(1)
                continue
            time_cnt = 0
            self.open_app()
            self.adb_ins.get_current_focus()
            self.uia_ins.click(content_desc='我的，未选中状态', interval=0.01)
            self.uia_ins.click(content_desc='我卖出的', interval=0.01)
            self.uia_ins.click(content_desc='待付款', interval=0.01)
            self.uia_ins.click(content_desc='修改价格', interval=0.01)
            dic = self.uia_ins.get_dict(class_='android.widget.EditText')
            try:
                src_price = float(dic['@text'])
            except TypeError as err:
                print_err(err)
                if not dispatch:
                    continue
                if self.uia_ins.click(content_desc='待发货', interval=0.01) and self.uia_ins.click(
                        content_desc='去发货', interval=0.01):
                    self.uia_ins.click('com.taobao.idlefish:id/right_text', interval=0.01)
                    self.uia_ins.click(text='继续', interval=0.01)
                continue
            if str(src_price)[-1] == '1':
                if not dispatch:
                    continue
                self.adb_ins.press_back_key(0.01)
                if self.uia_ins.click(content_desc='待发货', interval=0.01) and self.uia_ins.click(
                        content_desc='去发货', interval=0.01):
                    self.uia_ins.click('com.taobao.idlefish:id/right_text', interval=0.01)
                    self.uia_ins.click(text='继续', interval=0.01)
                continue
            price = src_price / 10 + 0.01
            print(f'price={price}')
            self.uia_ins.click(class_='android.widget.EditText', interval=0.01)
            self.adb_ins.input_text(price)
            self.uia_ins.click(content_desc='确定修改', interval=0.01)
            if self.uia_ins.click(content_desc='确定', index='1', interval=0.01):
                success_cnt += 1

    def dispatch(self, err_num=3):
        """发货

        :param err_num: 结束时的连续错误阈值
        """
        err_cnt = success_cnt = 0
        self.open_app()
        while True:
            print(f'success_cnt={success_cnt}, err_cnt={err_cnt}')
            if err_cnt >= err_num:
                break
            if self.uia_ins.click(content_desc='我的，未选中状态', interval=0.01):
                self.uia_ins.xml = ''
            self.uia_ins.click(content_desc='我卖出的', interval=0.01, xml=self.uia_ins.xml)
            self.uia_ins.click(content_desc='待发货', interval=0.01)
            if self.uia_ins.click(content_desc='去发货', interval=0.01):
                success_cnt += 1
                err_cnt = 0
                self.uia_ins.click('com.taobao.idlefish:id/right_text', interval=0.01)
                self.uia_ins.click(text='继续', interval=0.01)
            else:
                err_cnt += 1
            self.adb_ins.press_back_key(0.01)
        self.adb_ins.press_power_key()

    def rate(self, err_num=3):
        """评价

        :param err_num: 结束时的连续错误阈值
        """
        err_cnt = 0
        self.open_app()
        while True:
            print(f'err_cnt={err_cnt}')
            if err_cnt >= err_num:
                self.free_memory()
                self.adb_ins.press_power_key()
                break
            self.uia_ins.click(content_desc='我的，未选中状态', interval=0.01)
            self.uia_ins.click(content_desc='我卖出的', interval=0.01)
            self.uia_ins.click(content_desc='待评价', interval=0.01)
            if not self.uia_ins.click(content_desc='去评价', interval=0.01):
                err_cnt += 1
                self.adb_ins.press_back_key()
                self.adb_ins.press_back_key()
                continue
            err_cnt = 0
            self.uia_ins.click(content_desc='未选中，赏好评', interval=0.01)
            self.uia_ins.click(ResourceID.btn_transfer, '收货快', interval=0.01)
            self.uia_ins.click(
                ResourceID.btn_transfer, '下单爽快', xml=self.uia_ins.xml, interval=0.01)
            self.uia_ins.click(
                ResourceID.btn_transfer, '回复快', xml=self.uia_ins.xml, interval=0.01)
            self.uia_ins.click(
                ResourceID.publish_rate, xml=self.uia_ins.xml, interval=0.01)
            self.uia_ins.click(ResourceID.right_btn, interval=0.01)
            # self.uia_ins.get_current_ui_hierarchy()
            self.adb_ins.press_back_key(0.01)
            self.adb_ins.press_back_key(0.01)
            self.adb_ins.press_back_key(0.01)

    def delete_error_rate_order(self, err_num=3):
        """删除无法评价的订单（超过30天）

        :param err_num: 结束时的连续错误阈值
        """
        err_cnt = 0
        self.open_app()
        self.uia_ins.click(content_desc='我的，未选中状态', interval=0.01)
        self.uia_ins.click(content_desc='我卖出的', interval=0.01)
        self.uia_ins.click(content_desc='待评价', interval=0.01)
        while True:
            print(f'err_cnt={err_cnt}')
            if err_cnt >= err_num:
                self.free_memory()
                self.adb_ins.press_power_key()
                break
            if not self.uia_ins.click(content_desc='更多', interval=0.01):
                err_cnt += 1
                self.adb_ins.press_back_key()
                self.adb_ins.press_back_key()
                self.uia_ins.click(content_desc='我的，未选中状态', interval=0.01)
                self.uia_ins.click(content_desc='我卖出的', interval=0.01)
                self.uia_ins.click(content_desc='待评价', interval=0.01)
                continue
            err_cnt = 0
            self.uia_ins.click(content_desc='删除订单', interval=0.01)
            self.uia_ins.click(ResourceID.right_btn, interval=0.01)
