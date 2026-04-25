import schedule
import time
import subprocess
import os

def run_monitor():
    print("⏰ 开始执行监控任务...")
    python_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv", "bin", "python")
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monitor.py")
    subprocess.run([python_path, script_path])

# 每天早上9点跑一次
schedule.every().day.at("09:00").do(run_monitor)


print("✅ 定时任务已启动，等待执行...")

while True:
    schedule.run_pending()
    time.sleep(30)