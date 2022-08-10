"""数据库查询程序入口模块"""
# pylint: disable=unused-import
from datetime import datetime
from pacc.mysql import RetrieveKsjsb, UpdateKsjsb

d = RetrieveKsjsb('003001001').test_date
print(d, isinstance(datetime.now(), type(d)))
print(d.year)
# UpdateKsjsb('003001001').update_test_date(datetime.now())
