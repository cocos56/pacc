"""闲鱼全自动刷闲鱼币中央监控系统模块"""
import os
import shutil
from datetime import date, datetime, timedelta
from os import listdir, path
from xml.parsers.expat import ExpatError

import pyautogui
import pyperclip
from pymouse import PyMouse
from psutil import cpu_percent

from .idle_fish_base import Activity, ResourceID, IdleFishBase
from ..adb import LDConsole, LDADB, LDUIA
from ..base import sleep, print_err
from ..mysql import RetrieveIdleFish, RetrieveIdleFishData, \
    UpdateIdleFish, CreateRecordIdleFish
from ..tools import create_dir, get_global_ipv4_addr, DiskUsage


class IdleFish(IdleFishBase):
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
        if usage.free < reserved_gbs:
            print(listdir(dir_path))
            delete_dir = path.join(dir_path, listdir(dir_path)[0])
            print(f'正在删除{delete_dir}目录, {datetime.now()}')
            shutil.rmtree(delete_dir)
            print(f'已删除{delete_dir}目录, {datetime.now()}')
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
    def create(cls, start_index=1):
        """创建

        :param start_index: 起始索引值
        """
        for job_number, role in RetrieveIdleFishData.query_all_data():
            today = date.today()
            print(job_number, role, today)
            LDConsole.copy(job_number + role)
            update_idle_fish_ins = UpdateIdleFish(job_number)
            update_idle_fish_ins.update_create('NULL')
            update_idle_fish_ins.update_login(1)
            update_idle_fish_ins.update_last_create_date(today)
        cls.login(start_index, LDConsole.get_last_device_num())

    # pylint: disable=too-many-statements, too-many-branches
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
                if_mn = lduia_ins.get_dict(ResourceID.aliuser_login_mobile_et).get('@text')
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
                lduia_ins.click(ResourceID.aliuser_login_show_password_btn)
            except FileNotFoundError as err:
                print_err(err)
                continue
            lduia_ins.click(ResourceID.aliuser_login_password_et, xml=lduia_ins.xml)
            ldadb_ins = LDADB(start_index)
            ldadb_ins.input_text(retrieve_idle_fish_ins.login_pw)
            user_name = retrieve_idle_fish_ins.user_name
            if lduia_ins.click(ResourceID.aliuser_login_account_et):
                ldadb_ins.input_text(retrieve_idle_fish_ins.user_name)
                user_name = lduia_ins.get_dict(ResourceID.aliuser_login_account_et).get('@text')
                print(user_name, user_name == retrieve_idle_fish_ins.user_name)
                if user_name != retrieve_idle_fish_ins.user_name:
                    pyperclip.copy(retrieve_idle_fish_ins.user_name)
                    m = PyMouse()
                    a = m.position()  # 获取当前坐标的位置
                    print(a)
                    pyautogui.hotkey('ctrl', 'v')
                    print()
                input()
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
            start_index += 1

    @classmethod
    def buy(cls, start_index, end_index):
        """购买（下单）

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
            job_number = LDConsole(start_index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            today = date.today()
            coins = retrieve_idle_fish_ins.coins
            print(f'start_index={start_index}, device_name={LDConsole(start_index).get_name()}, '
                  f'buy={retrieve_idle_fish_ins.buy}, coins={coins}, '
                  f'today={today}')
            if not retrieve_idle_fish_ins.buy:
                print(f'设备{start_index}上的是否需要购买的标志为'
                      f'{retrieve_idle_fish_ins.buy}，无需购买')
                start_index += 1
                continue
            cls(start_index).run_app(19)
            lduia_ins = LDUIA(start_index)
            ldadb_ins = LDADB(start_index)
            try:
                lduia_ins.click(ResourceID.tab_title, '消息')
            except FileNotFoundError as err:
                print_err(err)
                continue
            try:
                if lduia_ins.click(text='我知道了'):
                    lduia_ins.xml = ''
            except FileNotFoundError as err:
                print_err(err)
                continue
            try:
                while not lduia_ins.click(index='1', content_desc='徐哥签名', xml=lduia_ins.xml):
                    if lduia_ins.click(index='0', content_desc='徐哥签名', xml=lduia_ins.xml) or \
                            Activity.Launcher in LDADB(start_index).get_current_focus():
                        break
                    ldadb_ins.swipe([290, 690], [290, 330], 500)
                    lduia_ins.xml = ''
            except FileNotFoundError as err:
                print_err(err)
                continue
            if Activity.Launcher in LDADB(start_index).get_current_focus():
                continue
            sleep(1)
            try:
                while not lduia_ins.click(naf='true', index='3'):
                    sleep(1)
            except FileNotFoundError as err:
                print_err(err)
                continue
            lduia_ins.click(content_desc='再次购买')
            last_buy_coins = 0
            if coins >= 50000:
                last_buy_coins = 50000
            elif coins >= 40000:
                last_buy_coins = 40000
            elif coins >= 30000:
                last_buy_coins = 30000
            elif coins >= 20000:
                last_buy_coins = 20000
            try:
                lduia_ins.click(ResourceID.tv_value, str(last_buy_coins // 100))
            except FileNotFoundError as err:
                print_err(err)
                continue
            lduia_ins.click(text='立即购买')
            LDADB(start_index).get_current_focus()
            sleep(1)
            try:
                lduia_ins.click(content_desc='确认购买')
            except FileNotFoundError as err:
                print_err(err)
                continue
            sleep(2)
            try:
                if lduia_ins.get_dict(content_desc='确认购买'):
                    continue
            except FileNotFoundError as err:
                print_err(err)
            if not lduia_ins.click(text='找朋友帮忙付'):
                try:
                    if not lduia_ins.click(text='卡'):
                        lduia_ins.click(text='余额')
                except FileNotFoundError as err:
                    print_err(err)
                    if not lduia_ins.click(text='卡'):
                        lduia_ins.click(text='账户余额')
                sleep(1)
                try:
                    while not lduia_ins.click(text='找朋友帮忙付'):
                        print('未找到找朋友帮忙付')
                        ldadb_ins.swipe([260, 900], [260, 600])
                except FileNotFoundError as err:
                    print_err(err)
            update_idle_fish_ins = UpdateIdleFish(job_number)
            update_idle_fish_ins.update_buy('NULL')
            update_idle_fish_ins.update_last_buy_date(today)
            update_idle_fish_ins.update_last_buy_coins(last_buy_coins)
            if retrieve_idle_fish_ins.pay_pw and retrieve_idle_fish_ins.pay_pw != 'AAAAAA':
                update_idle_fish_ins.update_confirm(1)
            lduia_ins.click(text='立即付款')
            sleep(1)
            try:
                lduia_ins.click(text='面对面扫码')
            except FileNotFoundError as err:
                print_err(err)
            lduia_ins.get_screen()
            lduia_ins.get_current_ui_hierarchy()
            start_index += 1

    @classmethod
    def pay(cls, start_index, end_index):
        """付款：获取好友代付二维码

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        while True:
            if start_index - 1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已获取好友代付二维码完毕'
                      f'，当前时间为：{datetime.now()}')
                break
            now = datetime.now()
            print(now)
            if not LDConsole(start_index).is_exist():
                print(f'设备{start_index}不存在，无需获取好友代付二维码')
                start_index += 1
                continue
            job_number = LDConsole(start_index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            today = date.today()
            print(f'start_index={start_index}, device_name={LDConsole(start_index).get_name()}, '
                  f'pay={retrieve_idle_fish_ins.pay}, '
                  f'today={today}')

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
            cls(start_index).run_app(18)
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
            sleep(1)
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
                            f'com.taobao.idlefish:id/au_num_{au_num}', xml=lduia_ins.xml):
                        all_is_ok = False
                except FileNotFoundError as err:
                    print_err(err)
                    continue
            if not all_is_ok:
                continue
            update_idle_fish_ins = UpdateIdleFish(job_number)
            update_idle_fish_ins.update_confirm('NULL')
            update_idle_fish_ins.update_last_confirm_date(today)
            sleep(1)
            LDADB(start_index).get_current_focus()
            lduia_ins.get_screen()
            try:
                lduia_ins.get_current_ui_hierarchy()
            except FileNotFoundError as err:
                print_err(err)
            LDConsole.quit(start_index)
            start_index += 1

    @classmethod
    def top_up_mobile(cls, start_index, end_index):
        """薅羊毛赚话费（使用最优方案充话费，use_best_deal_to_top_up_mobile）

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
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
            job_number = LDConsole(start_index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            today = date.today()
            print(f'start_index={start_index}, device_name={LDConsole(start_index).get_name()}, '
                  f'top_up_mobile={retrieve_idle_fish_ins.top_up_mobile}, '
                  f'last_top_up_mobile_date={retrieve_idle_fish_ins.last_top_up_mobile_date}, '
                  f'today={today}')
            if retrieve_idle_fish_ins.user_name[:2] != 'xy':
                print(f'设备{start_index}上的账号{retrieve_idle_fish_ins.user_name}不是以xy开头，'
                      f'无需薅羊毛赚话费')
                start_index += 1
                continue
            if not retrieve_idle_fish_ins.top_up_mobile:
                print(f'设备{start_index}上的执行薅羊毛赚话费的标志为'
                      f'{retrieve_idle_fish_ins.top_up_mobile}，无需薅羊毛赚话费')
                start_index += 1
                continue
            if not retrieve_idle_fish_ins.last_top_up_mobile_date:
                pass
            elif retrieve_idle_fish_ins.last_top_up_mobile_date >= today:
                print(f'今天已在设备{start_index}上执行过薅羊毛赚话费的任务，无需重复执行')
                start_index += 1
                continue
            cls(start_index).run_app(19)
            lduia_ins = LDUIA(start_index)
            lduia_ins.tap((50, 85), 6)
            lduia_ins.tap((479, 596), 3)
            LDADB(start_index).get_current_focus()
            try:
                if lduia_ins.get_dict(content_desc=r'HI，店长 '):
                    print('当前界面需要先点击一下升级小店然后再点击赚经验')
                    lduia_ins.tap((266, 599), 3)
                    lduia_ins.tap((479, 596), 3)
                    lduia_ins.xml = ''
            except FileNotFoundError as err:
                print_err(err)
                lduia_ins.xml = ''
                continue
            if not lduia_ins.get_dict(content_desc='提醒签到', xml=lduia_ins.xml):
                print('当前界面不是赚经验的界面，正在重新执行')
                continue
            if lduia_ins.get_dict(content_desc='薅羊毛赚话费'):
                lduia_ins.tap((460, 350), 20)
            lduia_ins.get_screen()
            try:
                lduia_ins.get_current_ui_hierarchy()
            except FileNotFoundError as err:
                print_err(err)
            cls(start_index).run_app(19)
            LDConsole.quit(start_index)
            UpdateIdleFish(job_number).update_last_top_up_mobile_date(today)
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
            new_host_name = f'{host_name}:{start_index}'
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
            elif not retrieve_idle_fish_ins.version:
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
                elif not retrieve_idle_fish_ins.version:
                    pass
                elif not retrieve_idle_fish_ins.last_update_version_date:
                    pass
                elif retrieve_idle_fish_ins.last_update_version_date >= today:
                    start_index += 1
                    continue
                elif retrieve_idle_fish_ins.version[:4] == '7.8.':
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
    def check_target_device(cls, index: int, reopen_flag=False) -> bool:
        """检查目标设备是否存在问题

        :param index: 目标设备的索引值
        :param reopen_flag: 是否需要重启模拟器并打开闲鱼app
        :return: 目标设备不存在或已掉线返回False，正常检查完毕返回True
        """
        if reopen_flag:
            cls(index).run_app(30)
        print(f'正在准备检查设备{index}')
        current_focus = LDADB(index).get_current_focus()
        if cls(index).should_restart(current_focus):
            return cls.check_target_device(index, reopen_flag=True)
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
                return cls.check_target_device(index, reopen_flag=True)
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            return cls.check_target_device(index, reopen_flag=True)
        if lduia_ins.get_dict(content_desc='奖励：闲鱼币x', xml=lduia_ins.xml):
            lduia_ins.tap((264, 709), 6)
        elif lduia_ins.get_dict(content_desc='经验不够，这里可以去赚哦', xml=lduia_ins.xml):
            lduia_ins.tap((487, 596), 3)
            return cls.check_target_device(index, reopen_flag=True)
        elif lduia_ins.get_dict(content_desc=r'HI，店长 ', xml=lduia_ins.xml):
            lduia_ins.tap((266, 599), 3)
            return cls.check_target_device(index, reopen_flag=True)
        elif lduia_ins.get_dict(content_desc='领取闲鱼币，去开新店', xml=lduia_ins.xml):
            lduia_ins.tap((283, 763), 3)
            return cls.check_target_device(index, reopen_flag=True)
        dic = lduia_ins.get_dict(content_desc='我的经验', xml=lduia_ins.xml)
        try:
            ex_p = int(dic['@content-desc'][5:])
        except TypeError as err:
            print('正在尝试关闭因生日提醒窗导致的错误')
            lduia_ins.tap((271, 765), 3)  # 关闭生日礼物
            print_err(err)
            return cls.check_target_device(index, reopen_flag=True)
        for _ in range(int(ex_p / 200)):
            lduia_ins.tap((276, 600), 0.01)
        if ex_p >= 200:
            return cls.check_target_device(index, reopen_flag=True)
        if lduia_ins.get_dict(content_desc='点击领取', xml=lduia_ins.xml):
            lduia_ins.tap((453, 492), 3)
            lduia_ins.tap((267, 642), 3)
            lduia_ins.xml = ''
        try:
            dic = lduia_ins.get_dict('android:id/content', xml=lduia_ins.xml)['node']
        except FileNotFoundError as err:
            print_err(err)
            return cls.check_target_device(index, reopen_flag=True)
        try:
            coins = dic[1]['node']['node']['node']['node']['node'][1]['@content-desc']
            if '万' in coins:
                coins = float(coins[:-1]) * 10000
            coins = int(coins)
        except (KeyError, TypeError, ValueError) as err:
            print_err(err)
            return cls.check_target_device(index, reopen_flag=True)
        if coins != retrieve_idle_fish_ins.coins:
            update_idle_fish_ins.update_coins(coins)
        png_path = lduia_ins.get_screen()
        dir_name = 'CurrentUIHierarchy/' + str(date.today()).replace('-', '_')
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
            os.remove(new_png)
        os.rename(png_path, new_png)
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
                if datetime.now().hour >= 3 or all_done:
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
            cpu_use = cpu_percent()
            print(cpu_use)
            while cpu_use > 60:
                sleep(5)
                cpu_use = cpu_percent(1)
                print(cpu_use)
            cls(start_index).run_app(19)
            # cls.restart_before_check_target_device(start_index)
            cls.check_target_device(start_index)
            start_index += 1

    def run_task_on_target_device(self, today: date.today()) -> None:
        """在指定设备上执行任务"""
        while self.should_restart():
            self.run_app()
        lduia_ins = LDUIA(self.ld_index)
        lduia_ins.tap((479, 916), 6)
        lduia_ins.get_screen()
        try:
            lduia_ins.get_current_ui_hierarchy()
        except (FileNotFoundError, ExpatError) as err:
            print_err(err)
            self.run_app()
            return self.run_task_on_target_device(today)
        if self.should_restart():
            return self.run_task_on_target_device(today)

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
        if start_index <= 1 and datetime.now().hour > 22:
            start_day = date.today() + timedelta(days=1)
        else:
            start_day = date.today()
        while True:
            today = date.today()
            while start_day > today:
                print(f'mainloop while start_day={start_day}, today={today}, {datetime.now()}')
                seconds = (datetime.fromisoformat(
                    f'{date.today() + timedelta(days=1)} 00:00:00') - datetime.now()).seconds
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
