#!/usr/bin/env python3
# KuudereEdit for KuudereOS
# Лёгкий редактор в стиле KuudereOS

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

class KuudereEdit:
    def __init__(self, root, filename=None):
        self.root = root
        self.root.title("KuudereEdit")
        self.root.geometry("900x600")
        self.root.configure(bg="#1a1a2e")

        self.current_file = None

        # Верхняя панель с кнопками
        toolbar = tk.Frame(root, bg="#16213e")
        toolbar.pack(fill=tk.X)

        # Кнопки
        buttons = [
            ("📂 Открыть", self.open_file),
            ("💾 Сохранить", self.save_file),
            ("💾 Сохранить как", self.save_as),
            ("✖ Выход", self.quit_app),
        ]

        for text, cmd in buttons:
            btn = tk.Button(
                toolbar, text=text, command=cmd,
                bg="#0f0f1e", fg="#e0e0e0", font=("Monospace", 10),
                borderwidth=0, activebackground="#7fb3ff",
                activeforeground="#0f0f1e", padx=10, pady=5
            )
            btn.pack(side=tk.LEFT, padx=2, pady=5)

        # Поле редактирования
        self.text = tk.Text(
            root, font=("Monospace", 12),
            bg="#0f0f1e", fg="#e0e0e0",
            insertbackground="#7fb3ff",
            selectbackground="#7fb3ff", selectforeground="#0f0f1e",
            borderwidth=0, wrap=tk.NONE,
            undo=True
        )
        self.text.pack(fill=tk.BOTH, expand=True)

        # Скроллбар
        scroll = tk.Scrollbar(self.text)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scroll.set)
        scroll.config(command=self.text.yview)

        # Строка статуса
        self.status = tk.Label(
            root, text="Готово", font=("Monospace", 9),
            bg="#16213e", fg="#7f8fa6", anchor="w", padx=10
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

        # Горячие клавиши
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-n>", lambda e: self.new_file())

        # Если передан файл — открыть
        if filename and os.path.exists(filename):
            self.load_file(filename)

    def update_title(self):
        name = self.current_file if self.current_file else "Без имени"
        self.root.title(f"KuudereEdit — {name}")
        self.status.config(text=f"Файл: {name}")

    def new_file(self):
        self.text.delete("1.0", tk.END)
        self.current_file = None
        self.update_title()

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Открыть файл",
            filetypes=[("Все файлы", "*.*"), ("Текст", "*.txt")]
        )
        if path:
            self.load_file(path)

    def load_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", content)
            self.current_file = path
            self.update_title()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть: {e}")

    def save_file(self):
        if not self.current_file:
            self.save_as()
            return
        try:
            content = self.text.get("1.0", tk.END).rstrip("\n")
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(content)
            self.status.config(text=f"Сохранено: {self.current_file}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    def save_as(self):
        path = filedialog.asksaveasfilename(
            title="Сохранить как",
            defaultextension=".txt",
            filetypes=[("Все файлы", "*.*"), ("Текст", "*.txt")]
        )
        if path:
            self.current_file = path
            self.save_file()
            self.update_title()

    def quit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    app = KuudereEdit(root, filename)
    root.mainloop()
