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

# 3. 查询所有需要回收的账号信息
SELECT role, user_name , coins FROM idle_fish WHERE role LIKE '宗毛毛%' and coins >= 30000 ORDER BY coins desc

# 4. 查询所有以xy开头的账号
SELECT * FROM `idle_fish` WHERE user_name LIKE 'xy%'
