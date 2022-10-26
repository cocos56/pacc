"""安卓调试桥模块"""
import base64
from datetime import date
from os import popen, system
from random import randint

from ..base import print_err, sleep
from ..config import Config
from ..mysql import RetrieveMobileInfo, UpdateMobileInfo
from ..tools import find_all_with_re, EMail, find_all_ints_with_re


def get_online_devices():
    """获取所有在线设备"""
    res = popen('adb devices').read()
    res = find_all_with_re(res, r'(.+)\tdevice')
    for i, _ in enumerate(res):
        res[i] = res[i].replace(':5555', '')
    return res


class ADB:  # pylint: disable=too-many-public-methods
    """安卓调试桥类"""

    def __init__(self, serial_num, offline_cnt=1):
        """构造函数：初始化安卓调试桥类的对象

        :param serial_num: 设备序列号
        :param offline_cnt: 离线次数计数器
        """
        self.dbr = RetrieveMobileInfo.get_ins(serial_num)
        self.dbu = UpdateMobileInfo(serial_num)
        if self.dbr.id_num not in get_online_devices():
            if self.dbr.ipv4_addr in get_online_devices():
                self.reboot()
            else:
                if not offline_cnt % 20:
                    EMail(self.dbr.serial_num).send_offline_error()
                print(f'{self.dbr.serial_num}不在线，该设备的ID为：{self.dbr.id_num}，请核对！')
                sleep(30)
                # pylint: disable=non-parent-init-called
                system('adb reconnect offline')
                self.__init__(serial_num, offline_cnt+1)
        self.cmd = f'adb -s {self.dbr.id_num} '
        if not self.get_ipv4_address():
            print(self.get_ipv4_address())
            sleep(60)
            # pylint: disable=non-parent-init-called
            self.__init__(serial_num)
        if not self.get_ipv4_address() == self.dbr.ipv4_addr:
            self.dbu.update_ipv4_addr(self.get_ipv4_address())
        if not Config.debug:
            self.reconnect()
        self.cmd = f'adb -s {self.dbr.ipv4_addr} '
        model = self.get_model()
        while not model:
            model = self.get_model()
        if not model == self.dbr.model:
            self.dbu.update_model(model)
        if 'com.android.settings/com.android.settings.Settings$UsbDetailsActivity' in \
                self.get_current_focus():
            if self.dbr.model in ['M2007J22C', 'Redmi K20 Pro Premium Edition']:
                self.press_back_key(6)

    def get_battery_temperature(self):
        """获取电池温度

        :return: 摄氏度的数值
        """
        res = popen(f'{self.cmd}shell dumpsys battery | findstr "temperature"').read()
        # print(res)
        try:
            return find_all_ints_with_re(res)[0]/10
        except IndexError as err:
            print_err(err)
            self.keep_online()
            return self.get_battery_temperature()

    def get_cpu_temperature(self):
        """获取CPU温度

        :return: 摄氏度的数值
        """
        # 获取热的区域
        # res = popen(f'{self.cmd}shell ls sys/class/thermal/').read()
        # print(res)
        try:
            res = popen(f'{self.cmd}shell cat /sys/class/thermal/thermal_zone9/temp').read()
            temperature = find_all_ints_with_re(res)[0]
            if 'MI 5' in self.dbr.model:
                temperature /= 10
            return temperature
        except IndexError as err:
            print_err(err)
            sleep(1)
            return -1

    def get_app_version_info(self, package_name):
        """获取指定APP的版本信息"""
        res = popen(f'{self.cmd}shell pm dump {package_name} | findstr "versionName"').read()
        try:
            res = find_all_with_re(res, 'versionName=(.+)\n')[0]
            print(f'The version of {package_name} is {res}')
            return res
        except IndexError as err:
            print_err(err)
            return '0.0.0'

    def get_app_list(self):
        """获取已安装应用的列表"""
        res = popen(f'{self.cmd}shell pm list package').read()
        print(res)

    def get_data_from_clipboard(self):
        """从粘贴板获取数据

        :return: 粘贴板上最新的一条数据
        """
        system(f'{self.cmd}shell am startservice ca.zgrs.clipper/.ClipboardService')
        cmd = f'{self.cmd}shell am broadcast -a clipper.get'
        try:
            data = find_all_with_re(popen(cmd).read(), '.+data="(.+)"')[0]
        except IndexError as error:
            print(error)
            return self.get_data_from_clipboard()
        return data

    def input_text_with_b64(self, text):
        """使用Base64编码输入文本"""
        system(f'{self.cmd}shell ime set com.android.adbkeyboard/.AdbIME')
        chars_b64 = str(base64.b64encode(text.encode('utf-8')))[1:]
        cmd = f"{self.cmd}shell am broadcast -a ADB_INPUT_B64 --es msg {chars_b64}"
        print(cmd)
        system(cmd)

    def input_text(self, text):
        """输入文本

        :param text: 文本内容
        """
        system(f'{self.cmd}shell ime set com.android.adbkeyboard/.AdbIME')
        cmd = f"{self.cmd}shell am broadcast -a ADB_INPUT_TEXT --es msg '{text}'"
        print(cmd)
        system(cmd)

    def get_model(self):  # pylint: disable=inconsistent-return-statements
        """获取手机型号信息

        :return: 手机型号信息
        """
        res = popen(f'{self.cmd}shell getprop ro.product.model').read()[:-1]
        if not res:
            self.reconnect()
            self.__init__(self.dbr.serial_num)  # pylint: disable=unnecessary-dunder-call
            return
        while res[-1] == '\n':
            res = res[:-1]
        return res

    def is_awake(self):
        """判断是否亮屏"""
        displays_models = ['M2007J22C', 'Redmi K20 Pro Premium Edition']
        if self.dbr.model in displays_models:
            res = popen(f'{self.cmd}shell dumpsys window displays | findstr mAwake').read()[4:-41]
            if 'false' in res:
                res = res[:-2]
        else:
            res = popen(f'{self.cmd}shell dumpsys window policy | findstr mAwake').read()[4:-1]
        try:
            if res[-1] == '\n':
                res = res[:-1]
        except IndexError as err:
            print_err(err)
            sleep(96)
            self.keep_online()
            return self.is_awake()
        print(res)
        # print([res])
        if 'true' in res:
            return True
        return False

    def get_current_focus(self):
        """获取当前界面的Activity"""
        displays_models = ['M2007J22C', 'Redmi K20 Pro Premium Edition']
        try:
            if self.dbr.model in displays_models:
                res = popen(
                    f'{self.cmd}shell dumpsys window displays | findstr mCurrentFocus').read()[2:-1]
            else:
                res = popen(
                    f'{self.cmd}shell dumpsys window windows | findstr mCurrentFocus').read()[2:-2]
        except UnicodeDecodeError as err:
            print_err(f'{self.dbr.serial_num} {err}')
            self.reboot()
            return self.get_current_focus()
        print(res)
        # print([res])
        if res.count('mCurrentFocus=Window{') > 1:
            self.reboot()
        return res

    def press_key(self, keycode, sleep_time=1):
        """按键

        :param keycode: 按键代码
        :param sleep_time: 休息时间
        """
        print(f'正在让{self.dbr.serial_num}按{keycode}')
        system(f'{self.cmd}shell input keyevent {keycode}')
        sleep(sleep_time, True, True)

    def press_home_key(self, sleep_time=1):
        """按起始键

        :param sleep_time: 休息时间
        """
        self.keep_online()
        if not self.is_awake():
            self.press_power_key()
        self.press_key('KEYCODE_HOME', sleep_time)

    def press_app_switch_key(self):
        """按应用切换键"""
        self.press_key('KEYCODE_APP_SWITCH')

    def press_back_key(self, sleep_time=1):
        """按返回键

        :param sleep_time: 休息时间
        """
        self.keep_online()
        self.press_key('KEYCODE_BACK', sleep_time)

    def press_power_key(self):
        """按电源键"""
        self.press_key('KEYCODE_POWER')

    def press_enter_key(self):
        """按回车键"""
        self.press_key('KEYCODE_ENTER')

    def usb(self, sleep_time=2):
        """restart adbd listening on USB
        :param sleep_time: 超时
        """
        cmd = f'{self.cmd}usb'
        system(cmd)
        print(cmd)
        sleep(sleep_time)

    def tcpip(self):
        """restart adbd listening on TCP on PORT"""
        system(f'adb -s {self.dbr.id_num} tcpip 5555')
        sleep(1, False, False)

    def connect(self):
        """connect to a device via TCP/IP [default port=5555]"""
        self.tcpip()
        system(f'adb connect {self.dbr.ipv4_addr}')
        sleep(6)
        system(f'adb connect {self.dbr.ipv4_addr}')
        if self.dbr.ipv4_addr not in get_online_devices():
            self.reboot_by_id()

    def disconnect(self):
        """disconnect from given TCP/IP device [default port=5555], or all"""
        system(f'adb disconnect {self.dbr.ipv4_addr}')
        sleep(2, False, False)

    def reconnect(self):
        """重新连接掉线的设备"""
        system('adb reconnect offline')
        self.disconnect()
        self.connect()

    def keep_online(self, retry_cnt=0):
        """保持在线"""
        self.__init__(self.dbr.serial_num)  # pylint: disable=unnecessary-dunder-call
        online_devices = get_online_devices()
        if self.dbr.ipv4_addr in online_devices and self.dbr.id_num in online_devices:
            print(f'{self.dbr.serial_num}所对应的的ID:{self.dbr.id_num}与IP:'
                  f'{self.dbr.ipv4_addr}均在线，无需额外操作')
        elif self.dbr.ipv4_addr not in online_devices and self.dbr.id_num not in online_devices:
            system('adb reconnect offline')
            sleep(6)
            if self.dbr.id_num in online_devices:
                return self.keep_online()
            if retry_cnt < 6:
                print(f'keep_online retry_cnt={retry_cnt}')
                sleep(30)
                return self.keep_online(retry_cnt+1)
            EMail(self.dbr.serial_num).send_offline_error()
            print(f'{self.dbr.serial_num}所对应的的ID:{self.dbr.id_num}与IP:'
                  f'{self.dbr.ipv4_addr}均离线，系统无法自动处理修复该问题')
            input('请手动处理后按回车键以继续')
            print('正在继续向下处理')
            return self.keep_online()
        elif self.dbr.ipv4_addr not in get_online_devices():
            print(f'{self.dbr.serial_num}所对应的的IP:{self.dbr.ipv4_addr}离线，但ID:'
                  f'{self.dbr.id_num}在线，正在尝试自动修复该问题')
            # pylint: disable=unnecessary-dunder-call
            self.__init__(self.dbr.serial_num)
        elif self.dbr.id_num not in get_online_devices():
            print(f'{self.dbr.serial_num}所对应的的ID:{self.dbr.id_num}离线，但IP:'
                  f'{self.dbr.ipv4_addr}在线，正在尝试自动修复该问题')
            self.reboot()
        return True

    def open_app(self, activity):
        """打开APP

        param activity: 活动名
        """
        self.press_home_key()
        self.start(activity)

    def start(self, activity, wait=True):
        """启动

        :param activity: 活动名
        :param wait: 是否等待
        """
        cmd = 'shell am start '
        if wait:
            cmd += '-W '
        cmd = self.cmd + cmd + activity
        system(cmd)
        print(cmd)

    def swipe(self, start_coordinate, end_coordinate, duration=-1):
        """滑动
        :param start_coordinate: 起点的坐标（x1, y1）
        :param end_coordinate: 终点的坐标（x2, y2）
        :param duration: the default duration value -1 means a random integer from 2500 to 2501
        """
        x1_coordinate, y1_coordinate = start_coordinate
        x2_coordinate, y2_coordinate = end_coordinate
        if duration == -1:
            duration = randint(2500, 2501)
        cmd = f'{self.cmd}shell input swipe {x1_coordinate} {y1_coordinate} ' \
              f'{x2_coordinate} {y2_coordinate} {duration}'
        system(cmd)
        print(self.dbr.serial_num, cmd)

    def long_press(self, x_coordinate, y_coordinate, duration=-1):
        """长按
        :param x_coordinate: 点的x轴坐标值
        :param y_coordinate: 点的y轴坐标值
        :param duration: the default duration is a random integer from 1000 to 1500
        """
        if duration == -1:
            duration = randint(1000, 1500)
        self.swipe((x_coordinate, y_coordinate), (x_coordinate, y_coordinate), duration)

    def reboot_by_cmd(self, cmd):
        """通过CMD指令重启设备

        :param cmd: CMD指令
        """
        popen(cmd)
        print(f'已向设备{self.dbr.serial_num}下达重启指令')
        sleep(96)
        # pylint: disable=unnecessary-dunder-call
        self.__init__(self.dbr.serial_num)

    def reboot(self):
        """通过IP重启指定的设备"""
        if self.dbr.ipv4_addr not in get_online_devices():
            # pylint: disable=unnecessary-dunder-call
            self.__init__(self.dbr.serial_num)
        self.reboot_by_cmd(f'adb -s {self.dbr.ipv4_addr} reboot')

    def reboot_by_id(self):
        """通过ID重启指定的设备"""
        self.reboot_by_cmd(f'adb -s {self.dbr.id_num} reboot')

    def reboot_per_day(self):
        """每天重启一次设备"""
        if self.dbr.last_reboot_date is None or date.today() > self.dbr.last_reboot_date:
            print('今天还未重启过设备，正在执行重启指令')
            self.reboot()
            self.dbu.update_last_reboot_date(date.today())
        else:
            print('今天已经重启过设备，无需重复操作')

    def get_ipv4_address(self):
        """获取设备的IPv4地址"""
        res = popen(f'{self.cmd}shell ifconfig wlan0').read()
        ipv4_address = find_all_with_re(res, r'inet addr:(\d+.\d+.\d+.\d+)  Bcast:.+')
        if len(ipv4_address) == 1:
            ipv4_address = ipv4_address[0]
        return ipv4_address

    def get_ipv6_address(self):
        """获取设备的IPv6地址"""
        res = popen(f'{self.cmd}shell ifconfig wlan0').read()
        ipv6_address = find_all_with_re(res, r'inet6 addr: (.+:.+:.+)/64 Scope: Global')
        if 0 < len(ipv6_address) <= 2:
            ipv6_address = ipv6_address[0]
            print(f'设备{self.dbr}的公网IPv6地址为：{ipv6_address}')
        else:
            print(f'设备{self.dbr}的公网IPv6地址数大于2或小于0，正在尝试重新获取')
            self.reboot()
            self.get_ipv6_address()
