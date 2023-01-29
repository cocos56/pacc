# 1. 查询币值总和
## 1.1. 所有账号的
SELECT SUM(coins) FROM `idle_fish`
## 1.2. 某一个代理的
SELECT SUM(coins) FROM idle_fish WHERE role LIKE '宗毛毛%'
## 1.3. 某一个代理需要回收的
SELECT SUM(coins) FROM idle_fish WHERE role LIKE '宗毛毛%' and coins >= 30000
## 1.4. 某一代理今天回收的
SELECT SUM(last_buy_coins) FROM idle_fish WHERE role LIKE '颜瑞捷%' and last_confirm_date = CURDATE()

# 2. 查询低版本账号
## 2.1. 部署在C4机器上的
SELECT * FROM idle_fish WHERE `hosts` LIKE '%C4%' and version != '7.8.10'
## 2.2. 部署在所有机器上的
SELECT * FROM idle_fish WHERE version != '7.8.10'

# 3. 查询需要回收的账号信息
## 3.1. 某一代理的

SELECT role, user_name , coins FROM idle_fish WHERE role LIKE '宗毛毛%' and coins >= 30000 ORDER BY coins desc

SELECT Job_N, role, `hosts`, version, user_name, pay_pw, coins, buy FROM idle_fish WHERE role LIKE '吴尧河%' and coins >= 30000 and `hosts` LIKE 'C4:%'

SELECT Job_N, role, `hosts`, version, user_name, pay_pw, coins, buy, last_buy_coins, confirm FROM idle_fish WHERE role LIKE '陈嘉乐%' and coins >= 20000 and `hosts` LIKE 'C4:%'

SELECT Job_N, role, `hosts`, version, user_name, pay_pw, coins, buy, last_buy_coins, last_buy_date, confirm FROM idle_fish WHERE role LIKE '贾传杰%' and coins >= 20000 and `hosts` LIKE 'C4:%'

SELECT Job_N, role, `hosts`, version, user_name, pay_pw, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE 'AAB%' and coins >= 20000 and `hosts` LIKE 'C5:%'


SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE 'AAA%' and coins >= 20000 and `hosts` LIKE 'C5:%'

SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE 'ABA%' and coins >= 20000 and `hosts` LIKE 'C5:%'

# 4. 查询已购买的账号信息

SELECT Job_N, role, `hosts`, version, user_name, pay_pw, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE 'AAB%' and last_buy_date='2023-01-26' and `hosts` LIKE 'C5:%'

# 5. 查询所有以xy开头的账号
SELECT * FROM `idle_fish` WHERE user_name LIKE 'xy%'

# 6. 在线状态
## 6.1. 查询所有已掉线的账号
SELECT Job_N, role, `hosts`, version, coins FROM idle_fish WHERE login=1
## 6.2. 查询所有未掉线的账号
SELECT Job_N, role FROM idle_fish WHERE login IS NULL

# 7. 今日已确认收货的

SELECT Job_N, role, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE()

SELECT Job_N, role, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE() AND role LIKE '颜瑞捷%'

SELECT Job_N, role, user_name, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE() AND role LIKE '陈嘉乐%';

# 8. 查询所有账号的基础信息
## 8.1. 某一代理的
SELECT Job_N, role, version, coins, user_name, login_pw, pay_pw, if_mn, `淘宝号` FROM `idle_fish` WHERE Job_N LIKE 'ZLJ%'

# 9. 混合查询
## 9.1. 某一代理今天回收的和今日已确认收货的明细

### 9.1.1. C3

#### 9.1.1.1. SYW

SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE 'SYW%' and coins >= 20000 and `hosts` LIKE 'C3:%';
SELECT Job_N, role, user_name, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE() AND Job_N LIKE 'SYW%';
SELECT FORMAT(SUM(last_buy_coins)*0.0001,2) as coins, FORMAT(SUM(last_buy_coins)*0.0003,2) as money FROM idle_fish WHERE Job_N LIKE 'SYW%' and last_confirm_date = CURDATE();

### 9.1.2. C4

#### 9.1.2.1. ZDR

SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE 'ZDR%' and coins >= 20000 and `hosts` LIKE 'C4:%';
SELECT Job_N, role, user_name, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE() AND Job_N LIKE 'ZDR%';
SELECT FORMAT(SUM(last_buy_coins)*0.0001,2) as coins, FORMAT(SUM(last_buy_coins)*0.0003,2) as money FROM idle_fish WHERE Job_N LIKE 'ZDR%' and last_confirm_date = CURDATE();

#### 9.1.2.2. ZLJ

SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE 'ZLJ%' and coins >= 20000 and `hosts` LIKE 'C4:%';
SELECT Job_N, role, user_name, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE() AND Job_N LIKE 'ZLJ%';
SELECT FORMAT(SUM(last_buy_coins)*0.0001,2) as coins, FORMAT(SUM(last_buy_coins)*0.0003,2) as money FROM idle_fish WHERE Job_N LIKE 'ZLJ%' and last_confirm_date = CURDATE();

### 9.1.3. C5

#### 9.1.3.1. ABA

SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE 'ABA%' and coins >= 20000 and `hosts` LIKE 'C5:%';
SELECT Job_N, role, user_name, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE() AND Job_N LIKE 'ABA%';
SELECT FORMAT(SUM(last_buy_coins)*0.0001,2) as coins, FORMAT(SUM(last_buy_coins)*0.0003,2) as money FROM idle_fish WHERE Job_N LIKE 'ABA%' and last_confirm_date = CURDATE();

#### 9.1.3.2. WTX

SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE 'WTX%' and coins >= 20000 and `hosts` LIKE 'C5:%';
SELECT Job_N, role, user_name, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE() AND Job_N LIKE 'WTX%';
SELECT FORMAT(SUM(last_buy_coins)*0.0001,2) as coins, FORMAT(SUM(last_buy_coins)*0.0003,2) as money FROM idle_fish WHERE Job_N LIKE 'WTX%' and last_confirm_date = CURDATE();
