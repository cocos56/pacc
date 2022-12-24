"""MySQL数据库备份模块"""
from os import system
from datetime import date, datetime


class MySQLDump:
    """MySQL数据库备份类"""
    @classmethod
    def start(cls):
        dbs = ['account', 'mobile']
        suffix = str(date.today()).replace('-', '_')
        for db in dbs:
            print(f'正在备份数据库{db}')
            cmd = f'mysqldump --defaults-extra-file=F:/GP/mysqldump/my.cnf {db} > ' \
                  f'D:/bak/{db}_{suffix}.sql'
            print(cmd)
            start_datetime = datetime.now()
            system(cmd)
            print(f'数据库{db}备份已完成，历时{datetime.now()-start_datetime}')
