"""闲鱼全自动刷闲鱼币中央监控系统模块2"""
# pylint: disable=duplicate-code
import os
import shutil
from os import listdir, path
from datetime import date, datetime, timedelta
from xml.parsers.expat import ExpatError

from psutil import cpu_percent

from .ld_proj import LDProj
from .idle_fish import Activity, ResourceID
from ..adb import LDConsole, LDADB, LDUIA
from ..base import sleep, print_err
from ..mysql import RetrieveIdleFish, UpdateIdleFish, CreateRecordIdleFish
from ..tools import create_dir, get_global_ipv4_addr, DiskUsage


class IdleFish2(LDProj):
    """咸鱼类"""

    def __init__(self, ld_index=1):
        """构造函数

        :param ld_index: 目标雷电模拟器的索引值
        """
        super().__init__()
        self.ld_index = ld_index

    @classmethod
    def backups(cls, start_index, end_index, dir_path='E:/ldbks', reserved_gbs=6*1024):
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

    def launch(self):
        """启动雷电模拟器"""
        if LDConsole(self.ld_index).is_exist():
            LDConsole.quit(self.ld_index)
            LDConsole(self.ld_index).launch()
        else:
            print(f'模拟器{self.ld_index}不存在，无法启动')

    def run_app(self, sleep_time=60):
        """启动雷电模拟器并运行咸鱼APP

        :param sleep_time: 等待时间
        """
        if LDConsole(self.ld_index).is_exist():
            LDConsole.quit(self.ld_index)
            LDConsole(self.ld_index).run_app('com.taobao.idlefish', '闲鱼')
        else:
            print(f'设备{self.ld_index}不存在，无法启动')
        sleep(sleep_time)

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
            cls(start_index).run_app(19)
            lduia_ins = LDUIA(start_index)
            if_mn = lduia_ins.get_dict(ResourceID.aliuser_login_mobile_et).get('@text')
            print([if_mn], len(if_mn))
            update_idle_fish_ins = UpdateIdleFish(job_number)
            if len(if_mn) == 11 and if_mn != retrieve_idle_fish_ins.if_mn:
                update_idle_fish_ins.update_if_mn(if_mn)
            else:
                print('手机号已是最新，无需更新')
            lduia_ins.click(ResourceID.login_password_btn)
            lduia_ins.click(ResourceID.confirm)
            lduia_ins.get_screen()
            lduia_ins.get_current_ui_hierarchy()
            update_idle_fish_ins.update_last_login_date(today)
            update_idle_fish_ins.update_last_login_ipv4_addr(get_global_ipv4_addr())
            update_idle_fish_ins.update_login('NULL')
            input()
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
            print(LDADB(start_index).get_current_focus())
            if lduia_ins.get_dict(content_desc=r'HI，店长 '):
                print('当前界面需要先点击一下升级小店然后再点击赚经验')
                lduia_ins.tap((266, 599), 3)
                lduia_ins.tap((479, 596), 3)
                lduia_ins.xml = ''
            if not lduia_ins.get_dict(content_desc='提醒签到', xml=lduia_ins.xml):
                print('当前界面不是赚经验的界面，正在重新执行')
                continue
            if lduia_ins.get_dict(content_desc='薅羊毛赚话费'):
                lduia_ins.tap((460, 350), 20)
            lduia_ins.get_screen()
            lduia_ins.get_current_ui_hierarchy()
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
    def check_version_on_target_device(cls, index: int, today: date.today()) -> bool:
        """检查目标设备上的版本是否存在问题

        :param index: 目标设备的索引值
        :param today: 今日的日期
        :return: 目标设备不存在返回False，正常检查完毕返回True
        """
        if not LDConsole(index).is_exist():
            print('目标设备不存在，无需检查')
            return False
        print(f'正在准备检查设备{index}上的的闲鱼版本号')
        version_info = LDADB(index).get_app_version_info('com.taobao.idlefish')
        job_number = LDConsole(index).get_job_number()
        if version_info not in ('0.0.0', RetrieveIdleFish(job_number).version):
            UpdateIdleFish(job_number).update_version(version_info)
        if version_info == '7.5.41':
            print('当前的闲鱼版本过老，需要升级')
        UpdateIdleFish(job_number).update_last_update_version_date(today)
        print(f'模拟器{index}上的闲鱼版本为：{version_info}')
        LDConsole.quit(index)
        print(f'第{index}项已检查完毕\n')
        return True

    @classmethod
    def check_version(cls, start_index: int, end_index: int, p_num=5):
        """检查版本是否存在问题

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        :param p_num: 并发数量
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
            should_run = False
            today = date.today()
            for i in range(p_num):
                index = start_index + i
                if LDConsole(index).is_exist():
                    job_number = LDConsole(index).get_job_number()
                    retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
                    print(f'设备{index}存在，version={retrieve_idle_fish_ins.version}，'
                          f'last_update_version_date='
                          f'{retrieve_idle_fish_ins.last_update_version_date}'
                          f'，today={today}，{datetime.now()}')
                    if not retrieve_idle_fish_ins.last_update_version_date:
                        should_run = True
                    elif retrieve_idle_fish_ins.last_update_version_date >= today:
                        continue
                    if not retrieve_idle_fish_ins.version or \
                            retrieve_idle_fish_ins.version != '7.8.10':
                        should_run = True
                else:
                    print(f'设备{index}不存在，{datetime.now()}')
            if not should_run:
                print(
                    '本轮中的设备全部属于不存在或已是最新版本或今日已更新过版本号的设备，无需进行检查版本信息的操作\n')
                start_index += p_num
                continue
            for i in range(p_num):
                cls(start_index + i).launch()
            sleep(5)
            for i in range(p_num):
                cls.check_version_on_target_device(start_index + i, today)
            start_index += p_num

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

    def should_restart(self, current_focus=''):
        """判断是否需要重启

        :param current_focus: 当前界面的Activity
        :return: 需要重启True，否则返回False
        """
        if not current_focus:
            current_focus = LDADB(self.ld_index).get_current_focus()
        if Activity.ApplicationNotResponding in current_focus:
            print('检测到咸鱼无响应，正在重启模拟器')
            return True
        if Activity.ApplicationError in current_focus:
            print('检测到咸鱼已停止运行，正在重启模拟器')
            return True
        if Activity.Launcher in current_focus:
            print('检测到咸鱼未正常运行，正在重启模拟器')
            return True
        if 'mCurrentFocus=null' in current_focus:
            print('检测到咸鱼未正常打开，正在重启模拟器')
            return True
        if Activity.UserLoginActivity in current_focus:
            print('检测到已掉线，请登录')
        return False

    def run_task_on_target_device(self, today: date.today()):
        """在指定设备上执行任务

        :return: 目标设备不存在返回False，正常执行完毕返回True
        """
        if not LDConsole(self.ld_index).is_exist():
            print(f'目标设备{self.ld_index}不存在，无需执行任务')
            return False
        job_number = LDConsole(self.ld_index).get_job_number()
        retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
        if retrieve_idle_fish_ins.last_run_date == today:
            print(f'设备{self.ld_index}今日已执行，无需执行任务')
            return False
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
        return True

    @classmethod
    def run_task(cls, start_index, p_num=3):
        """执行任务

        :param start_index: 起始索引值
        :param p_num: 并发数量
        :return: 正常执行完毕返回True，无需执行返回False
        """
        should_run = False
        today = date.today()
        for i in range(p_num):
            index = start_index + i
            if LDConsole(index).is_exist():
                job_number = LDConsole(index).get_job_number()
                retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
                if not retrieve_idle_fish_ins.last_run_date:
                    should_run = True
                elif retrieve_idle_fish_ins.last_run_date < today:
                    should_run = True
                print(f'设备{index}存在，name={LDConsole(index).get_name()}，last_run_date='
                      f'{retrieve_idle_fish_ins.last_run_date}，today={today}，{datetime.now()}')
            else:
                print(f'设备{index}不存在，{datetime.now()}')
        if not should_run:
            print('本轮设备全部不存在或者已执行，无需进行执行任务的操作\n')
            return False
        for i in range(p_num):
            index = start_index + i
            if not LDConsole(index).is_exist():
                print(f'设备{index}不存在，正在执行下一项')
                if i == p_num - 1:
                    sleep(60)
                continue
            job_number = LDConsole(index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            if retrieve_idle_fish_ins.last_run_date == today:
                print(f'设备{index}今日已执行，正在执行下一项')
                if i == p_num - 1:
                    sleep(60)
                continue
            if i == p_num - 1:
                cls(index).run_app()
            elif i == 0:
                cls(index).run_app(1)
            else:
                cls(index).run_app(26)
        for i in range(p_num):
            cls(start_index + i).run_task_on_target_device(today)
        sleep(69)
        for i in range(p_num):
            index = start_index + i
            if not LDConsole(index).is_exist():
                print(f'目标设备{index}不存在，无需进行执行任务后的收尾工作')
                continue
            job_number = LDConsole(index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            if retrieve_idle_fish_ins.last_run_date == today:
                print(f'目标设备{index}今日已执行，无需进行执行任务后的收尾工作')
                continue
            LDConsole.quit(index)
            job_number = LDConsole(index).get_job_number()
            if today != RetrieveIdleFish(job_number).last_run_date:
                UpdateIdleFish(job_number).update_last_run_date(today)
            print(f'第{index}项已执行完毕')
        return True

    @classmethod
    def mainloop(cls, start_index, end_index, p_num=3):
        """主循环

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        :param p_num: 并发数量
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
            cls.run_task(start_index, p_num)
            start_index += p_num
            if start_index > end_index:
                print(f'所有共{end_index - src_start_index + 1}项已执行完毕，'
                      f'当前时间为：{datetime.now()}')
                start_index = src_start_index = 1
                start_day = date.today() + timedelta(days=1)