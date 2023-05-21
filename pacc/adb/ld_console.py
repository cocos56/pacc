"""雷电模拟器控制台模块"""
from os import popen, system, path, remove
from datetime import date
import subprocess

from ..base import sleep, print_err
from ..config import LDC, Config
from ..mysql import RetrieveIdleFish, UpdateIdleFish


class LDConsole:
    """雷电模拟器控制台类"""

    def __init__(self, ld_index):
        """构造函数：初始化雷电模拟器控制台类的对象

        :param ld_index: 雷电模拟器的索引
        """
        self.ld_index = ld_index

    @classmethod
    def quit_all(cls):
        """关闭所有雷电模拟器"""
        system(f'{LDC}quitall')
        sleep(6)

    @classmethod
    def list(cls):
        """获取所有虚拟机的列表

        :return: 字典，键是索引值，值是虚拟机名
        """
        cmd = f'{LDC}list2'
        # print(cmd)
        try:
            res = popen(cmd).read()[:-1]
        except UnicodeDecodeError as err:
            print_err(err)
            return cls.list()
        try:
            res = [(int(i[0]), i[1]) for i in [i.split(',')[:2] for i in res.split()]]
        except IndexError as err:
            print_err(err)
            return cls.list()
        # print(res, len(res))
        try:
            last_item = res[-1]
        except IndexError as err:
            print_err(err)
            return cls.list()
        # print(last_item[0], type(last_item[0]), last_item[1], type(last_item[1]))
        if last_item[0] == 99999 and last_item[1] == '电脑桌面':
            res = res[:-1]
            # print(True)
        dic = dict(res)
        # print(dic)
        return dic

    @classmethod
    def get_last_device_num(cls):
        """获取按编号排序时最后一个设备的索引值"""
        return sorted(list(cls.list().keys()))[-1]

    def backup(self, dir_path):
        """备份设备

        :param dir_path: 备份文件夹的目录
        :return: 目标设备不存在或正在运行或今日已备份返回False，正常备份完毕返回True
        """
        if not self.is_exist():
            print(f'目标设备{self.ld_index}不存在，无法备份')
            return False
        if self.is_running(self.ld_index):
            print(f'目标设备{self.ld_index}正在运行，无法备份')
            return False
        filepath = f'{dir_path}/{self.get_name()}.ldbk'
        today = date.today()
        job_number = self.get_job_number()
        if RetrieveIdleFish(job_number).last_check_date != today:
            print(f'目标设备{self.ld_index}今天还未检查，无需进行备份工作')
            return False
        if RetrieveIdleFish(job_number).last_bak_date == today:
            print(f'目标设备{self.ld_index}今天已备份，无需重复备份工作')
            return False
        if RetrieveIdleFish(job_number).buy:
            print(f'目标设备{self.ld_index}还未完成购买工作，暂时无法进行备份工作')
            return False
        if path.exists(filepath):
            remove(filepath)
        cmd = f'{LDC}backup --index {self.ld_index} --file {filepath}'
        print(cmd)
        print(f'正在执行对设备{self.ld_index}的备份工作')
        system(cmd)
        print(f'已完成对设备{self.ld_index}的备份工作')
        UpdateIdleFish(job_number).update_last_bak_date(today)
        return True

    def is_exist(self):
        """判断虚拟机是否存在

        :return: 布尔值，存在返回True，否则返回False
        """
        return self.ld_index in self.list()

    def get_name(self):
        """获取设备的名字"""
        return self.list().get(self.ld_index)

    def get_job_number(self):
        """获取设备的工号"""
        try:
            return self.get_name()[:6]
        except TypeError as err:
            print_err(err)
            return self.get_job_number()

    def launch(self):
        """启动某一指定的雷电模拟器"""
        cmd = f'{LDC}launch --index {self.ld_index}'
        # print(cmd)
        popen(cmd)
        print(f'正在启动设备{self.ld_index}')
        sleep(5, False, False)

    @classmethod
    def quit(cls, ld_index, print_flag=False):
        """关闭某一指定的雷电模拟器

        :param ld_index: 待关闭雷电模拟器的索引值
        :param print_flag: 是否打印正常退出的信息
        """
        if cls.is_running(ld_index):
            print(f'正在退出设备{ld_index}')
            system(f'{LDC}quit --index {ld_index}')
            print_flag = True
        if cls.is_running(ld_index):
            print(f'检测到设备{ld_index}未正常退出，正在重复执行退出操作')
            return cls.quit(ld_index, print_flag=True)
        if print_flag:
            print(f'设备{ld_index}已正常退出')
        return True

    @classmethod
    def is_running(cls, ld_index):
        """判断某一指定的雷电模拟器是否正在运行

        :param ld_index: 待关闭雷电模拟器的索引值
        """
        cmd = f'{LDC}isrunning --index {ld_index}'
        # print(cmd)
        res = popen(cmd).read()
        # print(f'{ld_index} is {res}')
        return res == 'running'

    def run_app(self, package_name, app_name):
        """启动雷电模拟器并自动打开某一指定的应用

        :param package_name: 待自动打开应用的包名
        :param app_name: 应用名
        """
        cmd = f'{LDC}launchex --index {self.ld_index} --packagename {package_name}'
        # print(cmd)
        popen(cmd)
        print(f'正在启动设备{self.ld_index}并开启应用{app_name}')
        if Config.set_priority:
            sleep(1, False, False)
            cmd = 'wmic process where name="Ld9BoxHeadless.exe" call SetPriority 256'
            print(cmd)
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            sleep(2, False, False)
        else:
            sleep(5, False, False)

    @classmethod
    def copy(cls, name):
        """复制雷电模拟器设备

        :param name: 设备名
        """
        print(f'正在复制设备{name}')
        cmd = f'{LDC}copy --name {name} --from 0'
        print(cmd)
        system(cmd)
        print(f'设备{name}已完成复制')
