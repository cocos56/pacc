"""闲鱼UI程序入口模块"""
from datetime import datetime
from os.path import join
from shutil import move
from tkinter import Tk, Label, Text, END, Button

from pacc.mysql import CreateIdleFish


class IdleFishGUI:  # pylint: disable=too-many-instance-attributes
    """闲鱼图形化界面类"""
    def __init__(self):
        """构造方法"""
        self.log_line_num = 0
        window = Tk()  # 实例化出一个父窗口
        # 设置根窗口默认属性
        window.title("闲鱼登录工具_v0.0")  # 窗口名
        window.geometry('1068x681+260+80')  # 1068 681为窗口大小，+10 +10 定义窗口弹出时的默认展示位
        # 标签
        self.init_data_label = Label(window, text="待登录的账号")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(window, text="登录结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(window, text="登录日志")
        self.log_label.grid(row=12, column=0)
        self.init_data_text = Text(window, width=67, height=35)  # 原始数据录入框
        self.init_data_text.grid(row=1, column=0, rowspan=10, columnspan=10)
        src_data = 'Serial_N=1, Job_N=AAA018, role=徐可可8, RT=10000, user_name=tb100200, ' \
                   'login_pw=aa123bb456, pay_pw=123668\n' \
                   'Serial_N=2, Job_N=AAA019, role=徐可可9, RT=10000, user_name=xy100200, ' \
                   'login_pw=aa123bb456, pay_pw=123668'
        self.init_data_text.insert(1.0, src_data)
        self.result_data_text = Text(window, width=70, height=49)  # 处理结果展示
        self.result_data_text.grid(row=1, column=12, rowspan=15, columnspan=10)
        # 文本框
        self.log_data_text = Text(window, width=66, height=9)  # 日志框
        self.log_data_text.grid(row=13, column=0, columnspan=10)
        # 按钮
        self.str_trans_to_md5_button = Button(
            window, text="开始登录", bg="lightblue", width=10, command=self.src_into_db)
        self.str_trans_to_md5_button.grid(row=1, column=11)
        window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

    # 功能函数
    def src_into_db(self):  # pylint: disable=too-many-locals
        """将源数据插入到数据库中"""
        src = self.init_data_text.get(1.0, END)
        dic_li = []
        for single_src in src.split('\n'):
            if not single_src:
                continue
            split_single_src = single_src.split(', ')
            self.result_data_text.insert(1.0, f'f{split_single_src}\n')
            dic = {}
            for element in split_single_src:
                ele_split = element.split('=')
                # print(element, ele_split)
                for key_v in [ele_split]:
                    if not key_v:
                        continue
                    dic.update({key_v[0]: '='.join(key_v[1:])})
                    # print('='.join(key_v[1:]))
            print(dic)
            dic_li.append(dic)
        # input()
        print(dic_li)
        for dic in dic_li:
            job_number = dic.get('Job_N')
            role = dic.get('role')
            if '%' in job_number:
                # print(job_number, role)
                jn_prefix = job_number.split('%')[0]
                # print(jn_prefix)
                suffix = 1
                job_number = f'{jn_prefix}{str(suffix).zfill(3)}'
                exist_record = CreateIdleFish.exist_record(job_number)
                # print(job_number, exist_record)
                while exist_record:
                    suffix += 1
                    job_number = f'{jn_prefix}{str(suffix).zfill(3)}'
                    exist_record = CreateIdleFish.exist_record(job_number)
                    # print(job_number, exist_record)
                role_prefix = role.split('%')[0]
                role = f'{role_prefix}{suffix}'
                # print(f'自动推导出的job_number={job_number}, role={role}, 请确认后按回车以继续')
                # input()
            # pylint: disable=too-many-boolean-expressions
            if job_number and role and dic.get('RT') and dic.get('user_name') and \
                    dic.get('login_pw') and dic.get('pay_pw'):
                CreateIdleFish(
                    job_number, role, dic.get('RT'), dic.get('user_name'), dic.get('login_pw'),
                    dic.get('pay_pw'), dic.get('avc_link'), dic.get('if_mn'))
                txt_name = f'{job_number}{role}.txt'
                print(txt_name)
                with open(txt_name, 'w+', encoding='utf-8') as file:
                    file.write(txt_name)
                move(txt_name, join(r'\\10.1.1.2\acs', txt_name))
                print()
            else:
                continue
        # self.result_data_text.delete(1.0, END)
        self.write_log_to_text("INFO:src_trans_to_sql success")

    # 日志动态打印
    def write_log_to_text(self, log_msg):
        """写日志到日志文本框中

        :param log_msg: 日志信息
        """
        log_msg = f"{str(datetime.now())} {str(log_msg)}\n"  # 换行
        if self.log_line_num <= 7:
            self.log_data_text.insert(END, log_msg)
            self.log_line_num += 1
        else:
            self.log_data_text.delete(1.0, 2.0)
            self.log_data_text.insert(END, log_msg)


IdleFishGUI()
