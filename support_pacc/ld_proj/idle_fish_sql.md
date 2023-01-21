# 1. 查询币值总和
## 1.1. 所有账号的
SELECT SUM(coins) FROM `idle_fish`
## 1.2. 某一个代理的
SELECT SUM(coins) FROM idle_fish WHERE role LIKE '宗毛毛%'
## 1.3. 某一个代理需要回收的
SELECT SUM(coins) FROM idle_fish WHERE role LIKE '宗毛毛%' and coins >= 30000

# 2. 查询低版本账号
## 2.1. 部署在C4机器上的
SELECT * FROM idle_fish WHERE `hosts` LIKE '%C4%' and version != '7.8.10'
## 2.2. 部署在所有机器上的
SELECT * FROM idle_fish WHERE version != '7.8.10'

# 3. 查询需要回收的账号信息
## 3.1. 某一代理的
SELECT role, user_name , coins FROM idle_fish WHERE role LIKE '宗毛毛%' and coins >= 30000 ORDER BY coins desc
SELECT Job_N, role, `hosts`, version, user_name, pay_pw, coins, buy FROM idle_fish WHERE role LIKE '吴尧河%' and coins >= 30000 and `hosts` LIKE 'C4:%'

# 4. 查询所有以xy开头的账号
SELECT * FROM `idle_fish` WHERE user_name LIKE 'xy%'

# 5. 在线状态
## 5.1. 查询所有已掉线的账号
SELECT Job_N, role, `hosts`, version, coins FROM idle_fish WHERE login=1
## 5.2. 查询所有未掉线的账号
SELECT Job_N, role FROM idle_fish WHERE login IS NULL

# 6. 已确认收货的
SELECT Job_N, role, last_buy_coins, if_mn, last_confirm_date FROM `idle_fish` WHERE last_confirm_date = CURDATE()

# 7. 查询所有账号的基础信息
## 7.1. 某一代理的
SELECT Job_N, role, version, coins, user_name, login_pw, pay_pw, if_mn, `淘宝号` FROM `idle_fish` WHERE Job_N LIKE 'ZLJ%'
