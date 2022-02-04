import os
import smtplib
from smtplib import SMTPDataError
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime
from .sleep import sleep


class EMail:

    def __init__(self, deviceSN):
        # self.user = '3039991689@qq.com'
        self.user = 'coco10069@qq.com'
        self.password = os.getenv(self.user)
        self.receiver = 'zj175@139.com'
        self.deviceSN = deviceSN

    def sendEmail(self, msg):
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器及端口
        server.login(self.user, self.password)  # 括号中对应的是发件人邮箱账号、邮箱密码
        try:
            server.sendmail(self.user, [self.receiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        except SMTPDataError as e:
            print(e)
        server.quit()  # 关闭连接
        sleep(30)

    def sendOfflineError(self):
        msg = MIMEText('感知到%s于%s已掉线' % (self.deviceSN, datetime.now()), 'plain', 'utf-8')
        msg['From'] = formataddr(["掉线感知中枢", self.user])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["Coco56", self.receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "%s已掉线，请处理" % self.deviceSN  # 邮件的主题，也可以说是标题
        print('正在发送' + self.deviceSN + '的掉线感知邮件')
        self.sendEmail(msg)

    def sendVerificationCodeAlarm(self):
        msg = MIMEText('感知到%s于%s出现验证码' % (self.deviceSN, datetime.now()), 'plain', 'utf-8')
        msg['From'] = formataddr(["验证码感知中枢", self.user])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["Coco56", self.receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "%s出现验证码，请处理" % self.deviceSN  # 邮件的主题，也可以说是标题
        print('正在发送' + self.deviceSN + '的验证码感知邮件')
        self.sendEmail(msg)

