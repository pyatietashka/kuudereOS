#!/usr/bin/env python3
# KuudereVersion for KuudereOS
# Магазин версий KuudereOS

import tkinter as tk
from tkinter import messagebox
import subprocess
import json
import os
import sys

VERSIONS_FILE = os.path.expanduser("~/kuudereos-project/programs/kuudereversion/versions.json")

class KuudereVersion:
    def __init__(self, root):
        self.root = root
        self.root.title("KuudereVersion")
        self.root.geometry("750x600")
        self.root.configure(bg="#1a1a2e")

        self.versions = self.load_versions()

        # Заголовок
        header = tk.Frame(root, bg="#16213e")
        header.pack(fill=tk.X)
        tk.Label(
            header, text="🎨 KuudereVersion", font=("Monospace", 18, "bold"),
            bg="#16213e", fg="#7fb3ff"
        ).pack(pady=10)
        tk.Label(
            header, text="Выберите версию KuudereOS",
            font=("Monospace", 10), bg="#16213e", fg="#7f8fa6"
        ).pack(pady=(0, 10))

        # Проверка системы
        self.is_kuudereos = self.check_kuudereos()
        if not self.is_kuudereos:
            warn = tk.Label(
                root, text="⚠ Вы не на KuudereOS. Команда kuudereversion может не работать.",
                font=("Monospace", 9), bg="#1a1a2e", fg="#ff6b6b"
            )
            warn.pack(fill=tk.X, padx=10, pady=5)

        # Список версий
        canvas = tk.Canvas(root, bg="#1a1a2e", borderwidth=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(root, command=canvas.yview)
        self.frame = tk.Frame(canvas, bg="#1a1a2e")

        canvas.create_window((0, 0), window=self.frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Кнопка выхода
        bottom = tk.Frame(root, bg="#16213e")
        bottom.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Button(
            bottom, text="✖ Выход", command=root.destroy,
            bg="#0f0f1e", fg="#e0e0e0", font=("Monospace", 10),
            borderwidth=0, padx=10, pady=5
        ).pack(side=tk.RIGHT, padx=5, pady=5)

        self.render()

    def load_versions(self):
        if not os.path.exists(VERSIONS_FILE):
            return {}
        with open(VERSIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def check_kuudereos(self):
        try:
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release") as f:
                    content = f.read()
                    return "kuudereos" in content.lower()
        except:
            pass
        return False

    def copy_command(self, cmd):
        self.root.clipboard_clear()
        self.root.clipboard_append(cmd)
        messagebox.showinfo("KuudereVersion", "Команда скопирована в буфер обмена!")

    def install_version(self, key, version):
        name = version["name"]
        if messagebox.askyesno("KuudereVersion", f"Установить {name}?"):
            install_cmd = version.get("install", "")
            remove_cmd = version.get("remove", "")

            if remove_cmd:
                full = (
                    f"sudo apt remove -y {remove_cmd}; "
                    f"sudo apt autoremove -y; "
                    f"sudo apt install -y {install_cmd}"
                )
            else:
                full = f"sudo apt install -y {install_cmd}"

            subprocess.Popen(
                f"x-terminal-emulator -e bash -c '{full}; echo; echo Готово! Нажмите Enter...; read'",
                shell=True, start_new_session=True
            )

    def render(self):
        for key, version in self.versions.items():
            frame = tk.Frame(self.frame, bg="#16213e")
            frame.pack(fill=tk.X, padx=10, pady=5)

            # Название и описание
            info = tk.Frame(frame, bg="#16213e")
            info.pack(fill=tk.X, padx=10, pady=5)

            tk.Label(
                info, text=version["name"], font=("Monospace", 13, "bold"),
                bg="#16213e", fg="#7fb3ff", anchor="w"
            ).pack(fill=tk.X)

            tk.Label(
                info, text=version["desc"], font=("Monospace", 10),
                bg="#16213e", fg="#e0e0e0", anchor="w"
            ).pack(fill=tk.X)

            # Команда apt
            if version.get("remove"):
                apt_cmd = f"sudo apt remove {version['remove']} && sudo apt install {version['install']}"
            else:
                apt_cmd = f"sudo apt install {version['install']}"

            cmd_frame = tk.Frame(frame, bg="#0f0f1e")
            cmd_frame.pack(fill=tk.X, padx=10, pady=5)

            tk.Label(
                cmd_frame, text="Команда (работает на Debian-based):",
                font=("Monospace", 8), bg="#0f0f1e", fg="#7f8fa6", anchor="w"
            ).pack(fill=tk.X, padx=5, pady=(5, 0))

            tk.Label(
                cmd_frame, text=apt_cmd, font=("Monospace", 8),
                bg="#0f0f1e", fg="#a8c8ff", anchor="w", wraplength=700, justify=tk.LEFT
            ).pack(fill=tk.X, padx=5)

            # Кнопки
            btn_frame = tk.Frame(frame, bg="#16213e")
            btn_frame.pack(fill=tk.X, padx=10, pady=5)

            tk.Button(
                btn_frame, text="📋 Копировать команду",
                command=lambda c=apt_cmd: self.copy_command(c),
                bg="#0f0f1e", fg="#e0e0e0", font=("Monospace", 9),
                borderwidth=0, padx=10, pady=3
            ).pack(side=tk.LEFT, padx=2)

            tk.Button(
                btn_frame, text="⬇ Установить (KuudereOS)",
                command=lambda k=key, v=version: self.install_version(k, v),
                bg="#7fb3ff", fg="#0f0f1e", font=("Monospace", 9, "bold"),
                borderwidth=0, padx=10, pady=3
            ).pack(side=tk.RIGHT, padx=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = KuudereVersion(root)
    root.mainloop()
