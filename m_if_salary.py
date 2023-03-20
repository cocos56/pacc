"""闲鱼工资程序入口模块"""
from pacc.mysql import RetrieveIdleFishRecords


class IdleFishSalary:  # pylint: disable=too-few-public-methods
    """闲鱼工资类"""

    @classmethod
    def get_base_payee_group_records(cls):
        """获取分组汇总后的信息"""
        res = RetrieveIdleFishRecords.query_base_payee_group_records()
        for names, coins_sum, last_confirm_date, money, base_payee in res:
            print(f'names={names}, coins_sum={coins_sum}, money={money}, '
                  f'last_confirm_date={last_confirm_date}, base_payee={base_payee}')


IdleFishSalary.get_base_payee_group_records()
