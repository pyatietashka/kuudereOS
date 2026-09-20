#!/usr/bin/env python3
# Kuudere Control Center
# Центр управления KuudereOS

import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import platform

class ControlCenter:
    def __init__(self, root):
        self.root = root
        self.root.title("Kuudere Control Center")
        self.root.geometry("700x650")
        self.root.configure(bg="#1a1a2e")

        # Заголовок
        header = tk.Frame(root, bg="#16213e")
        header.pack(fill=tk.X)

        tk.Label(
            header, text="kuudere OS", font=("Monospace", 20, "bold"),
            bg="#16213e", fg="#7fb3ff"
        ).pack(pady=10)

        tk.Label(
            header, text="Control Center — Beta 1 (Chito)",
            font=("Monospace", 10), bg="#16213e", fg="#7f8fa6"
        ).pack(pady=(0, 10))

        # Прокручиваемая область
        container = tk.Frame(root, bg="#1a1a2e")
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(
            container, bg="#1a1a2e",
            borderwidth=0, highlightthickness=0
        )
        scrollbar = tk.Scrollbar(container, command=canvas.yview)
        main = tk.Frame(canvas, bg="#1a1a2e")

        canvas.create_window((0, 0), window=main, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        main.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Секция: Информация о системе
        tk.Label(
            main, text="📊 Система", font=("Monospace", 13, "bold"),
            bg="#1a1a2e", fg="#7fb3ff", anchor="w"
        ).pack(fill=tk.X, padx=20, pady=(10, 0))

        info_frame = tk.Frame(main, bg="#0f0f1e")
        info_frame.pack(fill=tk.X, padx=20, pady=5)

        info_text = self.get_system_info()
        tk.Label(
            info_frame, text=info_text, font=("Monospace", 10),
            bg="#0f0f1e", fg="#e0e0e0", justify=tk.LEFT, anchor="w"
        ).pack(fill=tk.X, padx=10, pady=10)

        # Секция: Программы
        tk.Label(
            main, text="🚀 Программы", font=("Monospace", 13, "bold"),
            bg="#1a1a2e", fg="#7fb3ff", anchor="w"
        ).pack(fill=tk.X, padx=20, pady=(15, 0))

        apps_frame = tk.Frame(main, bg="#1a1a2e")
        apps_frame.pack(fill=tk.X, padx=20, pady=5)

        apps = [
            ("📝 KuudereNotes", "kuuderenotes", False),
            ("✏ KuudereEdit", "kuudereedit", False),
            ("⚡ QuickRun", "python3 /home/pyatietashka/kuudereos-project/programs/quickrun/quickrun-compact.py", False),
            ("🔧 AutoBash", "python3 /home/pyatietashka/kuudereos-project/programs/autobash/autobash.py", True),
            ("📊 KuudereFetch", "kuuderefetch", True),
            ("🛒 KuudereStore", "kuuderestore", False),
            ("🎨 KuudereVersion", "kuudereversion", False),
            ("🔔 NotifyMe", "python3 /home/pyatietashka/kuudereos-project/programs/notifyme/notifyme.py", True),
        ]

        for name, cmd, in_terminal in apps:
            btn = tk.Button(
                apps_frame, text=name,
                command=lambda c=cmd, t=in_terminal: self.run_app(c, t),
                bg="#16213e", fg="#e0e0e0", font=("Monospace", 11),
                borderwidth=0, activebackground="#7fb3ff",
                activeforeground="#0f0f1e", anchor="w", padx=15, pady=8
            )
            btn.pack(fill=tk.X, pady=2)

        # Секция: Питание
        tk.Label(
            main, text="⚙ Питание", font=("Monospace", 13, "bold"),
            bg="#1a1a2e", fg="#7fb3ff", anchor="w"
        ).pack(fill=tk.X, padx=20, pady=(15, 0))

        power_frame = tk.Frame(main, bg="#1a1a2e")
        power_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Button(
            power_frame, text="🔄 Перезагрузить",
            command=lambda: self.power("reboot"),
            bg="#16213e", fg="#e0e0e0", font=("Monospace", 11),
            borderwidth=0, activebackground="#7fb3ff"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        tk.Button(
            power_frame, text="⏻ Выключить",
            command=lambda: self.power("poweroff"),
            bg="#16213e", fg="#ff6b6b", font=("Monospace", 11),
            borderwidth=0, activebackground="#ff6b6b"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # Отступ снизу
        tk.Frame(main, bg="#1a1a2e", height=20).pack()

        # Прокрутка колёсиком мыши
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

    def get_system_info(self):
        try:
            os_name = "KuudereOS"
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            os_name = line.split("=")[1].strip().strip('"')
                            break
            kernel = platform.release()
            host = platform.node()
            return f"OS: {os_name}\nKernel: {kernel}\nHost: {host}"
        except:
            return "OS: KuudereOS"

    def run_app(self, cmd, in_terminal=False):
        try:
            if in_terminal:
                subprocess.Popen(
                    f"x-terminal-emulator -e bash -c '{cmd}; echo; echo Нажмите Enter...; read'",
                    shell=True, start_new_session=True
                )
            else:
                subprocess.Popen(
                    cmd, shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить: {e}")

    def power(self, action):
        if messagebox.askyesno("KuudereOS", f"Вы уверены? ({action})"):
            subprocess.Popen(["sudo", action])

if __name__ == "__main__":
    root = tk.Tk()
    app = ControlCenter(root)
    root.mainloop()
