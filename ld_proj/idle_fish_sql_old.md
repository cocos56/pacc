# 1. 查询币值总和
## 1.1. 某一个代理的
SELECT SUM(coins) FROM idle_fish WHERE role LIKE '宗毛毛%'
## 1.2. 某一个代理需要回收的
SELECT SUM(coins) FROM idle_fish WHERE role LIKE '宗毛毛%' and coins >= 30000
## 1.3. 某一代理今天回收的
SELECT SUM(last_buy_coins) FROM idle_fish WHERE role LIKE '颜瑞捷%' and last_confirm_date = CURDATE()

# 2. 查询薅羊毛赚话费的任务情况
SET @Host_Name='%';
SELECT Job_N, role, `hosts`, top_up_mobile, user_name, top_up_mobile_cnt, last_top_up_mobile_date FROM idle_fish WHERE top_up_mobile=1 and `hosts` LIKE @Host_Name ORDER BY last_top_up_mobile_date, `hosts`

# 3. 查询所有以xy开头的账号
SELECT * FROM `idle_fish` WHERE user_name LIKE 'xy%'

# 4. 查询需要进行回收操作的账号信息
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE buy=1

# 5. 查询需要回收的账号信息
## 5.1. 某一代理的
SELECT role, user_name , coins FROM idle_fish WHERE role LIKE '宗毛毛%' and coins >= 30000 ORDER BY coins desc
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, coins, buy FROM idle_fish WHERE role LIKE '吴尧河%' and coins >= 30000 and `hosts` LIKE 'C4:%'
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, coins, buy, last_buy_coins, confirm FROM idle_fish WHERE role LIKE '陈嘉乐%' and coins >= 20000 and `hosts` LIKE 'C4:%'
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, coins, buy, last_buy_coins, last_buy_date, confirm FROM idle_fish WHERE role LIKE '贾传杰%' and coins >= 20000 and `hosts` LIKE 'C4:%'
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE 'AAB%' and coins >= 20000 and `hosts` LIKE 'C5:%'
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE 'AAA%' and coins >= 20000 and `hosts` LIKE 'C5:%'
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE 'ABA%' and coins >= 20000 and `hosts` LIKE 'C5:%'

# 6. 查询已购买的账号信息

SELECT Job_N, role, `hosts`, version, user_name, pay_pw, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE 'AAB%' and last_buy_date='2023-01-26' and `hosts` LIKE 'C5:%'

# 7. 今日已确认收货的
SELECT Job_N, role, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE()
SELECT Job_N, role, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE() AND role LIKE '颜瑞捷%'
SELECT Job_N, role, user_name, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE() AND role LIKE '陈嘉乐%';
