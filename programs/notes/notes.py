#!/usr/bin/env python3
# KuudereNotes for KuudereOS
# Заметки в стиле KuudereOS

import tkinter as tk
from tkinter import messagebox
import json
import os

NOTES_FILE = os.path.expanduser("~/.config/kuuderenotes/notes.json")

class KuudereNotes:
    def __init__(self, root):
        self.root = root
        self.root.title("KuudereNotes")
        self.root.geometry("800x500")
        self.root.configure(bg="#1a1a2e")

        self.notes = self.load_notes()
        self.current_index = None

        # Левая панель — список заметок
        left = tk.Frame(root, bg="#16213e", width=250)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)

        tk.Label(
            left, text="📝 Заметки", font=("Monospace", 14, "bold"),
            bg="#16213e", fg="#7fb3ff"
        ).pack(pady=10)

        self.listbox = tk.Listbox(
            left, font=("Monospace", 11),
            bg="#0f0f1e", fg="#e0e0e0",
            selectbackground="#7fb3ff", selectforeground="#0f0f1e",
            borderwidth=0, highlightthickness=0
        )
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Кнопки
        btn_frame = tk.Frame(left, bg="#16213e")
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(
            btn_frame, text="+ Новая", command=self.new_note,
            bg="#7fb3ff", fg="#0f0f1e", font=("Monospace", 10),
            borderwidth=0, activebackground="#a8c8ff"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        tk.Button(
            btn_frame, text="🗑 Удалить", command=self.delete_note,
            bg="#ff6b6b", fg="#0f0f1e", font=("Monospace", 10),
            borderwidth=0, activebackground="#ff9999"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # Правая панель — текст заметки
        right = tk.Frame(root, bg="#1a1a2e")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(
            right, text="Заголовок:", font=("Monospace", 11),
            bg="#1a1a2e", fg="#7fb3ff", anchor="w"
        ).pack(fill=tk.X, padx=10, pady=(10, 0))

        self.title_entry = tk.Entry(
            right, font=("Monospace", 12),
            bg="#16213e", fg="#e0e0e0",
            insertbackground="#e0e0e0", borderwidth=0
        )
        self.title_entry.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            right, text="Текст:", font=("Monospace", 11),
            bg="#1a1a2e", fg="#7fb3ff", anchor="w"
        ).pack(fill=tk.X, padx=10)

        self.text = tk.Text(
            right, font=("Monospace", 11),
            bg="#0f0f1e", fg="#e0e0e0",
            insertbackground="#e0e0e0", borderwidth=0, wrap=tk.WORD
        )
        self.text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Button(
            right, text="💾 Сохранить", command=self.save_note,
            bg="#7fb3ff", fg="#0f0f1e", font=("Monospace", 11, "bold"),
            borderwidth=0, activebackground="#a8c8ff"
        ).pack(pady=10)

        self.refresh_list()

    def load_notes(self):
        if not os.path.exists(NOTES_FILE):
            return []
        try:
            with open(NOTES_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    def save_notes(self):
        os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
        with open(NOTES_FILE, "w") as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for note in self.notes:
            self.listbox.insert(tk.END, note.get("title", "Без названия"))

    def on_select(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        self.current_index = selection[0]
        note = self.notes[self.current_index]
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note.get("title", ""))
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", note.get("text", ""))

    def new_note(self):
        self.notes.append({"title": "Новая заметка", "text": ""})
        self.save_notes()
        self.refresh_list()
        self.current_index = len(self.notes) - 1
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.current_index)
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, "Новая заметка")
        self.text.delete("1.0", tk.END)

    def save_note(self):
        if self.current_index is None:
            messagebox.showinfo("KuudereNotes", "Выберите заметку или создайте новую.")
            return
        self.notes[self.current_index]["title"] = self.title_entry.get()
        self.notes[self.current_index]["text"] = self.text.get("1.0", tk.END).strip()
        self.save_notes()
        self.refresh_list()
        self.listbox.selection_set(self.current_index)

    def delete_note(self):
        if self.current_index is None:
            return
        if messagebox.askyesno("KuudereNotes", "Удалить эту заметку?"):
            del self.notes[self.current_index]
            self.save_notes()
            self.refresh_list()
            self.current_index = None
            self.title_entry.delete(0, tk.END)
            self.text.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = KuudereNotes(root)
    root.mainloop()
