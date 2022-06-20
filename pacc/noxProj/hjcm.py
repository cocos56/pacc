"""花季传媒模块"""
# pylint: disable=R0801
from datetime import datetime
from xml.parsers.expat import ExpatError

from .noxProj import NoxProj
from ..multi.thread import runThreadsWithArgsList
from ..nox import getOnlineDevices, NoxADB, NoxConsole, NoxUIAutomator
from ..tools import sleep

ROOT = 'com.lxuvwyzb/com.xmqztdo.xmqztdo.'


# pylint: disable=R0903
class Activity:
    """安卓的活动名"""
    MainActivity = ROOT + 'MainActivity'  # 程序入口（广告页）
    Launcher = 'com.android.launcher3/com.android.launcher3.launcher3.Launcher'


class HJCM(NoxProj):
    """花季传媒模块"""
    def __init__(self, start_index=0, i_code='F3GWZN', nox_work_path=r'D:\Program Files\Nox\bin',
                 nox_step=3):
        self.start_index = start_index
        self.i_code = i_code
        super().__init__(nox_work_path)
        self.nox_step = nox_step
        self.nox_num = NoxConsole.get_number()
        self.last_online_devices = []

    def do_work_when_input_i_code(self, adb_ins, uia_ins):
        """进入输入邀请码界面输入邀请码并提交

        :param adb_ins: 安卓调试桥类的实例
        :param uia_ins: UI自动化测试类的实例
        """
        uia_ins.click(contentDesc='输入邀请码')
        uia_ins.click(text='请输入邀请码')
        adb_ins.inputText(self.i_code)
        uia_ins.click(contentDesc='提交')

    def do_all_work(self, device_ip):
        """执行所有的操作步骤

        :param device_ip: 设备IP
        """
        adb_ins = NoxADB(device_ip)
        while Activity.MainActivity not in adb_ins.getCurrentFocus():
            sleep(5, False, False)
        uia_ins = NoxUIAutomator(device_ip)
        uia_ins.getCurrentUIHierarchy()
        is_confirmed = False
        has_my = False
        err_cnt = 0
        uia_ins.click(text='关闭应用')
        while not uia_ins.click(contentDesc='进入', offset_y=20, interval=3):
            uia_ins.click(contentDesc='重新检测')
            if uia_ins.click(contentDesc='确定'):
                is_confirmed = True
                break
            if uia_ins.click(contentDesc='我的'):
                has_my = True
                break
            if err_cnt >= 9:
                break
            sleep(5, False, False)
            err_cnt += 1
        err_cnt = 0
        while not uia_ins.click(contentDesc='确定'):
            if is_confirmed:
                break
            elif has_my:
                break
            elif uia_ins.click(contentDesc='我的'):
                break
            if err_cnt >= 5:
                break
            sleep(5, False, False)
            err_cnt += 1
        adb_ins.pressBackKey()
        uia_ins.tap((484, 925))  # 点击【我的】
        adb_ins.pressBackKey()  # 从【保存凭据】返回
        uia_ins.click(contentDesc='账号设置')
        self.do_work_when_input_i_code(adb_ins, uia_ins)

    def do_work(self, device_ip):
        """执行操作步骤

        :param device_ip: 设备IP
        """
        try:
            self.do_all_work(device_ip)
        except FileNotFoundError as e:
            print(e)

    def run_app(self):
        NoxConsole(self.start_index).run_app('com.lxuvwyzb')

    def launch_all_by_step(self):
        """按照步骤启动所有的"""
        print(datetime.now())
        NoxConsole.quit_all()
        for i in range(self.nox_step):
            self.start_index += 1
            self.run_app()
        sleep(45)
        online_devices = getOnlineDevices()
        err_cnt = 0
        while True:
            sleep(5, False, False)
            for i in online_devices:
                if i in self.last_online_devices:
                    continue
            if len(online_devices) == self.nox_step:
                break
            if err_cnt >= 9:
                break
            err_cnt += 1
            online_devices = getOnlineDevices()
        self.last_online_devices = online_devices
        print(online_devices)
        runThreadsWithArgsList(self.do_work, online_devices)
        for i in online_devices:
            uia_ins = NoxUIAutomator(i)
            try:
                if uia_ins.getDict(contentDesc='您绑定的邀请码为：'):
                    continue
                self.clean_uia_files()
                adb_ins = NoxADB(i)
                if uia_ins.getDict(contentDesc='您绑定的邀请码为：'):
                    continue
                elif uia_ins.getDict(text='请输入邀请码'):
                    adb_ins.pressBackKey()
                    self.do_work_when_input_i_code(adb_ins, uia_ins)
                    continue
                elif uia_ins.getDict(contentDesc='输入邀请码'):
                    self.do_work_when_input_i_code(adb_ins, uia_ins)
                    continue
                elif uia_ins.getDict(text='请输入12位激活码'):
                    adb_ins.pressBackKey()
                    uia_ins.click(contentDesc='账号设置')
                    self.do_work_when_input_i_code(adb_ins, uia_ins)
                    continue
                elif uia_ins.click(contentDesc='账号设置'):
                    self.do_work_when_input_i_code(adb_ins, uia_ins)
                    continue
                elif uia_ins.getDict(contentDesc='——·含羞草公告·——'):
                    uia_ins.click(contentDesc='确定')
                    uia_ins.tap((484, 925))  # 点击【我的】
                    adb_ins.pressBackKey()  # 从【保存凭据】返回
                    uia_ins.click(contentDesc='账号设置')
                    self.do_work_when_input_i_code(adb_ins, uia_ins)
                    continue
                elif Activity.Launcher in adb_ins.getCurrentFocus():
                    adb_ins.start(Activity.MainActivity)
                    self.do_all_work(i)
                    continue
            except (ExpatError, FileNotFoundError) as e:
                print(e)

    def mainloop(self):
        while True:
            if self.start_index >= self.nox_num:
                break
            self.launch_all_by_step()
