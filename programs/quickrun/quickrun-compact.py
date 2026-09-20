#!/usr/bin/env python3
# QuickRun Compact for KuudereOS
# Как Win+R: маленькое окно, одна команда, Enter — выполнить

import tkinter as tk
import subprocess
import os

HINTS_FILE = os.path.expanduser("~/kuudereos-project/programs/quickrun/hints.txt")

class QuickRunCompact:
    def __init__(self, root):
        self.root = root
        self.root.title("QuickRun")
        self.root.geometry("500x90")
        self.root.configure(bg="#1a1a2e")
        self.root.attributes("-topmost", True)  # поверх всех окон

        # Загружаем подсказки
        self.hints = self.load_hints()

        # Поле ввода
        self.entry = tk.Entry(
            root, font=("Monospace", 14),
            bg="#16213e", fg="#e0e0e0",
            insertbackground="#e0e0e0"
        )
        self.entry.pack(fill=tk.X, padx=10, pady=(10, 5))
        self.entry.bind("<Return>", self.run_command)
        self.entry.bind("<Escape>", lambda e: self.root.destroy())
        self.entry.bind("<KeyRelease>", self.show_hints)
        self.entry.focus()

        # Метка подсказок
        self.hint_label = tk.Label(
            root, text="", font=("Monospace", 9),
            bg="#1a1a2e", fg="#7f8fa6", justify=tk.LEFT, anchor="w"
        )
        self.hint_label.pack(fill=tk.X, padx=10, pady=(0, 5))

    def load_hints(self):
        hints = {}
        if not os.path.exists(HINTS_FILE):
            return hints
        with open(HINTS_FILE, "r") as f:
            for line in f:
                if "|" in line:
                    cmd, desc = line.strip().split("|", 1)
                    hints[cmd] = desc
        return hints

    def show_hints(self, event):
        text = self.entry.get().strip()
        if not text:
            self.hint_label.config(text="")
            return

        matches = []
        for cmd, desc in self.hints.items():
            if cmd.startswith(text) and cmd != text:
                matches.append(f"{cmd} — {desc}")

        if matches:
            self.hint_label.config(text="\n".join(matches[:3]))
        else:
            self.hint_label.config(text="")

    def run_command(self, event):
        cmd = self.entry.get().strip()
        if not cmd:
            return

        try:
            # Запускаем в фоне, без ожидания
            subprocess.Popen(
                cmd, shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        except Exception as e:
            print(f"Ошибка: {e}")

        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuickRunCompact(root)
    root.mainloop()
