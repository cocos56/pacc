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
    login_guide_bar = 'com.taobao.idlefish:id/login_guide_bar'
    login_onekey_btn = 'com.taobao.idlefish:id/login_onekey_btn'


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

    def is_logout(self, work_name: str, current_focus='', depth=0) -> bool:
        """判断设备是否已掉线（需要重新登录）

        :param work_name: 工作名
        :param current_focus: 当前界面的Activity
        :param depth: 递归深度
        :return: 已掉线更新数据库里的在线状态并返回True，否则返回False
        """
        if not current_focus:
            current_focus = LDADB(self.ld_index).get_current_focus()
        lduia_ins = LDUIA(self.ld_index)
        try:
            if Activity.UserLoginActivity in current_focus or lduia_ins.get_dict(
                    ResourceID.login_guide_bar):
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
        except FileNotFoundError as err:
            print_err(err)
            if depth < 3:
                return self.is_logout(work_name, depth=depth+1)
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

    # pylint: disable=too-many-branches, too-many-statements, too-many-return-statements
    def top_up_mobile_on_target_device(self, reopen_flag=True) -> bool:
        """在特定设备上进行薅羊毛赚话费

        :param reopen_flag: 重启闲鱼的标志
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
        if retrieve_idle_fish_ins.last_top_up_mobile_date and retrieve_idle_fish_ins. \
                last_top_up_mobile_date >= today:
            print(f'今天已在设备{self.ld_index}上执行过薅羊毛赚话费的任务，无需重复执行')
            return False
        if retrieve_idle_fish_ins.login:
            print(f'目标设备{self.ld_index}已掉线，无法执行薅羊毛赚话费的任务\n')
            return False
        self.run_app(19)
        if self.is_logout('执行薅羊毛赚话费的任务'):
            return False
        lduia_ins = LDUIA(self.ld_index)
        lduia_ins.tap((50, 85), 6)
        lduia_ins.tap((479, 596), 3)  # 点击赚经验
        LDADB(self.ld_index).get_current_focus()
        try:
            if lduia_ins.get_dict(content_desc=r'HI，店长 '):
                print('当前界面需要先点击一下升级小店然后再点击赚经验')
                lduia_ins.tap((266, 599), 3)
                lduia_ins.tap((479, 596), 3)  # 点击赚经验
                lduia_ins.xml = ''
            elif lduia_ins.get_dict(content_desc='数码店', xml=lduia_ins.xml):
                print('当前界面需要先点击一下选好了然后再点击赚经验')
                lduia_ins.tap((270, 652), 3)  # 点击数码店
                lduia_ins.tap((268, 809), 6)  # 点击选好了
                lduia_ins.tap((479, 596), 3)  # 点击赚经验
                lduia_ins.xml = ''
        except FileNotFoundError as err:
            print_err(err)
            return self.top_up_mobile_on_target_device(reopen_flag)
        try:
            if not lduia_ins.get_dict(content_desc='提醒签到', xml=lduia_ins.xml):
                print('当前界面不是赚经验的界面，正在重新执行')
                return self.top_up_mobile_on_target_device(reopen_flag)
        except FileNotFoundError as err:
            print_err(err)
            return self.top_up_mobile_on_target_device(reopen_flag)
        try:
            if lduia_ins.get_dict(content_desc='薅羊毛赚话费', xml=lduia_ins.xml):
                lduia_ins.tap((460, 350), 20)
        except FileNotFoundError as err:
            print_err(err)
            return self.top_up_mobile_on_target_device(reopen_flag)
        png_path = lduia_ins.get_screen()
        dir_name = f'CurrentUIHierarchy/{str(date.today()).replace("-", "_")}_top_up_mobile'
        create_dir(dir_name)
        new_png = f'{dir_name}/{LDConsole(self.ld_index).get_name()}.png'
        if path.exists(new_png):
            remove(new_png)
        try:
            rename(png_path, new_png)
        except FileNotFoundError as err:
            print_err(err)
            return self.top_up_mobile_on_target_device(reopen_flag)
        try:
            lduia_ins.get_current_ui_hierarchy()
        except FileNotFoundError as err:
            print_err(err)
        if reopen_flag:
            self.run_app(19)
            LDConsole.quit(self.ld_index)
        if not retrieve_idle_fish_ins.top_up_mobile_cnt:
            top_up_mobile_cnt = 1
        else:
            top_up_mobile_cnt = retrieve_idle_fish_ins.top_up_mobile_cnt + 1
        UpdateIdleFish(job_number).update_top_up_mobile_cnt(top_up_mobile_cnt)
        UpdateIdleFish(job_number).update_last_top_up_mobile_date(today)
        return True

    def first_buy_on_target_device(self, today: date.today()): # pylint: disable=too-many-locals
        """在特定设备上进行首次购买（下单）

        :param today: 今日的日期
        :return: 正常走完首次购买的流程返回本次回收的闲鱼币币值，否则返回False
        """
        now = datetime.now()
        print(now)
        if not LDConsole(self.ld_index).is_exist():
            print(f'设备{self.ld_index}不存在，无需购买')
            return False
        job_number = LDConsole(self.ld_index).get_job_number()
        retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
        coins = retrieve_idle_fish_ins.coins
        print(f'start_index={self.ld_index}, device_name={LDConsole(self.ld_index).get_name()}, '
              f'buy={retrieve_idle_fish_ins.buy}, coins={coins}, '
              f'today={today}')
        if not retrieve_idle_fish_ins.buy:
            print(f'设备{self.ld_index}上的是否需要购买的标志为'
                  f'{retrieve_idle_fish_ins.buy}，无需购买')
            return False
        if retrieve_idle_fish_ins.login:
            print(f'设备{self.ld_index}上的账号已掉线，login={retrieve_idle_fish_ins.login}，无法购买')
            return False
        self.run_app(19)
        if self.is_logout('购买'):
            return False
        lduia_ins = LDUIA(self.ld_index)
        ldadb_ins = LDADB(self.ld_index)
        try:
            lduia_ins.click(ResourceID.search_bg_img_front)
        except FileNotFoundError as err:
            print_err(err)
            return self.first_buy_on_target_device(today)
        ldadb_ins.input_text('xgqm')
        try:
            if 'xgqm' not in lduia_ins.get_dict(class_='android.widget.EditText').get('@text'):
                return self.first_buy_on_target_device(today)
        except FileNotFoundError as err:
            print_err(err)
            return self.first_buy_on_target_device(today)
        except AttributeError as err:
            print_err(err)
            return False
        try:
            lduia_ins.click(content_desc='搜索')
            lduia_ins.click(content_desc='用户')
            lduia_ins.click(content_desc='会员名')
            while lduia_ins.click(content_desc='徐哥亲笔签名拍照版'):
                pass
        except FileNotFoundError as err:
            print_err(err)
            return self.first_buy_on_target_device(today)
        lduia_ins.click(content_desc='我想要', xml=lduia_ins.xml)
        try:
            if not lduia_ins.click(content_desc='立即购买'):
                naf_err_cnt = 0
                while not lduia_ins.click(naf='true', index='3'):
                    sleep(1)
                    naf_err_cnt += 1
                    if naf_err_cnt >= 5:
                        break
                lduia_ins.click(content_desc='再次购买')
                if naf_err_cnt >= 5:
                    return self.first_buy_on_target_device(today)
        except FileNotFoundError as err:
            print_err(err)
            return self.first_buy_on_target_device(today)
        if retrieve_idle_fish_ins.login:
            print(f'设备{self.ld_index}上的账号已掉线，login={retrieve_idle_fish_ins.login}，无法购买')
            return False
        if Activity.Launcher in LDADB(self.ld_index).get_current_focus():
            return self.first_buy_on_target_device(today)
        if coins >= 50000:
            last_buy_coins = 50000
        elif coins >= 40000:
            last_buy_coins = 40000
        elif coins >= 30000:
            last_buy_coins = 30000
        elif coins >= 20000:
            last_buy_coins = 20000
        elif coins >= 10000:
            last_buy_coins = 10000
        else:
            return False
        last_buy_coins = min(last_buy_coins, retrieve_idle_fish_ins.reminder_threshold)
        try:
            lduia_ins.click(ResourceID.tv_value, str(last_buy_coins // 100))
        except FileNotFoundError as err:
            print_err(err)
            return self.first_buy_on_target_device(today)
        try:
            lduia_ins.click(text='立即购买')
        except FileNotFoundError as err:
            print_err(err)
            return self.first_buy_on_target_device(today)
        LDADB(self.ld_index).get_current_focus()
        sleep(1)
        try:
            lduia_ins.click(content_desc='确认购买')
        except FileNotFoundError as err:
            print_err(err)
            return self.first_buy_on_target_device(today)
        sleep(2)
        try:
            if lduia_ins.get_dict(content_desc='确认购买'):
                return self.first_buy_on_target_device(today)
        except FileNotFoundError as err:
            print_err(err)
        try:
            if lduia_ins.get_dict(text='账户支付功能已关闭'):
                print(f'设备{self.ld_index}账户支付功能已关闭')
                return False
        except FileNotFoundError as err:
            print_err(err)
        if lduia_ins.click(index='3', text='添加收货地址', xml=lduia_ins.xml):
            print(f'设备{self.ld_index}上的账号需要添加收货地址')
            return False
        update_idle_fish_ins = UpdateIdleFish(job_number)
        update_idle_fish_ins.update_last_buy_coins(last_buy_coins)
        update_idle_fish_ins.update_last_buy_date(today)
        return last_buy_coins

    def second_buy_on_target_device(self, today: date.today()):
        """在特定设备上进行二次购买（下单）

        :param today: 今日的日期
        :return: 正常走完二次购买的流程返回本次回收的闲鱼币币值，否则返回False
        """
        now = datetime.now()
        print(now)
        if not LDConsole(self.ld_index).is_exist():
            print(f'设备{self.ld_index}不存在，无需购买')
            return False
        job_number = LDConsole(self.ld_index).get_job_number()
        retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
        coins = retrieve_idle_fish_ins.coins
        print(f'start_index={self.ld_index}, device_name={LDConsole(self.ld_index).get_name()}, '
              f'buy={retrieve_idle_fish_ins.buy}, coins={coins}, '
              f'today={today}')
        if not retrieve_idle_fish_ins.buy:
            print(f'设备{self.ld_index}上的是否需要购买的标志为'
                  f'{retrieve_idle_fish_ins.buy}，无需购买')
            return False
        if retrieve_idle_fish_ins.login:
            print(f'设备{self.ld_index}上的账号已掉线，login={retrieve_idle_fish_ins.login}，无法购买')
            return False
        self.run_app(19)
        if self.is_logout('购买'):
            return False
        lduia_ins = LDUIA(self.ld_index)
        ldadb_ins = LDADB(self.ld_index)
        try:
            lduia_ins.click(ResourceID.tab_title, '消息')
            if lduia_ins.click(text='我知道了'):
                lduia_ins.xml = ''
            while not lduia_ins.click(index='1', content_desc='xgqm', xml=lduia_ins.xml):
                current_focus = LDADB(self.ld_index).get_current_focus()
                if lduia_ins.click(index='0', content_desc='xgqm', xml=lduia_ins.xml) or \
                        Activity.Launcher in current_focus:
                    break
                if Activity.WebHybridActivity in current_focus:
                    ldadb_ins.press_back_key()
                    if self.is_logout('购买'):
                        break
                ldadb_ins.swipe([290, 690], [290, 330], 500)
                lduia_ins.xml = ''
        except FileNotFoundError as err:
            print_err(err)
            return self.second_buy_on_target_device(today)
        if retrieve_idle_fish_ins.login:
            print(f'设备{self.ld_index}上的账号已掉线，login={retrieve_idle_fish_ins.login}，无法购买')
            return False
        if Activity.Launcher in LDADB(self.ld_index).get_current_focus():
            return self.second_buy_on_target_device(today)
        sleep(1)
        try:
            while not lduia_ins.click(naf='true', index='3'):
                sleep(1)
                if lduia_ins.click(content_desc='立即购买'):
                    break
        except FileNotFoundError as err:
            print_err(err)
            return self.second_buy_on_target_device(today)
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
            lduia_ins.click(text='立即购买')
            LDADB(self.ld_index).get_current_focus()
            sleep(1)
            lduia_ins.click(content_desc='确认购买')
        except FileNotFoundError as err:
            print_err(err)
            return self.second_buy_on_target_device(today)
        sleep(2)
        try:
            if lduia_ins.get_dict(content_desc='确认购买'):
                return self.second_buy_on_target_device(today)
        except FileNotFoundError as err:
            print_err(err)
        try:
            if lduia_ins.get_dict(text='账户支付功能已关闭'):
                print(f'设备{self.ld_index}账户支付功能已关闭')
                return False
        except FileNotFoundError as err:
            print_err(err)
        if lduia_ins.click(index='3', text='添加收货地址', xml=lduia_ins.xml):
            print(f'设备{self.ld_index}上的账号需要添加收货地址')
            return False
        update_idle_fish_ins = UpdateIdleFish(job_number)
        update_idle_fish_ins.update_last_buy_coins(last_buy_coins)
        update_idle_fish_ins.update_last_buy_date(today)
        return last_buy_coins
