# 1. 查询币值总和
## 1.1. 所有账号的
SELECT SUM(coins) FROM `idle_fish`
## 1.2. 某一个代理的
SELECT SUM(coins) FROM idle_fish WHERE role LIKE '宗毛毛%'
## 1.3. 某一个代理需要回收的
SELECT SUM(coins) FROM idle_fish WHERE role LIKE '宗毛毛%' and coins >= 30000
## 1.4. 某一代理今天回收的
SELECT SUM(last_buy_coins) FROM idle_fish WHERE role LIKE '颜瑞捷%' and last_confirm_date = CURDATE()

# 2. 查询薅羊毛赚话费的任务情况

SET @Host_Name='%';
SELECT Job_N, role, `hosts`, top_up_mobile, user_name, top_up_mobile_cnt, last_top_up_mobile_date FROM idle_fish WHERE top_up_mobile=1 and `hosts` LIKE @Host_Name ORDER BY last_top_up_mobile_date, `hosts`

# 3. 查询低版本账号
## 3.1. 部署在C4机器上的
SELECT * FROM idle_fish WHERE `hosts` LIKE '%C4%' and version != '7.8.10'
## 3.2. 部署在所有机器上的
SELECT * FROM idle_fish WHERE version != '7.8.10'

# 4. 查询多主机列表的账号的信息

SELECT * FROM idle_fish WHERE `hosts` LIKE '%+%'

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

# 7. 查询所有以xy开头的账号
SELECT * FROM `idle_fish` WHERE user_name LIKE 'xy%'

# 8. 在线状态
## 8.1. 查询所有已掉线的账号
SELECT Job_N, role, `hosts`, version, coins FROM idle_fish WHERE login=1
## 8.2. 查询所有未掉线的账号
SELECT Job_N, role FROM idle_fish WHERE login IS NULL

# 9. 今日已确认收货的

SELECT Job_N, role, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE()

SELECT Job_N, role, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE() AND role LIKE '颜瑞捷%'

SELECT Job_N, role, user_name, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE() AND role LIKE '陈嘉乐%';

# 10. 查询所有账号的基础信息
## 10.1. 某一代理的
SELECT Job_N, role, version, coins, user_name, login_pw, pay_pw, if_mn, `淘宝号` FROM `idle_fish` WHERE Job_N LIKE 'ZLJ%'

SELECT Job_N, role, version, coins, user_name, login_pw, pay_pw, if_mn, `淘宝号` FROM `idle_fish` WHERE Job_N LIKE 'ZDR%'

# 11. 查询需要进行首次回收的账号

## 11.1. C7

SET @coins=10000, @HostsName='C7%', @Job_N='%';
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE RT= 10000 and coins >= 10000 and `hosts` LIKE @HostsName AND Job_N LIKE @Job_N;
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE RT= 10000 and coins >= 10000 and `hosts` LIKE @HostsName ORDER BY `hosts`;
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and confirm=1 and `hosts` LIKE @HostsName ORDER BY `hosts`;
SELECT Job_N, role, user_name, last_buy_coins, FORMAT(last_buy_coins*0.00033,2) as money, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE() AND `hosts` LIKE @HostsName AND Job_N LIKE @Job_N;
SELECT FORMAT(SUM(last_buy_coins)*0.0001,2) as coins, FORMAT(SUM(last_buy_coins)*0.00033,2) as money FROM idle_fish WHERE `hosts` LIKE @HostsName and last_confirm_date = CURDATE() AND Job_N LIKE @Job_N;

# 12. 混合查询

1. 查询大于目标币值的账号信息（工号排序）
2. 查询大于目标币值的账号信息（主机列表排序）
3. 查询大于目标币值的账号信息（RT值排序）

### 12.0.1. C5

SET @coins=20000, @HostsName='C5:%', @Job_N='%';
-- 结果1：查询大于目标币值的账号信息（工号排序）
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and coins >= @coins and `hosts` LIKE @HostsName;
-- 结果2：查询大于目标币值的账号信息（主机列表排序）
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and coins >= @coins and `hosts` LIKE @HostsName ORDER BY `hosts`;
-- 结果3：查询大于目标币值的账号信息（RT值排序）
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and coins >= @coins and `hosts` LIKE @HostsName ORDER BY RT;
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and confirm=1 and `hosts` LIKE @HostsName ORDER BY `hosts`;
SELECT Job_N, role, user_name, last_buy_coins, FORMAT(last_buy_coins*0.00033,2) as money, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE() AND Job_N LIKE @Job_N and `hosts` LIKE @HostsName;
SELECT FORMAT(SUM(last_buy_coins)*0.0001,2) as coins, FORMAT(SUM(last_buy_coins)*0.00033,2) as money FROM idle_fish WHERE Job_N LIKE @Job_N and last_confirm_date = CURDATE() and `hosts` LIKE @HostsName;
