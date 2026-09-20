#!/usr/bin/env python3
# TaskBot for KuudereOS
# Планировщик задач: запускает команды по расписанию

import subprocess
import os
import time
from datetime import datetime

TASKS_FILE = os.path.expanduser("~/.config/taskbot/tasks.txt")
LOG = os.path.expanduser("~/.config/taskbot/taskbot.log")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def load_tasks():
    """Загружает задачи из файла.
    Формат: HH:MM | команда
    """
    if not os.path.exists(TASKS_FILE):
        return []
    
    tasks = []
    with open(TASKS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "|" in line:
                time_str, cmd = line.split("|", 1)
                tasks.append((time_str.strip(), cmd.strip()))
    return tasks

def run_task(cmd):
    log(f"→ Запускаю: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            log(f"✓ Готово")
        else:
            log(f"✗ Ошибка (код {result.returncode})")
    except Exception as e:
        log(f"✗ Исключение: {e}")

def main():
    log("TaskBot запущен")
    
    while True:
        now = datetime.now().strftime("%H:%M")
        tasks = load_tasks()
        
        for task_time, cmd in tasks:
            if task_time == now:
                run_task(cmd)
                # Чтобы не запустить дважды в одну минуту
                time.sleep(60)
        
        time.sleep(30)

if __name__ == "__main__":
    main()
