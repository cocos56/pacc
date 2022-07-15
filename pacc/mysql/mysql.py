"""MySQL数据库模块"""
from os import getenv

from pymysql import connect, OperationalError

from ..multi import threadLock
from ..tools import sleep


class Config:
    conn = None
    cs = None

    def __init__(self, host=getenv('MySQL_Host'), port=3306, database='m', user='root',
                 password=getenv('MySQL_PW'), charset='utf8'):
        try:
            Config.conn = connect(host=host, port=port, database=database,
                                  user=user, password=password, charset=charset)
        except OperationalError as error:
            print(error)
            sleep(30)
            self.__init__(host=host, port=port, database=database,
                          user=user, password=password, charset=charset)
            return
        Config.cs = Config.conn.cursor()


Config()


def query(cmd):
    threadLock.acquire()
    try:
        Config.cs.execute(cmd)
        res = Config.cs.fetchall()
    except OperationalError as e:
        threadLock.release()
        print('query', e)
        sleep(30)
        Config()
        return query(cmd)
    if len(res) == 1:
        res = res[0]
    threadLock.release()
    return res


def commit():
    # 提交之前的操作，如果之前已经之执行过多次的execute，那么就都进行提交
    try:
        Config.conn.commit()
    except OperationalError as e:
        print('commit', e)
        sleep(30)
        Config()
        commit()
