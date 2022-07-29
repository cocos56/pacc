from datetime import datetime
from os import popen

from ..tools import sleep, system


class NoxConsole:

    @classmethod
    def get_number(cls): return popen('NoxConsole.exe list"').read().count('\n') - 1

    @classmethod
    def remove_all(cls): cls.remove(cls.get_number())

    @classmethod
    def remove(cls, stopIndex):
        if stopIndex < 1:
            return
        for i in range(1, stopIndex+1):
            system('NoxConsole.exe remove -index:%d' % i)

    @classmethod
    def copy(cls, num, nox_name='HXC'):
        nox_num = cls.get_number()
        num = num - num % 3
        if num <= nox_num:
            return
        start_time = datetime.now()
        for i in range(nox_num + 1, num+1):
            i_time = datetime.now()
            print('正在复制第%04d/%04d个' % (i, num))
            system('NoxConsole.exe copy -name:%s%04d -from:%s' % (nox_name, i, nox_name), False)
            end_time = datetime.now()
            print(f'复制已完成，本次用时{end_time-i_time}，总用时{end_time-start_time}，'
                  f'预计还需{(end_time-start_time)/i*(num-i)}\n')

    @classmethod
    def quit_all(cls):
        system('NoxConsole.exe quitall')
        sleep(13)
        if popen('tasklist | findstr "Nox.exe"').read():
            system('taskkill /IM Nox.exe')
            sleep(15)

    def __init__(self, noxIndex):
        self.noxIndex = noxIndex

    def run_app(self, packagename):
        cmd = 'NoxConsole.exe runapp -index:%d -packagename:%s' % (self.noxIndex, packagename)
        print(cmd)
        popen(cmd)
        sleep(5, False, False)
