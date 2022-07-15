"""MySQL数据库模块"""
from os import getenv

from pymysql import connect, OperationalError

from ..multi import threadLock
from ..tools import sleep


class MySQL:
    conn = None
    cs = None

    def __init__(self, host=getenv('MySQL_Host'), port=3306, database='m', user='root',
                 password=getenv('MySQL_PW'), charset='utf8'):
        try:
            self.__class__.conn = connect(host=host, port=port, database=database, user=user,
                                          password=password, charset=charset)
        except OperationalError as error:
            print(error)
            sleep(30)
            self.__init__(host=host, port=port, database=database, user=user, password=password,
                          charset=charset)
            return
        self.__class__.cs = self.__class__.conn.cursor()

    @classmethod
    def query(cls, cmd):
        threadLock.acquire()
        try:
            cls.cs.execute(cmd)
            res = cls.cs.fetchall()
        except OperationalError as e:
            threadLock.release()
            print('query', e)
            sleep(30)
            cls()
            return cls.query(cmd)
        if len(res) == 1:
            res = res[0]
        threadLock.release()
        return res

    @classmethod
    def commit(cls):
        # 提交之前的操作，如果之前已经之执行过多次的execute，那么就都进行提交
        try:
            cls.conn.commit()
        except OperationalError as e:
            print('commit', e)
            sleep(30)
            cls()
            cls.commit()


class M(MySQL):
    def __init__(self):
        super().__init__()


M()
