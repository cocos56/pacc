"""闲鱼工资程序入口模块"""
from pacc.mysql import RetrieveIdleFishRecords


class IdleFishSalary:  # pylint: disable=too-few-public-methods
    """闲鱼工资类"""

    @classmethod
    def get_base_payee_group_records(cls):
        """获取基层人员账号分组汇总后的信息"""
        res = RetrieveIdleFishRecords.query_base_payee_group_records()
        for names, coins_sum, last_confirm_date, money, base_payee in res:
            job_num_li = str(names).split('||')
            print(f'确认收货日期：{last_confirm_date}, 基层收款人：{base_payee}, '
                  f'总币值：{coins_sum/10000}万, 总钱数：{money}元, '
                  f'总账号数：{len(job_num_li)}, 明细如下：')
            for job_num in job_num_li:
                print(job_num)
            print()


IdleFishSalary.get_base_payee_group_records()
