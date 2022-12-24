"""MySQL数据库备份模块"""
from os import system
from datetime import date, datetime


# pylint: disable=too-few-public-methods
class MySQLDump:
    """MySQL数据库备份类"""
    @classmethod
    def start(cls):
        """开始进行备份"""
        databases = ['account', 'mobile']
        suffix = str(date.today()).replace('-', '_')
        for database in databases:
            print(f'正在备份数据库{database}')
            cmd = f'mysqldump --defaults-extra-file=F:/GP/mysqldump/my.cnf {database} > ' \
                  f'D:/bak/{database}_{suffix}.sql'
            print(cmd)
            start_datetime = datetime.now()
            system(cmd)
            print(f'数据库{database}备份已完成，历时{datetime.now()-start_datetime}')
