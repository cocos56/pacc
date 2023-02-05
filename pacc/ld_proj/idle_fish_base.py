"""闲鱼全自动刷闲鱼币中央监控系统基类模块"""
# pylint: disable=duplicate-code
from datetime import datetime, date
from os import path, rename, remove

from .ld_proj import LDProj
from ..adb import LDConsole, LDADB, LDUIA
from ..base import sleep, print_err
from ..mysql import RetrieveIdleFish, UpdateIdleFish
from ..tools import create_dir


class Activity:  # pylint: disable=too-few-public-methods
    """闲鱼全自动刷咸鱼币中央监控系统模块的安卓活动名类"""
    MainActivity = 'com.taobao.idlefish/com.taobao.idlefish.maincontainer.activity.MainActivity'
    UserLoginActivity = 'com.taobao.idlefish/com.ali.user.mobile.login.ui.UserLoginActivity'
    Launcher = 'com.android.launcher3/com.android.launcher3.Launcher'
    ApplicationNotResponding = 'Application Not Responding: com.taobao.idlefish'
    ApplicationError = 'Application Error: com.taobao.idlefish'
    WebViewActivity = 'com.taobao.idlefish/com.ali.user.mobile.ability.webview.WebViewActivity'
    WebHybridActivity = 'com.taobao.idlefish/com.taobao.idlefish.webview.WebHybridActivity'


class ResourceID:  # pylint: disable=too-few-public-methods
    """闲鱼全自动刷咸鱼币中央监控系统模块的安卓资源ID类"""
    aliuser_login_mobile_et = 'com.taobao.idlefish:id/aliuser_login_mobile_et'
    login_password_btn = 'com.taobao.idlefish:id/login_password_btn'
    confirm = 'com.taobao.idlefish:id/confirm'
    aliuser_login_show_password_btn = 'com.taobao.idlefish:id/aliuser_login_show_password_btn'
    aliuser_login_password_et = 'com.taobao.idlefish:id/aliuser_login_password_et'
    aliuser_login_login_btn = 'com.taobao.idlefish:id/aliuser_login_login_btn'
    aliuser_login_account_et = 'com.taobao.idlefish:id/aliuser_login_account_et'
    tab_title = 'com.taobao.idlefish:id/tab_title'
    tv_value = 'com.taobao.idlefish:id/tv_value'
    ali_user_guide_tb_login_btn = 'com.taobao.idlefish:id/ali_user_guide_tb_login_btn'
    search_bg_img_front = 'com.taobao.idlefish:id/search_bg_img_front'


class IdleFishBase(LDProj):
    """闲鱼基类"""

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
        """启动雷电模拟器并运行闲鱼APP

        :param sleep_time: 等待时间
        """
        if LDConsole(self.ld_index).is_exist():
            LDConsole.quit(self.ld_index)
            LDConsole(self.ld_index).run_app('com.taobao.idlefish', '闲鱼')
        else:
            print(f'设备{self.ld_index}不存在，无法启动')
        sleep(sleep_time)

    def should_restart(self, current_focus=''):
        """判断是否需要重启

        :param current_focus: 当前界面的Activity
        :return: 需要重启返回True，否则返回False
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
        return False

    def is_logout(self, work_name: str, current_focus='') -> bool:
        """判断设备是否已掉线（需要重新登录）

        :param work_name: 工作名
        :param current_focus: 当前界面的Activity
        :return: 已掉线更新数据库里的在线状态并返回True，否则返回False
        """
        if not current_focus:
            current_focus = LDADB(self.ld_index).get_current_focus()
        if Activity.UserLoginActivity in current_focus:
            print(f'检测设备{self.ld_index}到已掉线，需要重新登录')
            lduia_ins = LDUIA(self.ld_index)
            lduia_ins.get_screen()
            try:
                lduia_ins.get_current_ui_hierarchy()
            except FileNotFoundError as err:
                print_err(err)
            LDConsole.quit(self.ld_index)
            job_number = LDConsole(self.ld_index).get_job_number()
            update_idle_fish_ins = UpdateIdleFish(job_number)
            update_idle_fish_ins.update_login(1)
            print(f'设备{self.ld_index}由于已掉线，无法继续进行，{work_name}异常终止\n')
            return True
        return False

    def should_run_task(self, today: date.today()) -> bool:
        """判断是否需要执行任务

        :param today: 今日的日期
        :return: 需要执行任务返回True，否则返回False
        """
        if LDConsole(self.ld_index).is_exist():
            job_number = LDConsole(self.ld_index).get_job_number()
            retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
            if not retrieve_idle_fish_ins.last_run_date:
                return True
            if retrieve_idle_fish_ins.last_run_date < today:
                return True
            if retrieve_idle_fish_ins.login:
                print(f'目标设备{self.ld_index}已掉线，无需执行任务，{datetime.now()}')
            print(f'设备{self.ld_index}存在，name={LDConsole(self.ld_index).get_name()}，'
                  f'last_run_date={retrieve_idle_fish_ins.last_run_date}，today={today}，'
                  f'{datetime.now()}')
        else:
            print(f'设备{self.ld_index}不存在，无需执行任务，{datetime.now()}')
        return False

    def top_up_mobile_on_target_device(self) -> bool:
        """在特定设备上进行薅羊毛赚话费

        :return: 成功薅羊毛赚话费返回True，否则返回False
        """
        job_number = LDConsole(self.ld_index).get_job_number()
        retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
        today = date.today()
        print(f'start_index={self.ld_index}, device_name={LDConsole(self.ld_index).get_name()}, '
              f'top_up_mobile={retrieve_idle_fish_ins.top_up_mobile}, '
              f'top_up_mobile_cnt={retrieve_idle_fish_ins.top_up_mobile_cnt}, '
              f'last_top_up_mobile_date={retrieve_idle_fish_ins.last_top_up_mobile_date}, '
              f'today={today}')
        if retrieve_idle_fish_ins.user_name[:2] != 'xy':
            print(f'设备{self.ld_index}上的账号{retrieve_idle_fish_ins.user_name}不是以xy开头，'
                  f'无需薅羊毛赚话费')
            return False
        if not retrieve_idle_fish_ins.top_up_mobile:
            print(f'设备{self.ld_index}上的执行薅羊毛赚话费的标志为'
                  f'{retrieve_idle_fish_ins.top_up_mobile}，无需薅羊毛赚话费')
            return False
        if retrieve_idle_fish_ins.last_top_up_mobile_date and retrieve_idle_fish_ins.\
                last_top_up_mobile_date >= today:
            print(f'今天已在设备{self.ld_index}上执行过薅羊毛赚话费的任务，无需重复执行')
            return False
        self.run_app(19)
        lduia_ins = LDUIA(self.ld_index)
        lduia_ins.tap((50, 85), 6)
        lduia_ins.tap((479, 596), 3)
        LDADB(self.ld_index).get_current_focus()
        try:
            if lduia_ins.get_dict(content_desc=r'HI，店长 '):
                print('当前界面需要先点击一下升级小店然后再点击赚经验')
                lduia_ins.tap((266, 599), 3)
                lduia_ins.tap((479, 596), 3)
                lduia_ins.xml = ''
        except FileNotFoundError as err:
            print_err(err)
            self.top_up_mobile_on_target_device()
        if not lduia_ins.get_dict(content_desc='提醒签到', xml=lduia_ins.xml):
            print('当前界面不是赚经验的界面，正在重新执行')
            self.top_up_mobile_on_target_device()
        if lduia_ins.get_dict(content_desc='薅羊毛赚话费'):
            lduia_ins.tap((460, 350), 20)
        png_path = lduia_ins.get_screen()
        dir_name = f'CurrentUIHierarchy/{str(date.today()).replace("-", "_")}_top_up_mobile'
        create_dir(dir_name)
        new_png = f'{dir_name}/{LDConsole(self.ld_index).get_name()}.png'
        if path.exists(new_png):
            remove(new_png)
        rename(png_path, new_png)
        try:
            lduia_ins.get_current_ui_hierarchy()
        except FileNotFoundError as err:
            print_err(err)
        self.run_app(19)
        LDConsole.quit(self.ld_index)
        if not retrieve_idle_fish_ins.top_up_mobile_cnt:
            top_up_mobile_cnt = 1
        else:
            top_up_mobile_cnt = retrieve_idle_fish_ins.top_up_mobile_cnt + 1
        UpdateIdleFish(job_number).update_top_up_mobile_cnt(top_up_mobile_cnt)
        UpdateIdleFish(job_number).update_last_top_up_mobile_date(today)
        return True
