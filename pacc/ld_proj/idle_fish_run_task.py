"""闲鱼全自动刷闲鱼币之全自动做任务中央监控系统模块"""
# pylint: disable=duplicate-code
from datetime import date, datetime, timedelta
from xml.parsers.expat import ExpatError

from .idle_fish_base import IdleFishBase
from ..adb import LDConsole, LDUIA
from ..base import sleep, print_err
from ..mysql import RetrieveIdleFish, UpdateIdleFish


class IdleFishRunTask(IdleFishBase):
    """闲鱼类"""

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

    # pylint: disable=too-many-branches, too-many-statements
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
