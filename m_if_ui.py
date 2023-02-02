"""闲鱼UI程序入口模块"""
from datetime import datetime
from tkinter import Tk, Label, Text, END, Button


class IdleFishGUI:
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
        src_data = '1. Job_N=AAA011, role=徐可可1, RT=10000, user_name=tb100200, ' \
                   'login_pw=aa123bb456, pay_pw=123668, login=1\n' \
                   '2. Job_N=AAA012, role=徐可可2, RT=10000, user_name=xy100200, ' \
                   'login_pw=aa123bb456, pay_pw=123668, login=1'
        self.init_data_text.insert(1.0, src_data)
        self.result_data_text = Text(window, width=70, height=49)  # 处理结果展示
        self.result_data_text.grid(row=1, column=12, rowspan=15, columnspan=10)
        # 文本框
        self.log_data_text = Text(window, width=66, height=9)  # 日志框
        self.log_data_text.grid(row=13, column=0, columnspan=10)
        # 按钮
        self.str_trans_to_md5_button = Button(
            window, text="开始登录", bg="lightblue", width=10, command=self.src_trans_to_sql)
        self.str_trans_to_md5_button.grid(row=1, column=11)
        window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

    # 功能函数
    def src_trans_to_sql(self):
        """源数据转为数据库的插入语句"""
        src = self.init_data_text.get(1.0, END)
        print(f"src={src}")
        self.result_data_text.delete(1.0, END)
        self.result_data_text.insert(1.0, src)
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
