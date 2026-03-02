#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务器监控报告发送脚本
使用环境变量配置敏感信息:
  export EMAIL_USER=your_email@163.com
  export EMAIL_PASS=your_password
  export EMAIL_TO=recipient@189.cn
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import subprocess
import datetime
import os

# ========== 邮件配置 ==========
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER = os.environ.get("EMAIL_USER", "")
SENDER_PASSWORD = os.environ.get("EMAIL_PASS", "")
RECIPIENT = os.environ.get("EMAIL_TO", "")

# ========== 获取系统信息 ==========
def run_cmd(cmd):
    return subprocess.getoutput(cmd)

def get_system_info():
    return f"""主机名: {run_cmd("hostname")}
IP地址: {run_cmd("curl -s ipinfo.io/ip")}
运行时长: {run_cmd("uptime -p")}
时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""

def get_cpu_usage():
    cpu_line = run_cmd("grep cpu /proc/stat | head -1")
    parts = cpu_line.split()
    if len(parts) >= 5:
        user, nice, system, idle = int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4])
        total = user + nice + system + idle
        usage = (total - idle) / total * 100 if total > 0 else 0
        return f"{usage:.1f}%"
    return "N/A"

def get_memory():
    return run_cmd("free -h")

def get_disk():
    return run_cmd("df -h | grep -E '^/dev|^Filesystem'")

def get_top_processes():
    return run_cmd("ps aux --sort=-%mem | head -11")

def get_app_status():
    openclaw = "运行中" if run_cmd("pgrep -f openclaw") else "未运行"
    docker_count = run_cmd("docker ps -q 2>/dev/null | wc -l")
    return f"""OpenClaw: {openclaw}
Docker: {docker_count} 个容器运行中"""

# ========== 构建报告 ==========
def build_report():
    report = f"""
==================== 系统信息 ====================
{get_system_info()}

==================== 资源使用 ====================
CPU使用率: {get_cpu_usage()}

内存:
{get_memory()}

磁盘:
{get_disk()}

==================== 内存占用 Top 10 进程 ====================
{get_top_processes()}

==================== 应用状态 ====================
{get_app_status()}

==================== 报告结束 ====================
"""
    return report

# ========== 发送邮件 ==========
def send_email(content, subject="[OpenClaw] 服务器监控报告"):
    if not SENDER or not SENDER_PASSWORD or not RECIPIENT:
        print("错误: 请设置环境变量 EMAIL_USER, EMAIL_PASS, EMAIL_TO")
        return False
    
    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    msg["Subject"] = Header(subject, "utf-8")
    
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER, SENDER_PASSWORD)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.quit()
        print("邮件发送成功")
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False

# ========== 主程序 ==========
if __name__ == "__main__":
    report = build_report()
    print("--- 报告预览 ---")
    print(report)
    print("\n--- 发送邮件 ---")
    send_email(report)
