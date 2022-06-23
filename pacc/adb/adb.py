"""安卓调试桥模块"""
import base64
from datetime import datetime
from os import popen, system
from random import randint

from .uia import UIAutomator
from ..config import Config
from ..mysql import RetrieveBaseInfo, UpdateBaseInfo
from ..tools import findAllWithRe, sleep, EMail


def get_online_devices():
    """获取所有在线设备"""
    res = popen('adb devices').read()
    res = findAllWithRe(res, r'(.+)\tdevice')
    for i, _ in enumerate(res):
        res[i] = res[i].replace(':5555', '')
    return res


class ADB:  # pylint: disable=too-many-public-methods
    """安卓调试桥类"""
    reboot_per_hour_record = [-1]

    def __init__(self, device_sn, offline_cnt=1):
        """构造函数：初始化安卓调试桥类的对象

        :param device_sn: 设备序列号
        :param offline_cnt: 离线次数计数器
        """
        system('adb reconnect offline')
        self.device = RetrieveBaseInfo(device_sn)
        if self.device.ID not in get_online_devices():
            if not offline_cnt % 20:
                EMail(self.device.SN).sendOfflineError()
            print(self.device.SN, '不在线，该设备的ID为：', self.device.ID, '，请核对！', sep='')
            sleep(30)
            # pylint: disable=W0233
            self.__init__(device_sn, offline_cnt+1)
        self.cmd = f'adb -s {self.device.ID} '
        if not self.get_ipv4_address():
            print(self.get_ipv4_address())
            sleep(3)
            # pylint: disable=W0233
            self.__init__(device_sn)
        if not self.get_ipv4_address() == self.device.IP:
            UpdateBaseInfo(device_sn).updateIP(self.get_ipv4_address())
            self.device = RetrieveBaseInfo(device_sn)
        if not Config.debug:
            self.reconnect()
        self.cmd = f'adb -s {self.device.IP} '
        self.uia = UIAutomator(device_sn)
        if not self.get_model() == self.device.Model:
            UpdateBaseInfo(device_sn).updateModel(self.get_model())
            self.device = RetrieveBaseInfo(device_sn)
        if 'com.android.settings/com.android.settings.Settings$UsbDetailsActivity' in \
                self.get_current_focus():
            if self.device.Model in ['M2007J22C', 'Redmi K20 Pro Premium Edition']:
                self.press_back_key(6)

    def get_data_from_clipboard(self):
        """从粘贴板获取数据"""
        system(self.cmd + 'shell am startservice ca.zgrs.clipper/.ClipboardService')
        cmd = self.cmd + 'shell am broadcast -a clipper.get'
        try:
            data = findAllWithRe(popen(cmd).read(), '.+data="(.+)"')[0]
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

    def get_model(self):  # pylint: disable=R1710
        """获取手机型号信息

        :return:手机型号信息
        """
        res = popen(f'{self.cmd}shell getprop ro.product.model').read()[:-1]
        if not res:
            self.reconnect()
            # pylint: disable=unnecessary-dunder-call
            self.__init__(self.device.SN)
            return
        while res[-1] == '\n':
            res = res[:-1]
        return res

    def get_current_focus(self):
        """获取当前界面的Activity"""
        res = popen(self.cmd + 'shell dumpsys window | findstr mCurrentFocus').read()[2:-2]
        print(res)
        if res.count('mCurrentFocus=Window{') > 1:
            self.reboot()
        return res

    def press_key(self, keycode, sleep_time=1):
        """按键

        :param keycode: 按键代码
        :param sleep_time: 休息时间
        """
        print(f'正在让{self.device.SN}按{keycode}')
        system(f'{self.cmd}shell input keyevent {keycode}')
        sleep(sleep_time, False, False)

    def press_home_key(self):
        """按起始键"""
        self.keep_online()
        self.press_key('KEYCODE_HOME')

    def press_menu_key(self):
        """按菜单键"""
        self.press_key('KEYCODE_MENU')

    def press_back_key(self, sleep_time=1):
        """按返回键

        :param sleep_time: 休息时间
        """
        self.press_key('KEYCODE_BACK', sleep_time)

    def press_power_key(self):
        """按电源键"""
        self.press_key('KEYCODE_POWER')

    def press_enter_key(self):
        """按回车键"""
        self.press_key('KEYCODE_ENTER')

    def usb(self, timeout=2):
        """restart adbd listening on USB

        :param timeout: 超时
        """
        cmd = self.cmd + 'usb'
        system(cmd)
        print(cmd)
        sleep(timeout)

    def tcpip(self):
        """restart adbd listening on TCP on PORT"""
        system(f'adb -s {self.device.ID} tcpip 5555')
        sleep(1, False, False)

    def connect(self):
        """connect to a device via TCP/IP [default port=5555]"""
        self.tcpip()
        system(f'adb connect {self.device.IP}')
        sleep(6)
        system(f'adb connect {self.device.IP}')
        if self.device.IP not in get_online_devices():
            self.reboot_by_id()

    def disconnect(self):
        """disconnect from given TCP/IP device [default port=5555], or all"""
        system(f'adb disconnect {self.device.IP}')
        sleep(2, False, False)

    def reconnect(self):
        """重新连接掉线的设备"""
        system('adb reconnect offline')
        self.disconnect()
        self.connect()

    def keep_online(self):
        """保持在线"""
        if self.device.IP not in get_online_devices():
            # pylint: disable=unnecessary-dunder-call
            self.__init__(self.device.SN)

    def taps(self, instructions):
        """点击

        :param instructions: 指令集
        """
        for x_coordinate, y_coordinate, interval, tip in instructions:
            print(tip)
            self.uia.tap([x_coordinate, y_coordinate], interval)

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

    # pylint: disable=too-many-arguments
    def swipe(self, x1_coordinate, y1_coordinate, x2_coordinate, y2_coordinate, duration=-1):
        """滑动

        :param x1_coordinate: 起点的x轴坐标值
        :param y1_coordinate: 起点的y轴坐标值
        :param x2_coordinate: 终点的x轴坐标值
        :param y2_coordinate: 终点的y轴坐标值
        :param duration: the default duration is a random integer from 500 to 600
        """
        if duration == -1:
            duration = randint(500, 600)
        cmd = f'{self.cmd}shell input swipe {x1_coordinate} {y1_coordinate} ' \
              f'{x2_coordinate} {y2_coordinate} {duration}'
        system(cmd)
        print(self.device.SN, cmd)

    def long_press(self, x_coordinate, y_coordinate, duration=-1):
        """长按

        :param x_coordinate: 点的x轴坐标值
        :param y_coordinate: 点的y轴坐标值
        :param duration: the default duration is a random integer from 1000 to 1500
        """
        if duration == -1:
            duration = randint(1000, 1500)
        self.swipe(x_coordinate, y_coordinate, x_coordinate, y_coordinate, duration)

    def reboot(self):
        """重启设备"""
        self.reboot_by_ip()

    def reboot_by_cmd(self, cmd):
        """通过CMD指令重启设备

        :param cmd: CMD指令
        """
        popen(cmd)
        print(f'已向设备{self.device.SN}下达重启指令')
        sleep(69)
        # pylint: disable=unnecessary-dunder-call
        self.__init__(self.device.SN)

    def reboot_by_id(self):
        """通过ID重启指定的设备"""
        self.reboot_by_cmd(f'adb -s {self.device.ID} reboot')

    def reboot_by_ip(self):
        """通过IP重启指定的设备"""
        if self.device.IP not in get_online_devices():
            # pylint: disable=unnecessary-dunder-call
            self.__init__(self.device.SN)
        self.reboot_by_cmd(f'adb -s {self.device.IP} reboot')

    def reboot_per_hour(self, tip='小时'):
        """每小时重启一次设备

        :param tip: 该函数可能每天重启一次设备被复用，相应的tip值也应该改变
        """
        if not datetime.now().hour == self.reboot_per_hour_record[0]:
            self.reboot_per_hour_record = [datetime.now().hour]
        if self.device.SN not in self.reboot_per_hour_record:
            print(f'按每{tip}重启一次的计划重启{self.device.SN}')
            self.reboot()
            self.reboot_per_hour_record.append(self.device.SN)
            return True
        return False

    def reboot_per_day(self, hours=tuple([0])):
        """每天固定点重启一次设备

        :param hours: 重启的时
        """
        if datetime.now().hour in hours:
            self.reboot_per_hour(tip='天')
            return True
        return False

    def get_ipv4_address(self):
        """获取设备的IPv4地址"""
        res = popen(f'{self.cmd}shell ifconfig wlan0').read()
        ipv4_address = findAllWithRe(res, r'inet addr:(\d+.\d+.\d+.\d+)  Bcast:.+')
        if len(ipv4_address) == 1:
            ipv4_address = ipv4_address[0]
        return ipv4_address

    def get_ipv6_address(self):
        """获取设备的IPv6地址"""
        res = popen(f'{self.cmd}shell ifconfig wlan0').read()
        ipv6_address = findAllWithRe(res, r'inet6 addr: (.+:.+:.+)/64 Scope: Global')
        if 0 < len(ipv6_address) <= 2:
            ipv6_address = ipv6_address[0]
            print(f'设备{self.device}的公网IPv6地址为：{ipv6_address}')
        else:
            print(f'设备{self.device}的公网IPv6地址数大于2或小于0，正在尝试重新获取')
            self.reboot()
            self.get_ipv6_address()
