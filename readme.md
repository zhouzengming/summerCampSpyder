# 学校通知爬虫脚本
用于获取最新夏令营相关信息 

## 功能
1. 爬取武大网络空间安全学院、数学与统计学院、计算机学院、华科网络空间安全学院通知，并将最新消息发送到指定邮箱。
2. 发送爬虫日志到指定邮箱。

## 使用方法
1. 在utils.py第9-10行添加发件人的yeah邮箱相关信息
2. 在mainSpyder.py第4行添加收件人邮箱
3. 在uploadLog.py第3行添加收件人邮箱
4. 在系统中添加cron定时任务，建议每十分钟执行一次mainSpyder.py，每日执行一次uploadLog.py

## 注：
1. 发件邮箱若不是yeah邮箱则须在utils中修改对应的stmp服务器地址和端口