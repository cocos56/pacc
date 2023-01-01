"""咸鱼全自动刷咸鱼币中央监控系统模块"""
import os
from datetime import date, datetime, timedelta
from psutil import cpu_percent

from .ld_proj import LDProj
from ..adb import LDConsole, LDADB, LDUIA
from ..base import sleep, print_err
from ..tools import create_dir
from ..mysql import RetrieveIdleFish, UpdateIdleFish


class Activity:  # pylint: disable=too-few-public-methods
    """咸鱼全自动刷咸鱼币中央监控系统模块的安卓活动名类"""
    MainActivity = 'com.taobao.idlefish/com.taobao.idlefish.maincontainer.activity.MainActivity'
    UserLoginActivity = 'com.taobao.idlefish/com.ali.user.mobile.login.ui.UserLoginActivity'
    Launcher = 'com.android.launcher3/com.android.launcher3.Launcher'
    ApplicationNotResponding = 'Application Not Responding: com.taobao.idlefish'
    ApplicationError = 'Application Error: com.taobao.idlefish'


class IdleFish(LDProj):
    """咸鱼类"""

    def __init__(self, ld_index=1):
        """构造函数

        :param ld_index: 目标雷电模拟器的索引值
        """
        super().__init__()
        self.ld_index = ld_index

    @classmethod
    def backups(cls, start_index, end_index, dir_path='E:/ldbks'):
        """批量备份雷电模拟器的设备

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        :param dir_path: 备份文件夹的目录
        """
        src_start_index = start_index
        dir_path = f'{dir_path}/' + str(date.today()).replace('-', '_')
        create_dir(dir_path)
        start_datetime = datetime.now()
        while True:
            print(f'开始执行时的时间为{datetime.now()}')
            LDConsole(start_index).backup(dir_path)
            now = datetime.now()
            used_datetime = now-start_datetime
            executed_num = start_index- src_start_index + 1
            average_datetime = used_datetime/(start_index- src_start_index + 1)
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

    def use_best_deal_to_top_mobile_up(self):
        """薅羊毛赚话费（使用最优方案充话费）"""

    @classmethod
    def check_version_on_target_device(cls, index):
        """检查目标设备上的版本是否存在问题

        :param index: 目标设备的索引值
        :return: 目标设备不存在返回False，正常检查完毕返回True
        """
        if not LDConsole(index).is_exist():
            print('目标设备不存在，无需检查')
            sleep(10)
            return False
        print(f'正在准备检查设备{index}上的的闲鱼版本号')
        version_info = LDADB(index).get_app_version_info('com.taobao.idlefish')
        job_number = LDConsole(index).get_job_number()
        if version_info not in ('0.0.0', RetrieveIdleFish(job_number).version):
            UpdateIdleFish(job_number).update_version(version_info)
        if version_info == '7.5.41':
            print('当前的闲鱼版本过老，需要升级')
        print(f'模拟器{index}上的闲鱼版本为：{version_info}')
        LDConsole.quit(index)
        print(f'第{index}项已检查完毕\n')
        return True

    @classmethod
    def check_version(cls, start_index, end_index, p_num=5):
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
            for i in range(p_num):
                index = start_index + i
                if LDConsole(index).is_exist():
                    job_number = LDConsole(index).get_job_number()
                    retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
                    if not retrieve_idle_fish_ins.version:
                        should_run = True
                    elif retrieve_idle_fish_ins.version != '7.8.10':
                        should_run = True
                    print(f'设备{index}存在，version={retrieve_idle_fish_ins.version}'
                          f'，{datetime.now()}')
                else:
                    print(f'设备{index}不存在，{datetime.now()}')
            if not should_run:
                print('本轮设备全部不存在或已是最新版本，无需进行检查版本信息的操作\n')
                start_index += p_num
                continue
            for i in range(p_num):
                cls(start_index + i).launch()
            sleep(5)
            for i in range(p_num):
                cls.check_version_on_target_device(start_index + i)
            start_index += p_num

    # pylint: disable=too-many-return-statements, too-many-branches, too-many-statements
    # pylint: disable=too-many-locals
    @classmethod
    def check_target_device(cls, index, reopen_flag=False):
        """检查目标设备是否存在问题

        :param index: 目标设备的索引值
        :param reopen_flag: 是否需要重启模拟器并打开闲鱼app
        :return: 目标设备不存在返回False，正常检查完毕返回True
        """
        if reopen_flag:
            cls(index).run_app(30)
        if not LDConsole(index).is_exist():
            print(f'目标设备{index}不存在，无需检查')
            sleep(10)
            return False
        print(f'正在准备检查设备{index}')
        current_focus = LDADB(index).get_current_focus()
        if cls(index).should_restart(current_focus):
            return cls.check_target_device(index, reopen_flag=True)
        lduia_ins = LDUIA(index)
        if Activity.UserLoginActivity in current_focus:
            lduia_ins.get_screen()
            LDConsole.quit(index)
            print(f'第{index}项已检查完毕\n')
            return False
        lduia_ins.tap((50, 85), 9)
        try:
            if lduia_ins.get_dict(content_desc='数码店'):
                lduia_ins.tap((270, 652), 3)
                lduia_ins.tap((268, 809), 6)
                return cls.check_target_device(index, reopen_flag=True)
        except FileNotFoundError as err:
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
        for _ in range(int(ex_p/200)):
            lduia_ins.tap((276, 600), 0.1)
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
        job_number = LDConsole(index).get_job_number()
        retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
        update_idle_fish_ins = UpdateIdleFish(job_number)
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
        if os.path.exists(new_png):
            os.remove(new_png)
        os.rename(png_path, new_png)
        LDConsole.quit(index)
        today = date.today()
        if today != retrieve_idle_fish_ins.last_check_date:
            update_idle_fish_ins.update_last_check_date(today)
        print(f'第{index}项已检查完毕\n')
        return True

    @classmethod
    def check_even_devices(cls, start_index, end_index):
        """检查索引值为偶数的设备是否存在问题

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        if start_index % 2:
            start_index += 1
        while True:
            cls(start_index).run_app(15)
            cls.check_target_device(start_index)
            if start_index+1 >= end_index:
                print(f'所有共{(end_index-src_start_index+1)/2}项已检查完毕')
                break
            start_index += 2

    @classmethod
    def check_odd_devices(cls, start_index, end_index):
        """检查编号为奇数的设备是否存在问题

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        if not start_index % 2:
            start_index += 1
        while True:
            cls(start_index).run_app(15)
            cls.check_target_device(start_index)
            if start_index+1 >= end_index:
                print(f'所有共{(end_index-src_start_index+1)/2}项已检查完毕')
                break
            start_index += 2

    @classmethod
    def check_after_run(cls, start_index, end_index):
        """从数据库中读取到运行过的状态之后再进行检查

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        """
        src_start_index = start_index
        while True:
            print(datetime.now())
            if not LDConsole(start_index).is_exist():
                print(f'目标设备{start_index}不存在，无需检查\n')
                start_index += 1
                if start_index - 1 >= end_index:
                    print(
                        f'所有共{end_index - src_start_index + 1}项已检查完毕，当前时间为：'
                        f'{datetime.now()}\n')
                    src_start_index = start_index = 1
                    sleep(600)
                continue
            job_number = LDConsole(start_index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            print(start_index)
            print(retrieve_idle_fish_ins.last_run_date)
            print(retrieve_idle_fish_ins.last_check_date)
            if not retrieve_idle_fish_ins.last_check_date:
                pass
            elif not retrieve_idle_fish_ins.last_run_date:
                start_index += 1
                print()
                continue
            elif retrieve_idle_fish_ins.last_run_date <= retrieve_idle_fish_ins.last_check_date:
                start_index += 1
                print()
                continue
            cpu_use = cpu_percent()
            print(cpu_use)
            while cpu_use > 60:
                sleep(5)
                cpu_use = cpu_percent(1)
                print(cpu_use)
            cls(start_index).run_app(13)
            cls.check_target_device(start_index)
            start_index += 1

    @classmethod
    def check(cls, start_index, end_index, p_num=3):
        """检查是否存在问题

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        :param p_num: 并发数量
        """
        src_start_index = start_index
        while True:
            now = datetime.now()
            if now.hour >= 23 and now.minute >= 50:
                break
            print(now)
            for i in range(p_num):
                if i == p_num - 1:
                    cls(start_index+i).run_app(13)
                elif i == 0:
                    cls(start_index + i).run_app(1)
                else:
                    cls(start_index + i).run_app(5)
            for i in range(p_num):
                cls.check_target_device(start_index+i)
            if start_index+p_num-1 >= end_index:
                print(f'所有共{end_index-src_start_index+1}项已检查完毕，当前时间为：{datetime.now()}')
                break
            start_index += p_num

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

    def run_task_on_target_device(self):
        """在指定设备上执行任务

        :return: 目标设备不存在返回False，正常执行完毕返回True
        """
        print(f'准备在目标设备{self.ld_index}上执行任务')
        if not LDConsole(self.ld_index).is_exist():
            print(f'目标设备{self.ld_index}不存在，无需执行任务')
            sleep(10)
            return False
        print(f'目标设备{self.ld_index}存在，可以向下执行任务')
        while self.should_restart():
            self.run_app()
        lduia_ins = LDUIA(self.ld_index)
        lduia_ins.tap((479, 916), 6)
        lduia_ins.get_screen()
        try:
            lduia_ins.get_current_ui_hierarchy()
        except FileNotFoundError as err:
            print_err(err)
            self.run_app()
            return self.run_task_on_target_device()
        if self.should_restart():
            return self.run_task_on_target_device()
        return True

    @classmethod
    def run_task(cls, start_index, p_num=3):
        """执行任务

        :param start_index: 起始索引值
        :param p_num: 并发数量
        :return: 正常执行完毕返回True，无需执行返回False
        """
        should_run = False
        for i in range(p_num):
            index = start_index + i
            if LDConsole(index).is_exist():
                job_number = LDConsole(index).get_job_number()
                retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
                today = date.today()
                if not retrieve_idle_fish_ins.last_run_date:
                    should_run = True
                elif retrieve_idle_fish_ins.last_run_date < today:
                    should_run = True
                print(f'设备{index}存在，last_run_date={retrieve_idle_fish_ins.last_run_date}'
                      f'，today={today}，{datetime.now()}')
            else:
                print(f'设备{index}不存在，{datetime.now()}')
        if not should_run:
            print('本轮设备全部不存在或者已执行，无需进行执行任务的操作\n')
            return False
        for i in range(p_num):
            if i == p_num - 1:
                cls(start_index + i).run_app()
            elif i == 0:
                cls(start_index+i).run_app(1)
            else:
                cls(start_index+i).run_app(26)
        for i in range(p_num):
            cls(start_index+i).run_task_on_target_device()
        sleep(69)
        for i in range(p_num):
            index = start_index + i
            if not LDConsole(index).is_exist():
                print(f'目标设备{index}不存在，无需进行执行任务后的收尾工作')
                continue
            LDConsole.quit(index)
            job_number = LDConsole(index).get_job_number()
            today = date.today()
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
        if start_index <= 1 and datetime.now().hour >= 9:
            start_day = date.today() + timedelta(days=1)
        else:
            start_day = date.today()
        while True:
            while start_day != date.today():
                seconds = (datetime.fromisoformat(
                    f'{date.today() + timedelta(days=1)} 00:00:00') - datetime.now()).seconds
                if seconds > 3600:
                    sleep(3600)
                else:
                    sleep(seconds)
            cls.run_task(start_index, p_num)
            if start_index + p_num - 1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已执行完毕，'
                      f'当前时间为：{datetime.now()}')
                start_index = src_start_index = 1
                start_day = date.today() + timedelta(days=1)
            start_index += p_num
