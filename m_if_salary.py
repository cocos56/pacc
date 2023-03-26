"""闲鱼工资程序入口模块"""
from datetime import date

from pacc.mysql import RetrieveIdleFishRecords, RetrieveIdleFish
from pacc.tools import create_dir


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
        middle_payee_group_records = cls.get_middle_payee_group_records()
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
        res_dic = {}
        for name, job_num_li in base_mid_dic.items():
            li = []
            for job_number in job_num_li:
                retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
                dic = {'job_number': retrieve_idle_fish_ins.job_number,
                       'role': retrieve_idle_fish_ins.role,
                       'user_name': retrieve_idle_fish_ins.user_name,
                       'if_mn': retrieve_idle_fish_ins.if_mn,
                       'last_buy_coins': retrieve_idle_fish_ins.last_buy_coins,
                       'last_confirm_date': retrieve_idle_fish_ins.last_confirm_date,
                       'level': 'base_mid',
                       }
                li.append(dic)
            res_dic.update({name: li})
        for name, job_num_li in base_dic.items():
            li = []
            for job_number in job_num_li:
                retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
                dic = {'job_number': retrieve_idle_fish_ins.job_number,
                       'role': retrieve_idle_fish_ins.role,
                       'user_name': retrieve_idle_fish_ins.user_name,
                       'if_mn': retrieve_idle_fish_ins.if_mn,
                       'last_buy_coins': retrieve_idle_fish_ins.last_buy_coins,
                       'last_confirm_date': retrieve_idle_fish_ins.last_confirm_date,
                       'level': 'base',
                       }
                li.append(dic)
            if name not in res_dic:
                res_dic.update({name: li})
            else:
                res_dic.update({name: li + res_dic.get(name)})
        for name, job_num_li in middle_dic.items():
            li = []
            for job_number in job_num_li:
                retrieve_idle_fish_ins = RetrieveIdleFish(job_number)
                dic = {'job_number': retrieve_idle_fish_ins.job_number,
                       'role': retrieve_idle_fish_ins.role,
                       'user_name': retrieve_idle_fish_ins.user_name,
                       'if_mn': retrieve_idle_fish_ins.if_mn,
                       'last_buy_coins': retrieve_idle_fish_ins.last_buy_coins,
                       'last_confirm_date': retrieve_idle_fish_ins.last_confirm_date,
                       'level': 'middle',
                       }
                li.append(dic)
            if name not in res_dic:
                res_dic.update({name: li})
            else:
                res_dic.update({name: li + res_dic.get(name)})
        if None in res_dic:
            print('未指定收款人的记录如下：')
            print(res_dic.get(None))
            print('\n请对未指定收款人的记录进行处理\n')
            return False
        return res_dic

    @classmethod
    def get_payee_message(cls):
        """获取所有人员的通知消息"""
        payee_group_records = cls.get_payee_group_records()
        for name, records in payee_group_records.items():
            print(name, records)
            base_mid_coins = 0
            base_coins = 0
            middle_coins = 0
            for record in records:
                if record.get('level') == 'base_mid':
                    base_mid_coins += record.get('last_buy_coins')
                elif record.get('level') == 'middle':
                    middle_coins += record.get('last_buy_coins')
                elif record.get('level') == 'base':
                    base_coins += record.get('last_buy_coins')
            print(base_mid_coins, base_coins, middle_coins)
            dir_path = f'D:/0/computer/闲鱼挂机/结账信息/{str(date.today()).replace("-", "_")}'
            create_dir(dir_path)
            sum_money = base_mid_coins//10000*3+base_coins//10000*2+middle_coins//10000*1
            sum_info = f'收款人：{name}，总钱数：{sum_money}元'
            txt = f'{dir_path}/{name}_{sum_money}元.txt'
            if base_mid_coins != 0:
                sum_info += f'，中基层鱼币共：{base_mid_coins//10000}万（{base_mid_coins//10000*3}元）'
            if middle_coins != 0:
                sum_info += f'，中层鱼币共：{middle_coins//10000}万（{middle_coins//10000*1}元）'
            if base_coins != 0:
                sum_info += f'，基层鱼币共：{base_coins//10000}万（{base_coins//10000*2}元）'
            sum_info += '。\n\n'
            if base_mid_coins != 0:
                sum_info += '【中基层鱼币账号信息详情如下】\n'
                index = 0
                for record in records:
                    if record.get('level') == 'base_mid':
                        index += 1
                        sum_info += f'序号：{str(index).zfill(3)}，工号：{record.get("job_number")}' \
                                    f'{record.get("role")}，账号：{record.get("user_name")}' \
                                    f'，手机：{record.get("if_mn")}' \
                                    f'，鱼币：{record.get("last_buy_coins")//10000}万\n'
            if middle_coins != 0:
                if base_mid_coins != 0:
                    sum_info += '\n'
                sum_info += '【中层鱼币账号信息详情如下】\n'
                index = 0
                for record in records:
                    if record.get('level') == 'middle':
                        index += 1
                        sum_info += f'序号：{str(index).zfill(3)}，工号：{record.get("job_number")}' \
                                    f'{record.get("role")}，账号：{record.get("user_name")}' \
                                    f'，手机：{record.get("if_mn")}' \
                                    f'，鱼币：{record.get("last_buy_coins")//10000}万\n'
            if base_coins != 0:
                if base_mid_coins != 0 or middle_coins != 0:
                    sum_info += '\n'
                sum_info += '【基层鱼币账号信息详情如下】'
                index = 0
                for record in records:
                    if record.get('level') == 'base':
                        index += 1
                        sum_info += f'序号：{str(index).zfill(3)}，工号：{record.get("job_number")}' \
                                    f'{record.get("role")}，账号：{record.get("user_name")}' \
                                    f'，手机：{record.get("if_mn")}' \
                                    f'，鱼币：{record.get("last_buy_coins")//10000}万\n'
            sum_info += '\n'
            sum_info += f'收款人：{name}，总钱数：{sum_money}元，日期：{date.today()}'
            print(sum_info)
            with open(txt, 'w+') as file:
                file.write(sum_info)


IdleFishSalary.get_payee_message()
# IdleFishSalary.get_middle_payee_group_records()
