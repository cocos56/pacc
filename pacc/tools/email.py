"""发送邮件模块"""
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.utils import formataddr
from smtplib import SMTPDataError

from ..base import sleep, print_err
from ..mysql import RetrieveEmail

user = 'coco10069@qq.com'
password = RetrieveEmail(user).auth_code
receiver = 'zj175@139.com'


class EMail:
    """发送邮件类"""
    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备编号
        """
        self.serial_num = serial_num

    def send_email(self, error):
        """发送邮件

        :param error: 错误信息
        """
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器及端口
        server.login(user, password)  # 括号中对应的是发件人邮箱账号、邮箱密码
        msg = MIMEText(f'感知到{self.serial_num}于{datetime.now()}{error}', 'plain', 'utf-8')
        msg['From'] = formataddr((f"{error}感知中枢", user))  # 括号里的参数分别对应发件人昵称和账号
        msg['To'] = formataddr(("Coco56", receiver))  # 括号里的参数分别对应收件人昵称和账号
        msg['Subject'] = f"{self.serial_num}{error}，请处理"  # 邮件的主题，也可以说是标题
        print(f'正在发送{self.serial_num}的{error}感知邮件')
        try:
            # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.sendmail(user, [receiver, ], msg.as_string())
        except SMTPDataError as err:
            print_err(err)
        server.quit()  # 关闭连接
        sleep(30)

    def send_offline_error(self):
        """发送掉线提醒"""
        self.send_email('已掉线')

    def send_verification_code_alarm(self):
        """发送出现验证码提醒"""
        self.send_email('出现验证码')

    def send_login_alarm(self):
        """发送出现登录界面提醒"""
        self.send_email('出现登录界面')
