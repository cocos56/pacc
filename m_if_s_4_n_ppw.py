"""针对于没有支付密码的闲鱼工资程序入口模块"""
from pacc.mysql import RetrieveDispatchRecords, RetrieveIdleFishByUsername, \
    RetrieveIdleFishByConsignee, RetrieveIdleFish, UpdateRecordDispatch


class IdleFishSalary4NoPaymentPassword:
    """针对于没有支付密码的闲鱼工资类"""

    @classmethod
    def get_no_payee_jns(cls):
        """获取没有收款人的记录"""
        records = []
        for user_name, dispatch_consignee, base_payee, middle_payee in RetrieveDispatchRecords.\
                query_no_payee_records():
            if not base_payee or not middle_payee:
                un_jn = RetrieveIdleFishByUsername(user_name).job_number
                dc_jn = RetrieveIdleFishByConsignee(dispatch_consignee).job_number
                if un_jn != dc_jn:
                    print(f'un_jn={un_jn}, dc_jn={dc_jn}')
                    print('工号信息不一致，请核对')
                    input()
                records.append(un_jn)
        return records

    @classmethod
    def update_no_payee_records(cls):
        """更新没有收款人的记录"""
        for job_number in cls.get_no_payee_jns():
            retrieve_ins = RetrieveIdleFish(job_number)
            base_payee, middle_payee = retrieve_ins.base_payee, retrieve_ins.middle_payee
            if not base_payee or not middle_payee:
                print(retrieve_ins.job_number, retrieve_ins.role, retrieve_ins.user_name,
                      base_payee, middle_payee)
                print('还未设置收款人信息，请先设置')
                input()
            update_ins = UpdateRecordDispatch(retrieve_ins.user_name)
            update_ins.update_role(retrieve_ins.role)
            update_ins.update_job_number(job_number)


IdleFishSalary4NoPaymentPassword.update_no_payee_records()
