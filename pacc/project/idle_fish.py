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
            if self.uia_ins.click(content_desc='待发货'):
                success_cnt += 1
            self.uia_ins.click('com.taobao.idlefish:id/right_text')
            self.uia_ins.click(text='继续')
            self.adb_ins.press_back_key()
            self.adb_ins.press_back_key()
