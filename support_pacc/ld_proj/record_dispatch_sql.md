# 1. 查询无支付密码的账号确认收货的明细

## 1.1. 今日所有汇总
SELECT dispatch_date, Job_N, role, user_name, if_mn, buy_coins, dispatch_consignee,confirm_date, base_payee, middle_payee  FROM `record_dispatch` WHERE pay_pw='AAAAAA' and confirm_date=CURDATE() ORDER BY Job_N

## 1.2. 今日某代理汇总信息

SELECT dispatch_date, Job_N, role, user_name, if_mn, buy_coins, dispatch_consignee,confirm_date, base_payee, middle_payee  FROM `record_dispatch` WHERE pay_pw='AAAAAA' and confirm_date=CURDATE() and Job_N LIKE 'ZLJ%' ORDER BY buy_coins desc;
SELECT COUNT(Job_N), SUM(buy_coins), SUM(buy_coins)*3  FROM `record_dispatch` WHERE pay_pw='AAAAAA' and confirm_date=CURDATE() and Job_N LIKE 'ZLJ%';

## 1.3. 今日和昨日
SELECT dispatch_date, Job_N, role, user_name, if_mn, buy_coins, dispatch_consignee,confirm_date, base_payee, middle_payee  FROM `record_dispatch` WHERE pay_pw='AAAAAA' and confirm_date<=CURDATE() and confirm_date>=DATE_SUB(CURDATE(),INTERVAL 1 DAY) ORDER BY Job_N

SELECT * FROM `record_dispatch` WHERE pay_pw='AAAAAA' ORDER BY confirm_date, confirm_time

# 2. 按日期归类查询无支付密码的账号确认收货的汇总信息

## 2.1. 截止至今日
SELECT confirm_date AS 确认日期 , MIN(confirm_time) AS 最早时间, MAX(confirm_time) AS 最晚时间, count(Job_N) AS 数量, FORMAT(sum(buy_coins)/10000,0) AS 币值, FORMAT(sum(buy_coins)*0.0002,2) AS 价值 FROM `record_dispatch` WHERE pay_pw='AAAAAA' and confirm_date>=CURDATE() GROUP BY confirm_date ORDER BY confirm_date DESC;
SELECT dispatch_date, Job_N, role, user_name, if_mn, buy_coins, dispatch_consignee,confirm_date, confirm_time, base_payee, middle_payee  FROM `record_dispatch` WHERE pay_pw='AAAAAA' and confirm_date=CURDATE() ORDER BY confirm_time DESC

## 2.2. 截止至昨日
SELECT confirm_date, MIN(confirm_time), MAX(confirm_time), count(Job_N), sum(buy_coins) FROM `record_dispatch` WHERE pay_pw='AAAAAA' and confirm_date>=DATE_SUB(CURDATE(),INTERVAL 1 DAY) GROUP BY confirm_date ORDER BY confirm_date DESC

# 3. 查询某一账号的确认收货明细

SELECT * FROM record_dispatch WHERE user_name='15977128176' ORDER BY dispatch_date DESC
