"""发送邮件模块"""
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.utils import formataddr
from smtplib import SMTPDataError

from .sleep import sleep


class EMail:
    """发送邮件类"""
    def __init__(self, serial_num):
        """构造函数

        :param serial_num: 设备编号
        """
        # self.user = '3039991689@qq.com'
        self.user = 'coco10069@qq.com'
        self.password = os.getenv(self.user)
        self.receiver = 'zj175@139.com'
        self.serial_num = serial_num

    def send_email(self, msg):
        """发送邮件

        :param msg: 待发送的信息
        """
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器及端口
        server.login(self.user, self.password)  # 括号中对应的是发件人邮箱账号、邮箱密码
        try:
            # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.sendmail(self.user, [self.receiver, ], msg.as_string())
        except SMTPDataError as error:
            print(error)
        server.quit()  # 关闭连接
        sleep(30)

    def send_offline_error(self):
        """发送掉线提醒"""
        msg = MIMEText(f'感知到{self.serial_num}于{datetime.now()}已掉线', 'plain', 'utf-8')
        msg['From'] = formataddr(("掉线感知中枢", self.user))  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(("Coco56", self.receiver))  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = f"{self.serial_num}已掉线，请处理"  # 邮件的主题，也可以说是标题
        print(f'正在发送{self.serial_num}的掉线感知邮件')
        self.send_email(msg)

    def send_verification_code_alarm(self):
        """发送出现验证码提醒"""
        msg = MIMEText(f'感知到{self.serial_num}于{datetime.now()}出现验证码', 'plain', 'utf-8')
        msg['From'] = formataddr(("验证码感知中枢", self.user))  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(("Coco56", self.receiver))  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = f"{self.serial_num}出现验证码，请处理"  # 邮件的主题，也可以说是标题
        print(f'正在发送{self.serial_num}的验证码感知邮件')
        self.send_email(msg)
