"""MySQL数据库模块"""
from os import getenv

from pymysql import connect, OperationalError, ProgrammingError

from ..base import sleep, print_err


def get_connection(database='mobile'):
    """获取数据库的连接

    :param database: 数据库名
    :return: 数据库的连接
    """
    try:
        return connect(host=getenv('MySQL_Host'), port=3306, database=database, user='root',
                       password=getenv('MySQL_PW'))
    except OperationalError as err:
        print_err(err)
        sleep(60)
        return get_connection(database)


class MySQL:
    """MySQL数据库类"""
    conn = get_connection()
    cs = conn.cursor()

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
        self.database = database
        try:
            self.__class__.conn = connect(host=host, port=port, database=database, user=user,
                                          password=password, charset=charset)
        except OperationalError as error:
            print(f'database={database}')
            print_err(f'{self.__class__} {error}')
            sleep(30)
            # pylint: disable=non-parent-init-called
            self.__init__(host=host, port=port, database=database, user=user, password=password,
                          charset=charset)
            return
        self.__class__.cs = self.__class__.conn.cursor()
        print(f'已成功与{database}数据库建立连接')
        self.__class__.instance = self

    def __del__(self):
        """析构函数"""
        print(f'已成功与{self.database}数据库断开连接')
        # self.__class__.cs.close()

    @classmethod
    def query(cls, cmd):
        """查询函数：执行查询语句

        :param cmd: 待执行的查询语句
        """
        try:
            cls.cs.execute(cmd)
            res = cls.cs.fetchall()
        except (OperationalError, ProgrammingError) as error:
            print_err(f'{cls} query {error}')
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

    # pylint: disable=too-many-arguments
    def __init__(self, host=getenv('MySQL_Host'), port=3306, database='account', user='root',
                 password=getenv('MySQL_PW'), charset='utf8'):
        """构造函数"""
        super().__init__(host=host, port=port, database=database, user=user,
                         password=password, charset=charset)


Account()


class Record(MySQL):
    """MySQL中名为record的数据库，该数据库用于存储记录相关的信息"""

    # pylint: disable=too-many-arguments
    def __init__(self, host=getenv('MySQL_Host'), port=3306, database='record', user='root',
                 password=getenv('MySQL_PW'), charset='utf8'):
        """构造函数：初始化增类的对象

        :param host: 主机，默认从Windows系统变量中获取
        :param port: 端口号，默认访问3306端口
        :param database: 数据库名，默认读取record数据库
        :param user: 用户名，默认以root用户访问数据库
        :param password: 用户密码，默认从Windows系统变量中获取
        :param charset: 编码，默认使用utf8
        """
        super().__init__(host=host, port=port, database=database, user=user,
                         password=password, charset=charset)


Record()
