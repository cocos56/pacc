"""闲鱼全自动刷闲鱼币中央监控系统模块"""
# pylint: disable=too-many-lines
import shutil
from datetime import date, datetime, timedelta
from os import listdir, path, remove, rename
from os.path import join, exists
from xml.parsers.expat import ExpatError

import pyperclip
from PIL import Image
from pyzbar.pyzbar import decode

from .idle_fish_base import Activity, ResourceID, IdleFishBase
from ..adb import LDConsole, LDADB, LDUIA
from ..base import sleep, print_err
from ..mysql import RetrieveIdleFish, RetrieveIdleFishRecords, \
    UpdateIdleFish, CreateRecordIdleFish
from ..tools import create_dir, get_global_ipv4_addr, DiskUsage, CPU


class IdleFish(IdleFishBase):  # pylint: disable=too-many-public-methods
    """闲鱼类"""

    @classmethod
    def backups(cls, start_index, end_index, dir_path='E:/ldbks', reserved_gbs=6 * 1024):
        """批量备份雷电模拟器的设备

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        :param dir_path: 备份文件夹的目录
        :param reserved_gbs: 保留的GB数
        """
        print('正在进行备份设备')
        usage = DiskUsage(dir_path[:2])
        print(f'total={usage.total}, usage.used={usage.used}, usage.free={usage.free}, '
              f'usage.percent={usage.percent}, reserved_gbs={reserved_gbs}')
        while usage.free < reserved_gbs:
            print(listdir(dir_path))
            delete_dir = path.join(dir_path, listdir(dir_path)[0])
            print(f'正在删除{delete_dir}目录, {datetime.now()}')
            shutil.rmtree(delete_dir)
            print(f'已删除{delete_dir}目录, {datetime.now()}')
            usage = DiskUsage(dir_path[:2])
        src_start_index = start_index
        dir_path = f'{dir_path}/' + str(date.today()).replace('-', '_')
        create_dir(dir_path)
        start_datetime = datetime.now()
        while True:
            print(f'开始执行时的时间为{datetime.now()}')
            LDConsole(start_index).backup(dir_path)
            now = datetime.now()
            used_datetime = now - start_datetime
            executed_num = start_index - src_start_index + 1
            average_datetime = used_datetime / (start_index - src_start_index + 1)
            print(f'执行完毕时的时间为{now}，已历时{used_datetime}，'
                  f'已执行完{executed_num}个，单个平均用时{average_datetime}\n')
            if start_index >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已备份完毕')
                break
            start_index += 1

    @classmethod
    def create(cls, start_index=1) -> None:
        """创建

        :param start_index: 起始索引值
        """
        for job_number, role in RetrieveIdleFishRecords.query_all_create_records():
            today = date.today()
            print(job_number, role, today)
            LDConsole.copy(job_number + role)
            update_idle_fish_ins = UpdateIdleFish(job_number)
            update_idle_fish_ins.update_create('NULL')
            update_idle_fish_ins.update_login(1)
            update_idle_fish_ins.update_last_create_date(today)
        cls.login(start_index, LDConsole.get_last_device_num())

    @classmethod
    def get_acs(cls):
        """获取所有支付宝的代付码

        :return: 所有支付宝的代付码
        """
        ac_li = []
        for item in listdir(r'\\10.1.1.2\acs')[::-1]:
            spli = item.split('.')
            if spli and spli[-1] == 'txt':
                ac_li.append(item)
        return ac_li

    @classmethod
    def auto_create(cls):
        """自动登录"""
        time_cnt = 0
        while True:
            acs = cls.get_acs()
            print(acs)
            if acs:
                start_index, end_index = 1, LDConsole.get_last_device_num()
                cls.create(end_index)
                cls.login(start_index, end_index)
                time_cnt = 0
                for ac_txt in acs:
                    print(ac_txt)
                    remove(join(r'\\10.1.1.2\acs', ac_txt))
                continue
            print(f'time_cnt={time_cnt}')
            sleep(1)
            time_cnt += 1

    # pylint: disable=too-many-statements, too-many-branches, too-many-locals
    @classmethod
    def login(cls, start_index, end_index):
        """登录

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        while True:
            if start_index - 1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已登录完毕'
                      f'，当前时间为：{datetime.now()}')
                break
            now = datetime.now()
            print(now)
            if not LDConsole(start_index).is_exist():
                print(f'设备{start_index}不存在，无需登录')
                start_index += 1
                continue
            job_number = LDConsole(start_index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            today = date.today()
            print(f'start_index={start_index}, device_name={LDConsole(start_index).get_name()}, '
                  f'user_name={retrieve_idle_fish_ins.user_name}, '
                  f'login_pw={retrieve_idle_fish_ins.login_pw}, '
                  f'if_mn={retrieve_idle_fish_ins.if_mn}, '
                  f'login={retrieve_idle_fish_ins.login}, '
                  f'last_login_date={retrieve_idle_fish_ins.last_login_date}, '
                  f'last_login_ipv4_addr={retrieve_idle_fish_ins.last_login_ipv4_addr}, '
                  f'today={today}')
            if not retrieve_idle_fish_ins.login:
                print(f'设备{start_index}上的是否需要登录的标志为'
                      f'{retrieve_idle_fish_ins.login}，无需登录')
                start_index += 1
                continue
            cls(start_index).run_app(21)
            lduia_ins = LDUIA(start_index)
            try:
                if lduia_ins.click(ResourceID.login_guide_bar):
                    lduia_ins.xml = ''
                dic = lduia_ins.get_dict(ResourceID.aliuser_login_mobile_et, xml=lduia_ins.xml)
                if not dic:
                    lduia_ins.click(ResourceID.login_onekey_btn, xml=lduia_ins.xml)
                    dic = lduia_ins.get_dict(ResourceID.aliuser_login_mobile_et)
                if_mn = dic.get('@text')
            except (FileNotFoundError, AttributeError) as err:
                print_err(err)
                continue
            print([if_mn], len(if_mn))
            update_idle_fish_ins = UpdateIdleFish(job_number)
            if len(if_mn) == 11 and if_mn != retrieve_idle_fish_ins.if_mn:
                update_idle_fish_ins.update_if_mn(if_mn)
            else:
                print('手机号已是最新，无需更新')
            lduia_ins.click(ResourceID.login_password_btn, xml=lduia_ins.xml)
            try:
                lduia_ins.click(ResourceID.confirm)
            except FileNotFoundError as err:
                print_err(err)
                continue
            lduia_ins.click(ResourceID.aliuser_login_show_password_btn, xml=lduia_ins.xml)
            lduia_ins.click(ResourceID.aliuser_login_password_et, xml=lduia_ins.xml)
            ldadb_ins = LDADB(start_index)
            ldadb_ins.input_text(retrieve_idle_fish_ins.login_pw)
            user_name = retrieve_idle_fish_ins.user_name
            try:
                if lduia_ins.click(ResourceID.aliuser_login_account_et):
                    ldadb_ins.input_text(retrieve_idle_fish_ins.user_name)
                    user_name = lduia_ins.get_dict(ResourceID.aliuser_login_account_et).get('@text')
                    print(user_name, user_name == retrieve_idle_fish_ins.user_name)
                    if user_name != retrieve_idle_fish_ins.user_name:
                        pyperclip.copy(retrieve_idle_fish_ins.user_name)
                        ldadb_ins.swipe((238, 423), (238, 423), 3000)
                        lduia_ins.tap((69, 353))
                        user_name = lduia_ins.get_dict(
                            ResourceID.aliuser_login_account_et).get('@text')
                        print(user_name, user_name == retrieve_idle_fish_ins.user_name)
                        if user_name != retrieve_idle_fish_ins.user_name:
                            continue
            except FileNotFoundError as err:
                print_err(err)
                continue
            try:
                login_pw = lduia_ins.get_dict(ResourceID.aliuser_login_password_et).get('@text')
            except (FileNotFoundError, AttributeError) as err:
                print_err(err)
                continue
            print(user_name, user_name == retrieve_idle_fish_ins.user_name)
            print(login_pw, login_pw == retrieve_idle_fish_ins.login_pw)
            if len(if_mn) == 11:
                lduia_ins.click(ResourceID.aliuser_login_login_btn, xml=lduia_ins.xml)
                sleep(3)
            elif user_name == retrieve_idle_fish_ins.user_name and \
                    login_pw == retrieve_idle_fish_ins.login_pw:
                lduia_ins.click(ResourceID.aliuser_login_login_btn, xml=lduia_ins.xml)
                sleep(3)
            update_idle_fish_ins.update_last_login_date(today)
            update_idle_fish_ins.update_last_login_ipv4_addr(get_global_ipv4_addr())
            update_idle_fish_ins.update_login('NULL')
            update_idle_fish_ins.update_version('NULL')
            if retrieve_idle_fish_ins.top_up_mobile:
                update_idle_fish_ins.update_top_up_mobile_cnt(-1)
            if Activity.WebViewActivity in ldadb_ins.get_current_focus():
                print(f'{start_index}于{datetime.now()}需要验证码登录，请输入验证码')
                update_idle_fish_ins.update_last_hvc_date(today)
            else:
                update_idle_fish_ins.update_last_nvc_date(today)
                try:
                    lduia_ins.click(ResourceID.tab_title, '我的')
                except FileNotFoundError as err:
                    print_err(err)
            lduia_ins.get_screen()
            try:
                lduia_ins.get_current_ui_hierarchy()
            except FileNotFoundError as err:
                print_err(err)
                lduia_ins.tap((478, 919))
            start_index += 1

    @classmethod
    def auto_buy(cls, start_index, end_index):
        """自动选择购买方法（首次或二次购买）

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        while True:
            if start_index - 1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已购买完毕'
                      f'，当前时间为：{datetime.now()}')
                break
            now = datetime.now()
            print(now)
            if not LDConsole(start_index).is_exist():
                print(f'设备{start_index}不存在，无需购买')
                start_index += 1
                continue
            today = date.today()
            job_number = LDConsole(start_index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            print(f'start_index={start_index}, device_name={LDConsole(start_index).get_name()}, '
                  f'buy={retrieve_idle_fish_ins.buy}, coins={retrieve_idle_fish_ins.coins}, '
                  f'today={today}')
            if not retrieve_idle_fish_ins.buy:
                print(f'设备{start_index}上的是否需要购买的标志为'
                      f'{retrieve_idle_fish_ins.buy}，无需购买')
                start_index += 1
                continue
            if retrieve_idle_fish_ins.login:
                print(f'设备{start_index}上的账号已掉线，login={retrieve_idle_fish_ins.login}，无法购买')
                start_index += 1
                continue
            if retrieve_idle_fish_ins.last_buy_date == today:
                print('今日已购买，无需重复购买')
                cls(start_index).get_pay_code(today)
                start_index += 1
                continue
            if retrieve_idle_fish_ins.reminder_threshold == 10000:
                print('已智能选择为使用首次购买方法')
                last_buy_coins = cls(start_index).first_buy_on_target_device(today)
            else:
                print('已智能选择为使用二次购买方法')
                last_buy_coins = cls(start_index).second_buy_on_target_device(today)
            if last_buy_coins:
                cls(start_index).get_pay_code(today)
            start_index += 1

    @classmethod
    def first_buy(cls, start_index, end_index):
        """首次购买（下单）

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        while True:
            if start_index - 1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已购买完毕'
                      f'，当前时间为：{datetime.now()}')
                break
            today = date.today()
            last_buy_coins = cls(start_index).first_buy_on_target_device(today)
            if last_buy_coins:
                cls(start_index).get_pay_code(today)
            start_index += 1

    @classmethod
    def second_buy(cls, start_index, end_index):
        """二次购买（下单）

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        while True:
            if start_index - 1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已购买完毕'
                      f'，当前时间为：{datetime.now()}')
                break
            today = date.today()
            last_buy_coins = cls(start_index).second_buy_on_target_device(today)
            if last_buy_coins:
                cls(start_index).get_pay_code(today)
            start_index += 1

    # pylint: disable=too-many-return-statements
    def get_pay_code(self, today: date.today(), retry_cnt=0, not_found=False):
        """获取好友代付二维码

        :param today: 今日的日期
        :param retry_cnt: 重试次数
        :param not_found: 未找到提醒发货的标志
        :return: 正常走完首次购买的流程返回True，否则返回False
        """
        self.run_app(19)
        lduia_ins = LDUIA(self.ld_index)
        ldadb_ins = LDADB(self.ld_index)
        try:
            lduia_ins.click(content_desc='我的，未选中状态')
            ldadb_ins.swipe([260, 800], [260, 660])
            lduia_ins.click(content_desc='我买到的')
            dst_path = r'\\10.1.1.2\aps\\'
            if not lduia_ins.click(content_desc='去付款', interval=3):
                if lduia_ins.click(content_desc='删除订单', xml=lduia_ins.xml):
                    return False
                if lduia_ins.get_dict(content_desc='确认收货', xml=lduia_ins.xml):
                    pass
                elif not lduia_ins.get_dict(content_desc='提醒发货', xml=lduia_ins.xml):
                    if not not_found:
                        return self.get_pay_code(today, retry_cnt=retry_cnt, not_found=True)
                    return False
            else:
                if lduia_ins.click(content_desc='支付宝支付'):
                    sleep(2)
                    lduia_ins.click(content_desc='立即支付')
                    lduia_ins.xml = ''
                    sleep(2)
                if not lduia_ins.click(text='找朋友帮忙付', xml=lduia_ins.xml):
                    if not lduia_ins.click(text='卡'):
                        if not lduia_ins.click(text='余额'):
                            lduia_ins.click(text='支付宝小荷包')
                    sleep(1)
                    while not lduia_ins.click(text='找朋友帮忙付'):
                        print('未找到找朋友帮忙付')
                        ldadb_ins.swipe([260, 900], [260, 600])
                        if lduia_ins.get_dict(content_desc='我买到的', xml=lduia_ins.xml):
                            return self.get_pay_code(today, retry_cnt)
                        if lduia_ins.get_dict(text='交易已付款，请勿重复支付。', xml=lduia_ins.xml):
                            return self.get_pay_code(today, retry_cnt)
                        if lduia_ins.get_dict(text='确认付款', xml=lduia_ins.xml):
                            return self.get_pay_code(today, retry_cnt)
                lduia_ins.click(text='立即付款')
                lduia_ins.click(text='面对面扫码')
                src_png = lduia_ins.get_screen()
                dst_png = path.join(dst_path,
                                    f'{str(self.ld_index).zfill(3)}_'
                                    f'{LDConsole(self.ld_index).get_job_number()}.png')
                lduia_ins.get_current_ui_hierarchy()
                qr_codes = decode(Image.open(src_png))
                while not exists(dst_png):
                    print(qr_codes, retry_cnt)
                    shutil.copy(src_png, dst_png)
                if lduia_ins.get_dict(text='帮我付款'):
                    if not qr_codes and retry_cnt < 16:
                        return self.get_pay_code(today, retry_cnt=retry_cnt+1)
                else:
                    return self.get_pay_code(today, retry_cnt)
        except FileNotFoundError as err:
            print_err(err)
            return self.get_pay_code(today, retry_cnt)
        job_number = LDConsole(self.ld_index).get_job_number()
        retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
        update_idle_fish_ins = UpdateIdleFish(job_number)
        update_idle_fish_ins.update_buy('NULL')
        update_idle_fish_ins = UpdateIdleFish(job_number)
        if 10000 <= retrieve_idle_fish_ins.reminder_threshold <= 40000:
            new_reminder_threshold = retrieve_idle_fish_ins.reminder_threshold + 10000
            print(f'new reminder_threshold is {new_reminder_threshold}')
            update_idle_fish_ins.update_reminder_threshold(new_reminder_threshold)
        if retrieve_idle_fish_ins.pay_pw and retrieve_idle_fish_ins.pay_pw != 'AAAAAA':
            update_idle_fish_ins.update_confirm(1)
        LDConsole.quit(self.ld_index)
        files = listdir(dst_path)
        length = len(files)
        print(files, length)
        while length > 3:
            sleep(10)
            files = listdir(dst_path)
            length = len(files)
            print(files, length)
        return True

    # pylint: disable=too-many-branches, too-many-statements
    @classmethod
    def confirm(cls, start_index, end_index):
        """确认收货

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        while True:
            if start_index - 1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已确认收货完毕'
                      f'，当前时间为：{datetime.now()}')
                break
            now = datetime.now()
            print(now)
            if not LDConsole(start_index).is_exist():
                print(f'设备{start_index}不存在，无需确认收货')
                start_index += 1
                continue
            job_number = LDConsole(start_index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            today = date.today()
            print(f'start_index={start_index}, device_name={LDConsole(start_index).get_name()}, '
                  f'confirm={retrieve_idle_fish_ins.confirm}, '
                  f'pay_pw={retrieve_idle_fish_ins.pay_pw}, '
                  f'today={today}')
            if not retrieve_idle_fish_ins.confirm:
                print(f'设备{start_index}上的是否需要确认收货的标志为'
                      f'{retrieve_idle_fish_ins.confirm}，无需确认收货')
                start_index += 1
                continue
            if retrieve_idle_fish_ins.login:
                print(
                    f'设备{start_index}上的账号已掉线，login={retrieve_idle_fish_ins.login}，无法确认收货')
                start_index += 1
                continue
            cls(start_index).run_app(18)
            if cls(start_index).is_logout('确认收货'):
                start_index += 1
                continue
            lduia_ins = LDUIA(start_index)
            try:
                lduia_ins.click(ResourceID.tab_title, '我的')
            except FileNotFoundError as err:
                print_err(err)
                continue
            ldadb_ins = LDADB(start_index)
            ldadb_ins.swipe([260, 800], [260, 660])
            try:
                lduia_ins.click(content_desc='我买到的')
            except FileNotFoundError as err:
                print_err(err)
                continue
            sleep(2)
            try:
                if not lduia_ins.click(content_desc='确认收货'):
                    sleep(9)
                    continue
            except FileNotFoundError as err:
                print_err(err)
                continue
            lduia_ins.click(content_desc='我已收到货，确认收货')
            sleep(3)
            lduia_ins.xml = ''
            all_is_ok = True
            for au_num in retrieve_idle_fish_ins.pay_pw:
                print(au_num)
                try:
                    if not lduia_ins.click(
                            f'com.taobao.idlefish:id/au_num_{au_num}', xml=lduia_ins.xml,
                            interval=0.01):
                        all_is_ok = False
                except FileNotFoundError as err:
                    print_err(err)
                    continue
            if not all_is_ok:
                continue
            sleep(1)
            LDADB(start_index).get_current_focus()
            lduia_ins.get_screen()
            try:
                lduia_ins.get_current_ui_hierarchy()
            except FileNotFoundError as err:
                print_err(err)
            sleep(1)
            try:
                if lduia_ins.get_dict(text='请输入支付密码'):
                    continue
            except FileNotFoundError as err:
                print_err(err)
            update_idle_fish_ins = UpdateIdleFish(job_number)
            update_idle_fish_ins.update_confirm('NULL')
            update_idle_fish_ins.update_last_confirm_date(today)
            try:
                if lduia_ins.get_dict(content_desc='去评价'):
                    LDConsole.quit(start_index)
            except FileNotFoundError as err:
                print_err(err)
            start_index += 1

    @classmethod
    def top_up_mobile(cls, start_index, end_index) -> None:
        """薅羊毛赚话费（使用最优方案充话费，use_best_deal_to_top_up_mobile）

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        dir_name = f'CurrentUIHierarchy/{str(date.today()).replace("-", "_")}_top_up_mobile'
        if exists(dir_name):
            for i in listdir(dir_name):
                job_number = i[:6]
                print(job_number)
                top_up_mobile_cnt = RetrieveIdleFish(job_number).top_up_mobile_cnt - 1
                yesterday = date.today() - timedelta(days=1)
                update_idle_fish_ins = UpdateIdleFish(job_number)
                update_idle_fish_ins.update_top_up_mobile_cnt(top_up_mobile_cnt)
                update_idle_fish_ins.update_last_top_up_mobile_date(yesterday)
        while True:
            if start_index - 1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已薅羊毛赚话费完毕'
                      f'，当前时间为：{datetime.now()}')
                break
            now = datetime.now()
            print(now)
            if not LDConsole(start_index).is_exist():
                print(f'设备{start_index}不存在，无需薅羊毛赚话费')
                start_index += 1
                continue
            cls(start_index).top_up_mobile_on_target_device()
            start_index += 1

    @classmethod
    def update_hosts(cls, start_index, end_index, host_name):
        """更新设备所在的主机列表

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        :param host_name: 当前主机的主机名
        """
        src_start_index = start_index
        while True:
            if start_index - 1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已更新主机列表完毕'
                      f'，当前时间为：{datetime.now()}')
                break
            now = datetime.now()
            print(now)
            if not LDConsole(start_index).is_exist():
                print(f'设备{start_index}不存在，无需更新主机列表')
                start_index += 1
                continue
            job_number = LDConsole(start_index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            today = date.today()
            device_name = LDConsole(start_index).get_name()
            new_host_name = f'{host_name}:{str(start_index).zfill(3)};'
            print(f'start_index={start_index}, device_name={device_name},'
                  f'new_host_name={new_host_name}, hosts={retrieve_idle_fish_ins.hosts}, '
                  f'update_last_update_hosts_date='
                  f'{retrieve_idle_fish_ins.last_update_hosts_date}, today={today}')
            if not retrieve_idle_fish_ins.hosts:
                UpdateIdleFish(job_number).update_hosts(new_host_name)
                UpdateIdleFish(job_number).update_last_update_hosts_date(today)
            elif new_host_name not in retrieve_idle_fish_ins.hosts:
                UpdateIdleFish(job_number).update_hosts(
                    f'{new_host_name}+{retrieve_idle_fish_ins.hosts}')
                UpdateIdleFish(job_number).update_last_update_hosts_date(today)
            start_index += 1

    @classmethod
    def record(cls, start_index, end_index):
        """记录设备今天的状态

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        while True:
            if start_index - 1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已记录设备今天的状态完毕'
                      f'，当前时间为：{datetime.now()}')
                break
            now = datetime.now()
            print(now)
            if not LDConsole(start_index).is_exist():
                print(f'设备{start_index}不存在，无需记录设备今天的状态')
                start_index += 1
                continue
            job_number = LDConsole(start_index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            today = date.today()
            print(
                f'start_index={start_index}, today={today}, job_number={job_number}, role='
                f'{retrieve_idle_fish_ins.role}, hosts={retrieve_idle_fish_ins.hosts}, '
                f'last_update_hosts_date={retrieve_idle_fish_ins.last_update_hosts_date}, \n'
                f'version={retrieve_idle_fish_ins.version}, '
                f'last_update_version_date={retrieve_idle_fish_ins.last_update_version_date}, '
                f'coins={retrieve_idle_fish_ins.coins}, '
                f'user_name={retrieve_idle_fish_ins.user_name}, today_global_ipv4_addr='
                f'{retrieve_idle_fish_ins.today_global_ipv4_addr}')
            if not retrieve_idle_fish_ins.last_check_date or \
                    retrieve_idle_fish_ins.last_check_date < today:
                print(f'设备{start_index}的闲鱼币信息今日未更新，请先更新闲鱼币信息')
                start_index += 1
                continue
            if not retrieve_idle_fish_ins.version:
                print(f'设备{start_index}的版本信息异常，请先更新版本信息')
                start_index += 1
                continue
            CreateRecordIdleFish(
                today, job_number, retrieve_idle_fish_ins.role, retrieve_idle_fish_ins.hosts,
                retrieve_idle_fish_ins.version, retrieve_idle_fish_ins.coins,
                retrieve_idle_fish_ins.user_name, retrieve_idle_fish_ins.today_global_ipv4_addr)
            start_index += 1

    @classmethod
    def update_ip(cls, start_index, end_index):
        """更新本机今日的公网IP地址

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        ipv4_addr = get_global_ipv4_addr()
        while True:
            if start_index - 1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已更新今日的公网IPv4地址完毕'
                      f'，当前时间为：{datetime.now()}')
                break
            now = datetime.now()
            print(now)
            if not LDConsole(start_index).is_exist():
                print(f'设备{start_index}不存在，无需更新当前设备的今日公网IPv4地址')
                start_index += 1
                continue
            job_number = LDConsole(start_index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            today = date.today()
            device_name = LDConsole(start_index).get_name()
            print(f'start_index={start_index}, device_name={device_name}, ipv4_addr={ipv4_addr}, '
                  f'today_global_ipv4_addr={retrieve_idle_fish_ins.today_global_ipv4_addr}, '
                  f'last_update_ip_date={retrieve_idle_fish_ins.last_update_ip_date}, '
                  f'today={today}')
            if ipv4_addr != retrieve_idle_fish_ins.today_global_ipv4_addr:
                UpdateIdleFish(job_number).update_today_global_ipv4_addr(ipv4_addr)
                UpdateIdleFish(job_number).update_last_update_ip_date(today)
            start_index += 1

    @classmethod
    def check_version_on_target_device(cls, index: int, today: date.today()) -> None:
        """检查目标设备上的版本是否存在问题

        :param index: 目标设备的索引值
        :param today: 今日的日期
        """
        print(f'正在准备检查设备{index}上的的闲鱼版本号')
        version_info = LDADB(index).get_app_version_info('com.taobao.idlefish')
        job_number = LDConsole(index).get_job_number()
        if version_info != RetrieveIdleFish(job_number).version:
            UpdateIdleFish(job_number).update_version(version_info)
        if version_info == '7.5.41':
            print('当前的闲鱼版本过老，需要升级')
        UpdateIdleFish(job_number).update_last_update_version_date(today)
        print(f'模拟器{index}上的闲鱼版本为：{version_info}')
        LDConsole.quit(index)
        print(f'第{index}项已检查完毕\n')

    @classmethod
    def check_version(cls, start_index: int, end_index: int):
        """检查版本是否存在问题

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        while True:
            if start_index - 1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已检查版本完毕'
                      f'，当前时间为：{datetime.now()}')
                break
            now = datetime.now()
            if now.hour >= 23 and now.minute >= 50:
                break
            print(now)
            today = date.today()
            if LDConsole(start_index).is_exist():
                job_number = LDConsole(start_index).get_job_number()
                retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
                print(f'设备{start_index}存在，version={retrieve_idle_fish_ins.version}，'
                      f'last_update_version_date='
                      f'{retrieve_idle_fish_ins.last_update_version_date}'
                      f'，today={today}，{datetime.now()}')
                if retrieve_idle_fish_ins.last_check_date != today:
                    start_index += 1
                    continue
                if not retrieve_idle_fish_ins.version:
                    pass
                elif retrieve_idle_fish_ins.version == '0.0.0':
                    pass
                elif not retrieve_idle_fish_ins.last_update_version_date:
                    pass
                elif retrieve_idle_fish_ins.last_update_version_date >= today:
                    start_index += 1
                    continue
                elif retrieve_idle_fish_ins.version[:4] in ['7.5.', '7.7.', '7.8.', '7.9.']:
                    start_index += 1
                    continue
            else:
                print(f'设备{start_index}不存在，{datetime.now()}')
                start_index += 1
                continue
            cls(start_index).launch()
            sleep(5)
            cls.check_version_on_target_device(start_index, today)
            start_index += 1

    @classmethod
    def restart_before_check_target_device(cls, index):
        """检查目标设备是否存在问题之前如果有需要先重启一次

        :param index: 目标设备的索引值
        :return: 不需要重启返回False，重启一次完毕返回True
        """
        if date(year=2023, month=1, day=21) >= date.today() >= date(year=2023, month=1, day=10):
            print('当前正值抽福卡日期段，每天检查之前需要先重启一次')
        else:
            return False
        print(f'正在准备检查设备{index}之前的重启操作')
        lduia_ins = LDUIA(index)
        lduia_ins.tap((50, 85), 9)
        cls(index).run_app(19)
        return True

    # pylint: disable=too-many-return-statements, too-many-branches, too-many-statements
    # pylint: disable=too-many-locals
    @classmethod
    def check_target_device(cls, index: int, reopen_flag=False, sleep_time=30) -> bool:
        """检查目标设备是否存在问题

        :param index: 目标设备的索引值
        :param reopen_flag: 是否需要重启模拟器并打开闲鱼app
        :param sleep_time: 等待时间
        :return: 目标设备不存在或已掉线返回False，正常检查完毕返回True
        """
        if reopen_flag:
            cls(index).run_app(sleep_time)
        print(f'正在准备检查设备{index}')
        current_focus = LDADB(index).get_current_focus()
        if cls(index).should_restart(current_focus):
            sleep_time += 30
            return cls.check_target_device(index, reopen_flag=True, sleep_time=sleep_time+30)
        if cls(index).is_logout('检查工作', current_focus):
            return False
        lduia_ins = LDUIA(index)
        job_number = LDConsole(index).get_job_number()
        update_idle_fish_ins = UpdateIdleFish(job_number)
        retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
        lduia_ins.tap((50, 85), 9)
        try:
            if lduia_ins.get_dict(content_desc='数码店'):
                lduia_ins.tap((270, 652), 3)
                lduia_ins.tap((268, 809), 6)
                return cls.check_target_device(index, reopen_flag=True, sleep_time=sleep_time+30)
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            return cls.check_target_device(index, reopen_flag=True, sleep_time=sleep_time+30)
        if lduia_ins.get_dict(content_desc='奖励：闲鱼币x', xml=lduia_ins.xml):
            lduia_ins.tap((264, 709), 6)
        elif lduia_ins.get_dict(content_desc='经验不够，这里可以去赚哦', xml=lduia_ins.xml):
            lduia_ins.tap((487, 596), 3)
            return cls.check_target_device(index, reopen_flag=True, sleep_time=sleep_time+30)
        elif lduia_ins.get_dict(content_desc=r'HI，店长 ', xml=lduia_ins.xml):
            lduia_ins.tap((266, 599), 3)
            return cls.check_target_device(index, reopen_flag=True, sleep_time=sleep_time+30)
        elif lduia_ins.get_dict(content_desc='领取闲鱼币，去开新店', xml=lduia_ins.xml):
            lduia_ins.tap((283, 763), 3)
            return cls.check_target_device(index, reopen_flag=True, sleep_time=sleep_time+30)
        dic = lduia_ins.get_dict(content_desc='我的经验', xml=lduia_ins.xml)
        try:
            ex_p = int(dic['@content-desc'][5:])
        except TypeError as err:
            print('正在尝试关闭因生日提醒窗导致的错误')
            lduia_ins.tap((271, 765), 3)  # 关闭生日礼物
            print_err(err)
            return cls.check_target_device(index, reopen_flag=True, sleep_time=sleep_time+30)
        for _ in range(int(ex_p / 200)):
            lduia_ins.tap((276, 600), 0.01)
        if ex_p >= 200:
            return cls.check_target_device(index, reopen_flag=True, sleep_time=sleep_time+30)
        if lduia_ins.get_dict(content_desc='点击领取', xml=lduia_ins.xml):
            lduia_ins.tap((453, 492), 3)
            lduia_ins.tap((267, 642), 3)
            lduia_ins.xml = ''
        try:
            dic = lduia_ins.get_dict('android:id/content', xml=lduia_ins.xml)['node']
        except FileNotFoundError as err:
            print_err(err)
            return cls.check_target_device(index, reopen_flag=True, sleep_time=sleep_time+30)
        try:
            coins = dic[1]['node']['node']['node']['node']['node'][1]['@content-desc']
            if '万' in coins:
                coins = float(coins[:-1]) * 10000
            coins = int(coins)
        except (KeyError, TypeError, ValueError) as err:
            print_err(err)
            return cls.check_target_device(index, reopen_flag=True, sleep_time=sleep_time+30)
        if coins != retrieve_idle_fish_ins.coins:
            update_idle_fish_ins.update_coins(coins)
        png_path = lduia_ins.get_screen()
        dir_name = f'CurrentUIHierarchy/{str(date.today()).replace("-", "_")}'
        reminder_threshold = retrieve_idle_fish_ins.reminder_threshold
        if reminder_threshold:
            if coins >= reminder_threshold:
                dir_name = f'{dir_name}_rty'
            else:
                dir_name = f'{dir_name}_rtn'
        else:
            if coins >= 30000:
                dir_name = f'{dir_name}_30k'
            elif coins >= 20000:
                dir_name = f'{dir_name}_20k'
            elif coins >= 10000:
                dir_name = f'{dir_name}_10k'
        create_dir(dir_name)
        new_png = f'{dir_name}/{LDConsole(index).get_name()}.png'
        if path.exists(new_png):
            remove(new_png)
        rename(png_path, new_png)
        LDConsole.quit(index)
        today = date.today()
        if today != retrieve_idle_fish_ins.last_check_date:
            update_idle_fish_ins.update_last_check_date(today)
        print(f'第{index}项已检查完毕\n')
        return True

    @classmethod
    def check_after_run(cls, start_index, end_index, break_flag=False):
        """从数据库中读取到运行过的状态之后再进行检查

        :param start_index: 起始索引值（包含）
        :param end_index: 终止索引值（包含）
        :param break_flag: 执行完之后是否终止执行
        """
        src_start_index = start_index
        start_day = date.today()
        all_done = True
        while True:
            now = datetime.now()
            print(now)
            while start_day != date.today():
                seconds = (datetime.fromisoformat(
                    f'{date.today() + timedelta(days=1)} 00:00:00') - datetime.now()).seconds
                if seconds > 3600:
                    sleep(3600)
                else:
                    sleep(seconds)
            if start_index > end_index:
                print(f'所有共{end_index - src_start_index + 1}项已检查完毕，当前时间为：'
                      f'{datetime.now()}\n')
                if datetime.now().hour >= 23 or all_done:
                    start_day = date.today() + timedelta(days=1)
                src_start_index = start_index = 1
                all_done = True
                if break_flag:
                    break
                continue
            if now.hour >= 23 and now.minute >= 50:
                print(f'目标设备{start_index}当前的执行时间为{now}，不在正常的检查时段，无需检查\n')
                start_index += 1
                continue
            if not LDConsole(start_index).is_exist():
                print(f'目标设备{start_index}不存在，无需检查\n')
                start_index += 1
                continue
            job_number = LDConsole(start_index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            print(start_index, LDConsole(start_index).get_name())
            today = date.today()
            print(f'last_run_date={retrieve_idle_fish_ins.last_run_date}, '
                  f'last_check_date={retrieve_idle_fish_ins.last_check_date}, '
                  f'today={today}, all_done={all_done}, login={retrieve_idle_fish_ins.login}')
            if retrieve_idle_fish_ins.login:
                print(f'目标设备{start_index}已掉线，无需检查\n')
                start_index += 1
                continue
            if retrieve_idle_fish_ins.last_check_date != today:
                all_done = False
            if not retrieve_idle_fish_ins.last_run_date:
                start_index += 1
                print()
                continue
            if retrieve_idle_fish_ins.last_check_date and \
                    retrieve_idle_fish_ins.last_check_date >= retrieve_idle_fish_ins.last_run_date:
                start_index += 1
                print()
                continue
            CPU.wait_until_idle()
            # if retrieve_idle_fish_ins.top_up_mobile and retrieve_idle_fish_ins.top_up_mobile_cnt \
            #         and retrieve_idle_fish_ins.top_up_mobile_cnt > 3:
            #     cls(start_index).top_up_mobile_on_target_device(False)
            cls(start_index).run_app(19)
            # cls.restart_before_check_target_device(start_index)
            cls.check_target_device(start_index)
            start_index += 1

    def run_task_on_target_device(self, today: date.today(), sleep_time=60) -> bool:
        """在指定设备上执行任务

        :param today: 今日的日期
        :param sleep_time: 等待时间
        :return: 执行结束时返回True
        """
        while self.should_restart():
            self.run_app(sleep_time)
            sleep_time += 30
        lduia_ins = LDUIA(self.ld_index)
        lduia_ins.tap((479, 916), 6)
        lduia_ins.get_screen()
        try:
            lduia_ins.get_current_ui_hierarchy()
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            self.run_app(sleep_time)
            return self.run_task_on_target_device(today, sleep_time=sleep_time+30)
        if self.should_restart():
            return self.run_task_on_target_device(today, sleep_time=sleep_time+30)
        return True

    @classmethod
    def run_task(cls, run_list: list, today: date.today()) -> None:
        """执行任务

        :param run_list: 待执行任务设备的索引值列表
        :param today: 今日的日期
        """
        for i, index in enumerate(run_list):
            if i == len(run_list) - 1:
                cls(index).run_app()
            elif i == 0:
                cls(index).run_app(1)
            else:
                cls(index).run_app(26)
        for index in run_list:
            cls(index).run_task_on_target_device(today)
        if run_list:
            sleep(69)
        for index in run_list:
            LDConsole.quit(index)
            job_number = LDConsole(index).get_job_number()
            if today != RetrieveIdleFish(job_number).last_run_date:
                UpdateIdleFish(job_number).update_last_run_date(today)
            print(f'第{index}项已执行完毕')

    @classmethod
    def mainloop(cls, start_index: int, end_index: int, p_num=3, check_after_run=-1) -> None:
        """主循环

        :param start_index: 起始索引值（包含）
        :param end_index: 终止索引值（包含）
        :param p_num: 并发数量
        :param check_after_run: 检查的起始索引值，默认为-1代表不检查
        """
        src_start_index = start_index
        now = datetime.now()
        if start_index <= 1 and now.hour >= 23 and now.minute >= 50:
            start_day = date.today() + timedelta(days=1)
        else:
            start_day = date.today()
        while True:
            today = date.today()
            while start_day > today:
                now = datetime.now()
                print(f'mainloop while start_day={start_day}, today={today}, {now}')
                seconds = (datetime.fromisoformat(
                    f'{date.today() + timedelta(days=1)} 00:00:00') - now).seconds
                if seconds > 3600:
                    sleep(3600)
                else:
                    sleep(seconds)
                today = date.today()
            print(f'mainloop start_day={start_day}, today={today}, {datetime.now()}')
            run_list = []
            while len(run_list) < p_num:
                if IdleFish(start_index).should_run_task(today):
                    run_list.append(start_index)
                start_index += 1
                if start_index > end_index:
                    break
            cls.run_task(run_list, today)
            if start_index > end_index:
                print(f'所有共{end_index - src_start_index + 1}项已执行完毕，'
                      f'当前时间为：{datetime.now()}')
                start_index = src_start_index = 1
                start_day = date.today() + timedelta(days=1)
                if check_after_run != -1:
                    cls.check_after_run(check_after_run+1, end_index, True)
