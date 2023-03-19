"""闲鱼工资程序入口模块"""
from pacc.mysql import RetrieveIdleFishRecords


class IdleFishSalary:  # pylint: disable=too-few-public-methods
    """闲鱼工资类"""

    @classmethod
    def get_group_records(cls):
        """获取分组汇总后的信息"""
        RetrieveIdleFishRecords.query_group_records()


IdleFishSalary.get_group_records()
