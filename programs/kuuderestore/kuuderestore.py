#!/usr/bin/env python3
# KuudereStore for KuudereOS
# Магазин приложений в стиле KuudereOS

import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import json
import os

APPS_FILE = os.path.expanduser("~/kuudereos-project/programs/kuuderestore/apps.json")

class KuudereStore:
    def __init__(self, root):
        self.root = root
        self.root.title("KuudereStore")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a2e")

        # Загрузка приложений
        self.apps = self.load_apps()

        # Заголовок
        header = tk.Frame(root, bg="#16213e")
        header.pack(fill=tk.X)
        tk.Label(
            header, text="🛒 KuudereStore", font=("Monospace", 18, "bold"),
            bg="#16213e", fg="#7fb3ff"
        ).pack(pady=10)

        # Поиск
        search_frame = tk.Frame(root, bg="#1a1a2e")
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(
            search_frame, text="🔍", font=("Monospace", 12),
            bg="#1a1a2e", fg="#7fb3ff"
        ).pack(side=tk.LEFT)
        self.search = tk.Entry(
            search_frame, font=("Monospace", 11),
            bg="#16213e", fg="#e0e0e0",
            insertbackground="#e0e0e0", borderwidth=0
        )
        self.search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search.bind("<KeyRelease>", lambda e: self.refresh())

        # Основная область: слева категории, справа список
        main = tk.Frame(root, bg="#1a1a2e")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Категории
        cat_frame = tk.Frame(main, bg="#16213e", width=180)
        cat_frame.pack(side=tk.LEFT, fill=tk.Y)
        cat_frame.pack_propagate(False)

        tk.Label(
            cat_frame, text="Категории", font=("Monospace", 11, "bold"),
            bg="#16213e", fg="#7fb3ff"
        ).pack(pady=5)

        self.category = tk.StringVar(value="Все")
        categories = ["Все"] + list(self.apps.keys())
        for cat in categories:
            rb = tk.Radiobutton(
                cat_frame, text=cat, variable=self.category, value=cat,
                command=self.refresh, bg="#16213e", fg="#e0e0e0",
                selectcolor="#0f0f1e", activebackground="#16213e",
                activeforeground="#7fb3ff", font=("Monospace", 10),
                anchor="w"
            )
            rb.pack(fill=tk.X, padx=5, pady=2)

        # Список приложений
        list_frame = tk.Frame(main, bg="#1a1a2e")
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            list_frame, bg="#1a1a2e", borderwidth=0, highlightthickness=0
        )
        scrollbar = tk.Scrollbar(list_frame, command=self.canvas.yview)
        self.apps_frame = tk.Frame(self.canvas, bg="#1a1a2e")

        self.canvas.create_window((0, 0), window=self.apps_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.apps_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.refresh()

    def load_apps(self):
        if not os.path.exists(APPS_FILE):
            return {}
        with open(APPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def is_installed(self, pkg):
        try:
            result = subprocess.run(
                ["dpkg", "-l", pkg],
                capture_output=True, text=True
            )
            return "ii" in result.stdout
        except:
            return False

    def install(self, pkg, name):
        if messagebox.askyesno("KuudereStore", f"Установить {name}?"):
            subprocess.Popen(
                f"x-terminal-emulator -e bash -c 'sudo apt install -y {pkg}; echo; echo Нажмите Enter...; read'",
                shell=True, start_new_session=True
            )

    def remove(self, pkg, name):
        if messagebox.askyesno("KuudereStore", f"Удалить {name}?"):
            subprocess.Popen(
                f"x-terminal-emulator -e bash -c 'sudo apt remove -y {pkg}; echo; echo Нажмите Enter...; read'",
                shell=True, start_new_session=True
            )

    def refresh(self):
        # Очистка
        for widget in self.apps_frame.winfo_children():
            widget.destroy()

        search_text = self.search.get().lower()
        cat = self.category.get()

        # Собираем список
        items = []
        for category, apps in self.apps.items():
            if cat != "Все" and category != cat:
                continue
            for app in apps:
                if search_text and search_text not in app["name"].lower() and search_text not in app["desc"].lower():
                    continue
                items.append((category, app))

        # Отображаем
        for category, app in items:
            frame = tk.Frame(self.apps_frame, bg="#16213e")
            frame.pack(fill=tk.X, pady=3)

            # Информация
            info = tk.Frame(frame, bg="#16213e")
            info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

            tk.Label(
                info, text=app["name"], font=("Monospace", 12, "bold"),
                bg="#16213e", fg="#e0e0e0", anchor="w"
            ).pack(fill=tk.X)

            tk.Label(
                info, text=app["desc"], font=("Monospace", 9),
                bg="#16213e", fg="#7f8fa6", anchor="w"
            ).pack(fill=tk.X)

            tk.Label(
                info, text=f"[{category}]", font=("Monospace", 8),
                bg="#16213e", fg="#7fb3ff", anchor="w"
            ).pack(fill=tk.X)

            # Кнопки
            btn_frame = tk.Frame(frame, bg="#16213e")
            btn_frame.pack(side=tk.RIGHT, padx=10)

            installed = self.is_installed(app["pkg"])

            if installed:
                tk.Button(
                    btn_frame, text="🗑 Удалить",
                    command=lambda p=app["pkg"], n=app["name"]: self.remove(p, n),
                    bg="#ff6b6b", fg="#0f0f1e", font=("Monospace", 9),
                    borderwidth=0, padx=10, pady=5
                ).pack()
            else:
                tk.Button(
                    btn_frame, text="⬇ Установить",
                    command=lambda p=app["pkg"], n=app["name"]: self.install(p, n),
                    bg="#7fb3ff", fg="#0f0f1e", font=("Monospace", 9),
                    borderwidth=0, padx=10, pady=5
                ).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = KuudereStore(root)
    root.mainloop()
