# Server Monitor

服务器监控脚本 - 自动检测系统资源并发送邮件报告

## 功能

- 检测系统信息（主机名、IP、运行时长）
- 监控资源使用（CPU、内存、磁盘）
- 查看内存占用 Top 10 进程
- 检查应用状态（OpenClaw、Docker）
- 自动发送邮件报告

## 文件

- `send_email.py` - Python 邮件发送脚本
- `check_process.sh` - Bash 监控脚本

## 配置

使用环境变量配置邮箱信息：

```bash
export EMAIL_USER=your_email@163.com
export EMAIL_PASS=your_password
export EMAIL_TO=recipient@example.com
```

## 使用

```bash
# Python 脚本
python3 send_email.py

# Bash 脚本
./check_process.sh
```

## 定时任务

添加到 crontab 实现定时发送：

```bash
# 每天早上 8 点发送
0 8 * * * cd /root/server-monitor && python3 send_email.py
```

## 邮件服务器

默认使用 163 邮箱 SMTP（SSL 端口 465），可根据需要修改脚本中的 SMTP 配置。

## License

MIT
