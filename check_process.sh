#!/bin/bash
# 检测本机运行程序并发送邮件报告
# 发件人: pandac00@163.com
# 收件人: 19922307306@189.cn

# ========== 配置区 ==========
SENDER="pandac00@163.com"
RECIPIENT="19922307306@189.cn"
SUBJECT="[OpenClaw] 服务器进程监控报告 - $(hostname) - $(date '+%Y-%m-%d %H:%M:%S')"
TEST_MODE=true

# ========== 检测函数 ==========

get_system_info() {
    echo "==================== 系统信息 ===================="
    echo "主机名: $(hostname)"
    echo "IP地址: $(curl -s ipinfo.io/ip 2>/dev/null || hostname -I)"
    echo "系统: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
    echo "内核: $(uname -r)"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "运行时长: $(uptime -p)"
    echo ""
}

get_resource_usage() {
    echo "==================== 资源使用 ===================="
    echo "--- CPU使用率 ---"
    top -bn1 | grep 'Cpu(s)' | awk '{print "使用率: " 100-$8 "%"}'
    echo ""
    echo "--- 内存使用 ---"
    free -h
    echo ""
    echo "--- 磁盘使用 ---"
    df -h | grep -E '^/dev|^Filesystem'
    echo ""
}

get_key_processes() {
    echo "==================== 关键进程 ===================="
    echo "--- 资源占用 Top 10 (CPU) ---"
    ps aux --sort=-%cpu | head -11
    echo ""
    echo "--- 资源占用 Top 10 (内存) ---"
    ps aux --sort=-%mem | head -11
    echo ""
}

get_network_status() {
    echo "==================== 网络状态 ===================="
    echo "--- 监听端口 ---"
    ss -tlnp 2>/dev/null | head -20
    echo ""
}

get_app_status() {
    echo "==================== 应用状态 ===================="
    if pgrep -f "openclaw" > /dev/null; then
        echo "OpenClaw: 运行中 (PID: $(pgrep -f openclaw))"
    else
        echo "OpenClaw: 未运行"
    fi
    if command -v docker &> /dev/null; then
        echo "Docker: $(docker --version 2>/dev/null)"
        echo "运行中的容器: $(docker ps -q 2>/dev/null | wc -l)"
    fi
    echo ""
}

get_recent_errors() {
    echo "==================== 最近错误日志 ===================="
    journalctl -p err --no-pager -n 5 2>/dev/null | tail -10
    echo ""
}

# ========== 主程序 ==========

main() {
    REPORT=""
    REPORT+=$(get_system_info)
    REPORT+=$(get_resource_usage)
    REPORT+=$(get_key_processes)
    REPORT+=$(get_network_status)
    REPORT+=$(get_app_status)
    REPORT+=$(get_recent_errors)
    
    REPORT+="==================== 报告结束 ===================="
    REPORT+=""
    REPORT+="此邮件由服务器监控脚本自动生成"
    
    if [ "$TEST_MODE" = true ]; then
        echo "========== 测试模式 =========="
        echo "收件人: $RECIPIENT"
        echo ""
        echo "$REPORT"
    else
        echo "$REPORT" | mail -s "$SUBJECT" -r "$SENDER" "$RECIPIENT"
        echo "邮件已发送至: $RECIPIENT"
    fi
}

main "$@"
