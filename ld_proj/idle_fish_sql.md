# 1. 查询币值总和
## 1.1. 所有账号的
SELECT SUM(coins) FROM `idle_fish`

# 2. 查询低版本账号
## 2.1. 部署在C4机器上的
SELECT * FROM idle_fish WHERE `hosts` LIKE '%C4%' and version != '7.8.10'
## 2.2. 部署在所有机器上的
SELECT * FROM idle_fish WHERE version != '7.8.10'

# 3. 查询多主机列表的账号的信息
SELECT * FROM idle_fish WHERE `hosts` LIKE '%+%'

# 4. 在线状态
## 4.1. 查询所有已掉线的账号
SELECT Job_N, role, `hosts`, version, coins FROM idle_fish WHERE login=1
## 4.2. 查询所有未掉线的账号
SELECT Job_N, role FROM idle_fish WHERE login IS NULL

# 5. 查询所有账号的基础信息
## 5.1. 某一代理的

SELECT Job_N, role, version, coins, user_name, login_pw, pay_pw, if_mn FROM `idle_fish` WHERE Job_N LIKE 'WAS%'

SELECT Job_N, role, version, coins, user_name, login_pw, pay_pw, if_mn FROM `idle_fish` WHERE Job_N LIKE 'ZDR%'

SELECT Job_N, role, version, coins, user_name, login_pw, pay_pw, if_mn FROM `idle_fish` WHERE Job_N LIKE 'WDC%'

# 6. 查询收货地址
SELECT Job_N, user_name, if_mn, last_buy_date, pay_pw, `hosts`, `收货地址` FROM idle_fish WHERE Job_N LIKE 'ZLJ%' AND pay_pw = 'AAAAAA' ORDER BY `hosts`

# 7. 查询待删除的账号

SELECT Job_N, role FROM idle_fish WHERE role like '%_待删'

# 8. 查询收款人

SELECT Job_N, role, user_name, if_mn, pay_pw, nickname, last_buy_consignee, base_payee, middle_payee FROM idle_fish;
SELECT Job_N, role, user_name, if_mn, pay_pw, nickname, last_buy_consignee, base_payee, middle_payee FROM idle_fish WHERE base_payee IS NULL or middle_payee IS NULL

# 9. 查询某主机上账号信息的汇总分析情况

SELECT Left((`hosts`), 3) AS 主机名, COUNT(1) AS 账号数, COUNT(login) AS 离线数, SUM(coins) AS 总币值, MAX(last_run_time) AS 最晚运行时间, MAX(last_check_time), MIN(last_run_date) AS 最早运行日期, MAX(last_run_date) AS 最晚运行日期 FROM `idle_fish` GROUP BY Left((`hosts`), 3) ORDER BY Left((`hosts`), 3)

# 10. 混合查询

1. 结果1：查询大于目标币值的账号信息（工号排序）
2. 结果2：查询大于目标币值的账号信息（主机列表排序）
3. 结果3：查询大于目标币值的账号信息（RT值、币值排序）
4. 结果4：查询大于目标币值的账号信息（上次回收时间排序）
5. 结果5：查询大于目标币值的账号信息（币值排序）
6. 结果6：查询今日下单进行回收鱼币操作的账号信息（回收时间排序）

-- 变量设置
SET @coins=40000, @HostsName='%', @Job_N='%', @price=0.00015, @target_date=CURDATE();
-- 结果1：查询大于目标币值的账号信息（工号排序）
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and coins >= @coins and `hosts` LIKE @HostsName;
-- 结果2：查询大于目标币值的账号信息（主机列表排序）
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and coins >= @coins and `hosts` LIKE @HostsName ORDER BY `hosts`;
-- 结果3：查询大于目标币值的账号信息（RT值、币值排序）
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and coins >= @coins and `hosts` LIKE @HostsName ORDER BY RT, coins DESC;
-- 结果4：查询大于目标币值的账号信息（上次回收时间、币值排序）
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and coins >= @coins and `hosts` LIKE @HostsName ORDER BY last_buy_date, coins DESC;
-- 结果5：查询大于目标币值的账号信息（币值排序）
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and coins >= @coins and `hosts` LIKE @HostsName ORDER BY coins DESC;
-- 结果6：查询今日下单进行回收鱼币操作的账号信息（回收时间排序）
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, last_buy_time, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and last_buy_date=@target_date and `hosts` LIKE @HostsName ORDER BY last_buy_time DESC;
-- 结果7：查询今日下单且无备注的账号信息（按照能否自动确认、加注日期、主机名排序）
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, last_buy_time, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and last_buy_date=@target_date and `hosts` LIKE @HostsName ORDER BY confirm, `加注日期`, `hosts`;
-- 结果8：查询可能存在偷卖偷用的账号信息
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, last_buy_time, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and last_buy_date<=DATE_SUB(CURDATE(),INTERVAL 20 DAY) and `hosts` LIKE @HostsName ORDER BY last_buy_date, coins;
-- 结果9：查询今日剩余需要进行自动确认收货操作的账号信息（主机名排序）
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, if_mn, coins, RT, buy, last_buy_coins, last_buy_date, confirm, 加注日期 FROM idle_fish WHERE Job_N LIKE @Job_N and confirm=1 and `hosts` LIKE @HostsName ORDER BY `hosts`;
-- 结果10：
SELECT Job_N, role, base_payee, middle_payee, user_name, last_buy_coins, FORMAT(last_buy_coins*@price,2) as money, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = @target_date AND Job_N LIKE @Job_N and `hosts` LIKE @HostsName;
-- 结果11：
SELECT Job_N, role, user_name, last_buy_coins, FORMAT(last_buy_coins*@price,2) as money, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = @target_date AND Job_N LIKE @Job_N and `hosts` LIKE @HostsName;
-- 结果12：
SELECT GROUP_CONCAT(Job_N, role), sum(last_buy_coins), FORMAT(sum(last_buy_coins)*@price,2) as money, if_mn, last_confirm_date, base_payee, middle_payee FROM `idle_fish` WHERE last_confirm_date = @target_date AND Job_N LIKE @Job_N and `hosts` LIKE @HostsName GROUP BY base_payee ORDER BY `Job_N`;
-- 结果13：
SELECT FORMAT(SUM(last_buy_coins)*0.0001,2) as coins, FORMAT(SUM(last_buy_coins)*@price,2) as money FROM idle_fish WHERE Job_N LIKE @Job_N and last_confirm_date = @target_date and `hosts` LIKE @HostsName;