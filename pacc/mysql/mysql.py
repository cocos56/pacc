"""MySQL数据库模块"""
from os import getenv

from pymysql import connect, OperationalError

from ..base import sleep
from ..multi import threadLock


class MySQL:
    """MySQL数据库类"""
    conn = connect(host=getenv('MySQL_Host'), port=3306, database='mobile', user='root',
                   password=getenv('MySQL_PW'))
    cs = conn.cursor()
    conn.close()

    instance = None

    # pylint: disable=too-many-arguments
    def __init__(self, host=getenv('MySQL_Host'), port=3306, database='mobile', user='root',
                 password=getenv('MySQL_PW'), charset='utf8'):
        """构造函数：初始化增类的对象

        :param host: 主机，默认从Windows系统变量中获取
        :param port: 端口号
        :param database: 数据库名
        :param user: 用户名
        :param password: 用户密码，默认从Windows系统变量中获取
        :param charset: 编码
        """
        try:
            self.__class__.conn = connect(host=host, port=port, database=database, user=user,
                                          password=password, charset=charset)
        except OperationalError as error:
            print(error)
            sleep(30)
            # pylint: disable=non-parent-init-called
            self.__init__(host=host, port=port, database=database, user=user, password=password,
                          charset=charset)
            return
        self.database = database
        self.__class__.cs = self.__class__.conn.cursor()
        print(f'已成功与{database}数据库建立连接')
        self.__class__.instance = self

    def __del__(self):
        print(f'已成功与{self.database}数据库断开连接')
        self.__class__.cs.close()

    @classmethod
    def query(cls, cmd):
        """查询函数：执行查询语句

        :param cmd: 待执行的查询语句
        """
        with threadLock:
            try:
                cls.cs.execute(cmd)
                res = cls.cs.fetchall()
            except OperationalError as error:
                threadLock.release()
                print('query', error)
                sleep(30)
                cls()
                return cls.query(cmd)
            if len(res) == 1:
                res = res[0]
            return res

    @classmethod
    def commit(cls):
        """提交之前的操作，如果之前已经之执行过多次的execute，那么就都进行提交"""
        try:
            cls.conn.commit()
        except OperationalError as error:
            print('commit', error)
            sleep(30)
            cls()
            cls.commit()


class Mobile(MySQL):
    """MySQL中名为mobile的数据库，该数据库用于存储手机项目相关的信息"""


Mobile()


class Account(MySQL):
    """MySQL中名为account的数据库，该数据库用于存储网络账号相关的信息"""

    def __init__(self):
        """构造函数"""
        super().__init__(database='account')


Account()
