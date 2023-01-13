# 1. 查询所有记录

## 1.1. 通过工号

SELECT * FROM `record_idle_fish` WHERE Job_N='JCJ019' ORDER BY record_date DESC
SELECT * FROM `record_idle_fish` WHERE Job_N='ZLJ042' ORDER BY record_date DESC
SELECT * FROM `record_idle_fish` WHERE Job_N='AAA011' ORDER BY record_date DESC

## 1.2. 通过主机名

SELECT * FROM `record_idle_fish` WHERE `hosts` = 'C3:174' ORDER BY record_date DESC
