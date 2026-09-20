#!/usr/bin/env python3
# AutoBash for KuudereOS
# Запускает команды из файла ~/.config/autobash/commands.txt

import subprocess
import os
import sys
from datetime import datetime

CONFIG = os.path.expanduser("~/.config/autobash/commands.txt")
LOG = os.path.expanduser("~/.config/autobash/autobash.log")

def log(message):
    """Пишет сообщение в лог и в консоль"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def run_commands():
    log("AutoBash запущен")

    if not os.path.exists(CONFIG):
        log(f"Файл с командами не найден: {CONFIG}")
        return

    with open(CONFIG, "r") as f:
        commands = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not commands:
        log("Нет команд для выполнения")
        return

    log(f"Запускаю {len(commands)} команд...")
    for cmd in commands:
        log(f"→ {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                log(f"✓ Готово")
                if result.stdout.strip():
                    log(f"  Вывод: {result.stdout.strip()}")
            else:
                log(f"✗ Ошибка (код {result.returncode})")
                if result.stderr.strip():
                    log(f"  Ошибка: {result.stderr.strip()}")
        except Exception as e:
            log(f"✗ Исключение: {e}")

    log("AutoBash завершён")

if __name__ == "__main__":
    run_commands()
