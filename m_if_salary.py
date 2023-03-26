"""闲鱼工资程序入口模块"""
from pacc.mysql import RetrieveIdleFishRecords, RetrieveIdleFish


class IdleFishSalary:  # pylint: disable=too-few-public-methods
    """闲鱼工资类"""

    @classmethod
    def get_base_payee_group_records(cls):
        """获取所有基层人员账号分组汇总后的信息"""
        res = RetrieveIdleFishRecords.query_base_payee_group_records()
        res_dic = {}
        for names, base_payee in res:
            res_dic.update({base_payee: str(names).split('||')})
        return res_dic

    @classmethod
    def get_middle_payee_group_records(cls):
        """获取所有中层人员账号分组汇总后的信息"""
        res_dic = {}
        res = RetrieveIdleFishRecords.query_middle_payee_group_records()
        for names, middle_payee in res:
            res_dic.update({middle_payee: str(names).split('||')})
        return res_dic

    @classmethod
    def get_payee_group_records(cls):
        """获取所有人员账号分组汇总后的信息"""
        base_payee_group_records = cls.get_base_payee_group_records()
        # print(base_payee_group_records)
        middle_payee_group_records = cls.get_middle_payee_group_records()
        # print(middle_payee_group_records)
        base_mid_dic = {}
        base_dic = {}
        middle_dic = {}
        for base_payee, job_num_li in base_payee_group_records.items():
            base_mid = set(job_num_li) & set(middle_payee_group_records.get(base_payee, []))
            if base_mid:
                base_mid_dic.update({base_payee: list(base_mid)})
        for base_payee, job_num_li in base_payee_group_records.items():
            base = set(job_num_li) - set(middle_payee_group_records.get(base_payee, []))
            if base:
                base_dic.update({base_payee: list(base)})
        for middle_payee, job_num_li in middle_payee_group_records.items():
            middle = set(job_num_li) - set(base_payee_group_records.get(middle_payee, []))
            if middle:
                middle_dic.update({middle_payee: list(middle)})
        print(base_mid_dic)
        print(base_dic)
        print(middle_dic)
        for k, v in base_mid_dic.items():
            print(k, v)


IdleFishSalary.get_payee_group_records()
# IdleFishSalary.get_middle_payee_group_records()
