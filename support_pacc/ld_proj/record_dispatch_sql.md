# 1. 查询无支付密码的账号确认收货的明细

SELECT * FROM `record_dispatch` WHERE pay_pw='AAAAAA' ORDER BY confirm_date, confirm_time

# 2. 按日期归类查询无支付密码的账号确认收货的时间（最大值与最小值）与回收总量

SELECT confirm_date, MIN(confirm_time), MAX(confirm_time), COUNT(buy_coins) FROM `record_dispatch` WHERE pay_pw='AAAAAA' GROUP BY confirm_date

