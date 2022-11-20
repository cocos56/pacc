"""咸鱼全自动刷咸鱼币中央监控系统模块"""
import os
from datetime import date, datetime, timedelta

from .ld_proj import LDProj
from ..adb import LDConsole, LDADB, LDUIA
from ..base import sleep, print_err
from ..tools import create_dir


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
    def check_version_target_device(cls, index):
        """检查目标设备上的版本是否存在问题

        :param index: 目标设备的索引值
        :return: 目标设备不存在返回False，正常检查完毕返回True
        """
        if not LDConsole(index).is_exist():
            print('目标设备不存在，无需检查')
            sleep(10)
            return False
        version_info = LDADB(index).get_app_version_info('com.taobao.idlefish')
        if version_info == '7.5.41':
            print('当前版本过老，需要升级')
        print(f'模拟器{index}上的咸鱼版本为：{version_info}')
        LDConsole.quit(index)
        print(f'第{index}项已检查完毕\n')
        return True

    @classmethod
    def check_version(cls, start_index, end_index, p_num=3):
        """检查版本是否存在问题

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        :param p_num: 并发数量
        """
        src_start_index = start_index
        while True:
            for i in range(p_num):
                cls(start_index + i).launch()
            sleep(10)
            for i in range(p_num):
                cls.check_version_target_device(start_index + i)
            if start_index + p_num - 1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已检查版本完毕')
                break
            start_index += p_num

    @classmethod
    def check_target_device(cls, index):  # pylint: disable=too-many-return-statements
        """检查目标设备是否存在问题

        :param index: 目标设备的索引值
        :return: 目标设备不存在返回False，正常检查完毕返回True
        """
        if not LDConsole(index).is_exist():
            print('目标设备不存在，无需检查')
            sleep(10)
            return False
        current_focus = LDADB(index).get_current_focus()
        if cls(index).should_restart(current_focus):
            cls(index).run_app()
            return cls.check_target_device(index)
        lduia_ins = LDUIA(index)
        if Activity.UserLoginActivity in current_focus:
            lduia_ins.get_screen()
            LDConsole.quit(index)
            print(f'第{index}项已检查完毕\n')
            return False
        lduia_ins.tap((50, 85), 10)
        try:
            if lduia_ins.get_dict(content_desc='数码店'):
                lduia_ins.tap((270, 652), 3)
                lduia_ins.tap((268, 809), 6)
                lduia_ins.get_screen()
                cls(index).run_app()
                return cls.check_target_device(index)
        except FileNotFoundError as err:
            print_err(err)
            cls(index).run_app()
            return cls.check_target_device(index)
        dic = lduia_ins.get_dict('android:id/content', xml=lduia_ins.xml)['node']
        try:
            coins = dic[1]['node']['node']['node']['node']['node'][1]['@content-desc']
            if '万' in coins:
                coins = float(coins[:-1]) * 10000
            coins = int(coins)
        except (KeyError, TypeError) as err:
            print_err(err)
            cls(index).run_app()
            return cls.check_target_device(index)
        png_path = lduia_ins.get_screen()
        dir_name = 'CurrentUIHierarchy/' + str(date.today()).replace('-', '_')
        if coins >= 30000:
            dir_name = f'{dir_name}_30k'
        elif coins >= 20000:
            dir_name = f'{dir_name}_20k'
        elif coins >= 15000:
            dir_name = f'{dir_name}_15k'
        elif coins >= 10000:
            dir_name = f'{dir_name}_10k'
        create_dir(dir_name)
        new_png = f'{dir_name}/{LDConsole(index).get_name()}.png'
        if os.path.exists(new_png):
            os.remove(new_png)
        os.rename(png_path, new_png)
        LDConsole.quit(index)
        print(f'第{index}项已检查完毕\n')
        return True

    @classmethod
    def check(cls, start_index, end_index, p_num=3):
        """检查是否存在问题

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        :param p_num: 并发数量
        """
        src_start_index = start_index
        while True:
            for i in range(p_num):
                cls(start_index+i).run_app(10)
            # cls(start_index + 1).run_app(10)
            # cls(start_index + 2).run_app(10)
            for i in range(p_num):
                cls.check_target_device(start_index+i)
            # cls.check_target_device(start_index + 1)
            # cls.check_target_device(start_index + 2)
            if start_index+p_num-1 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已检查完毕')
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
        if not LDConsole(self.ld_index).is_exist():
            print('目标设备不存在，无需执行任务')
            sleep(10)
            return False
        while self.should_restart():
            self.run_app()
        lduia_ins = LDUIA(self.ld_index)
        lduia_ins.tap((479, 916), 10)
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
    def run_task(cls, start_index):
        """执行任务

        :param start_index: 起始索引值
        """
        cls(start_index).run_app(1)
        cls(start_index + 1).run_app(26)
        cls(start_index + 2).run_app()
        cls(start_index).run_task_on_target_device()
        cls(start_index + 1).run_task_on_target_device()
        cls(start_index + 2).run_task_on_target_device()
        sleep(69)
        LDConsole.quit(start_index)
        print(f'第{start_index}项已执行完毕')
        LDConsole.quit(start_index + 1)
        print(f'第{start_index + 1}项已执行完毕')
        LDConsole.quit(start_index + 2)
        print(f'第{start_index + 2}项已执行完毕\n')

    @classmethod
    def mainloop(cls, start_index, end_index, p_num=3):
        """主循环

        :param start_index: 起始索引值
        :param end_index: 终止索引值
        :param p_num: 并发数量
        """
        src_start_index = start_index
        if datetime.now().hour >= 10:
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
            cls.run_task(start_index)
            if start_index + 2 >= end_index:
                print(f'所有共{end_index - src_start_index + 1}项已执行完毕')
                start_index = src_start_index - 3
                start_day = date.today() + timedelta(days=1)
                cls.check(src_start_index, end_index, p_num)
            start_index += 3
