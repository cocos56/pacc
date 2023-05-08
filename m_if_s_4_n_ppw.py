"""针对于没有支付密码的闲鱼工资程序入口模块"""
from pacc.mysql import RetrieveIdleFishDispatchRecords, RetrieveIdleFishByUsername, \
    RetrieveIdleFishByConsignee


class IdleFishSalary4NoPaymentPassword:
    """针对于没有支付密码的闲鱼工资类"""

    @classmethod
    def get_no_payee_jns(cls):
        """获取没有收款人的记录"""
        records = []
        for dispatch_date, Job_N, role, user_name, dispatch_consignee, base_payee, middle_payee in \
                RetrieveIdleFishDispatchRecords.query_no_payee_records():
            print(
                dispatch_date, Job_N, role, user_name, dispatch_consignee, base_payee, middle_payee)
            if not base_payee or not middle_payee:
                un_jn = RetrieveIdleFishByUsername(user_name).job_number
                dc_jn = RetrieveIdleFishByConsignee(dispatch_consignee).job_number
                print(f'un_jn={un_jn}, dc_jn={dc_jn}')
                if un_jn != dc_jn:
                    print('工号信息不一致，请核对')
                    input()
                records.append(un_jn)
        return records

    @classmethod
    def update_no_payee_records(cls):
        """更新没有收款人的记录"""
        print(cls.get_no_payee_jns())


IdleFishSalary4NoPaymentPassword.update_no_payee_records()
