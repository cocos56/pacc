"""闲鱼中控模块"""
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


class IdleFish(Project):
    """闲鱼中控类"""

    def open_app(self):
        """打开闲鱼APP"""
        self.free_memory()
        self.adb_ins.open_app(Activity.MainActivity)
        sleep(5)

    def change_price(self, end_num=8):
        """改价

        :param end_num: 结束的数量
        """
        success_cnt = 0
        while True:
            print(f'success_cnt={success_cnt}')
            if success_cnt >= end_num:
                break
            self.open_app()
            self.adb_ins.get_current_focus()
            self.uia_ins.click(content_desc='我的，未选中状态')
            self.uia_ins.click(content_desc='我卖出的')
            self.uia_ins.click(content_desc='待付款')
            self.uia_ins.click(content_desc='修改价格')
            dic = self.uia_ins.get_dict(class_='android.widget.EditText')
            try:
                src_price = float(dic['@text'])
            except TypeError as err:
                print_err(err)
                continue
            if str(src_price)[-1] == '1':
                continue
            price = src_price / 10 + 0.01
            print(f'price={price}')
            self.uia_ins.click(class_='android.widget.EditText')
            self.adb_ins.input_text(price)
            self.uia_ins.click(content_desc='确定修改')
            self.uia_ins.click(content_desc='确定', index='1')
            self.uia_ins.get_current_ui_hierarchy()
            success_cnt += 1
            sleep(30)

    def dispatch(self, end_num=8):
        """发货

        :param end_num: 结束的数量
        """
        success_cnt = 0
        self.open_app()
        while True:
            print(f'success_cnt={success_cnt}')
            if success_cnt >= end_num:
                break
            self.uia_ins.click(content_desc='我的，未选中状态')
            self.uia_ins.click(content_desc='我卖出的')
            self.uia_ins.click(content_desc='待发货')
            self.uia_ins.click(content_desc='去发货')
            self.uia_ins.click('com.taobao.idlefish:id/right_text')
            if self.uia_ins.click(text='继续'):
                success_cnt += 1
            self.adb_ins.press_back_key()
            self.adb_ins.press_back_key()
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
