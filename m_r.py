"""数据库查询程序入口模块"""
# pylint: disable=unused-import
from datetime import datetime, date, timedelta
from pacc.mysql import RetrieveKsjsb, UpdateKsjsb

print(datetime.now() - (datetime.now() - timedelta(minutes=20)) > timedelta(minutes=20))
