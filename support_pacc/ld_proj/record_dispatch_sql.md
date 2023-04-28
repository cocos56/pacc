# 1. 查询无支付密码的账号确认收货的明细

## 日期段
SELECT dispatch_date, Job_N, role, user_name, if_mn, buy_coins, dispatch_consignee,confirm_date, base_payee, middle_payee  FROM `record_dispatch` WHERE pay_pw='AAAAAA' and confirm_date<=CURDATE() and confirm_date>=DATE_SUB(CURDATE(),INTERVAL 1 DAY) ORDER BY Job_N

## 单日期
SELECT dispatch_date, Job_N, role, user_name, if_mn, buy_coins, dispatch_consignee,confirm_date, base_payee, middle_payee  FROM `record_dispatch` WHERE pay_pw='AAAAAA' and confirm_date='2023-04-25' ORDER BY Job_N

SELECT * FROM `record_dispatch` WHERE pay_pw='AAAAAA' ORDER BY confirm_date, confirm_time

# 2. 按日期归类查询无支付密码的账号确认收货的汇总信息

SELECT confirm_date, MIN(confirm_time), MAX(confirm_time), count(Job_N), sum(buy_coins) FROM `record_dispatch` WHERE pay_pw='AAAAAA' and confirm_date>=DATE_SUB(CURDATE(),INTERVAL 1 DAY) GROUP BY confirm_date ORDER BY confirm_date DESC

# 3. 查询某一账号的确认收货明细

SELECT * FROM record_dispatch WHERE user_name='15977128176' ORDER BY dispatch_date DESC
