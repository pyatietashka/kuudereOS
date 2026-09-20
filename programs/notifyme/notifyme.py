#!/usr/bin/env python3
# NotifyMe for KuudereOS
# Показывает уведомление, когда команда заканчивает работу

import subprocess
import sys
import threading
import os
from datetime import datetime

def notify(title, message):
    """Показывает системное уведомление"""
    try:
        subprocess.run([
            "notify-send",
            "-i", "dialog-information",
            title, message
        ], check=True)
    except Exception as e:
        print(f"Не удалось показать уведомление: {e}")

def run_command(cmd, name=None):
    """Запускает команду и показывает уведомление по завершении"""
    if name is None:
        name = cmd[:50]

    start = datetime.now()
    print(f"[{start.strftime('%H:%M:%S')}] Запускаю: {cmd}")

    try:
        result = subprocess.run(
            cmd, shell=True,
            capture_output=True, text=True
        )
        end = datetime.now()
        duration = (end - start).total_seconds()

        if result.returncode == 0:
            notify(
                "✓ Команда выполнена",
                f"{name}\nВремя: {duration:.1f} сек"
            )
            print(f"[{end.strftime('%H:%M:%S')}] ✓ Готово за {duration:.1f} сек")
        else:
            notify(
                "✗ Ошибка команды",
                f"{name}\nКод: {result.returncode}"
            )
            print(f"[{end.strftime('%H:%M:%S')}] ✗ Ошибка (код {result.returncode})")

    except Exception as e:
        notify("✗ Ошибка", f"{name}\n{e}")
        print(f"✗ Исключение: {e}")

def run_in_background(cmd, name=None):
    """Запускает команду в фоне, чтобы не блокировать"""
    thread = threading.Thread(target=run_command, args=(cmd, name))
    thread.daemon = True
    thread.start()
    return thread

def main():
    if len(sys.argv) < 2:
        print("NotifyMe для KuudereOS")
        print()
        print("Использование:")
        print("  notifyme <команда>            — запустить команду")
        print("  notifyme --name 'Имя' <команда> — с именем")
        print()
        print("Примеры:")
        print("  notifyme 'sleep 10'")
        print("  notifyme --name 'Бэкап' 'cp -r ~/Документы ~/Бэкап'")
        return

    args = sys.argv[1:]
    name = None

    if args[0] == "--name" and len(args) >= 3:
        name = args[1]
        cmd = " ".join(args[2:])
    else:
        cmd = " ".join(args)

    run_command(cmd, name)

if __name__ == "__main__":
    main()
