注意：一定是命令提示符而不是用PowerShell去执行命令

mysqldump.exe -V
mysqldump  Ver 8.0.30 for Win64 on x86_64 (MySQL Community Server - GPL)

mysqldump -u%s -p%s --default-character-set=utf8 -h%s  %s > %s%s.sql
mysqldump [选项] 数据库名 [表名] > 脚本名
mysqldump account > account.sql
