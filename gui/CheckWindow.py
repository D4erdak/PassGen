import tkinter as tk
from tkinter import ttk


class CheckWindow:
    def __init__(self, master: tk.Toplevel) -> None:
        self.master = master
        self.setup_window()
        self.create_widgets()

    def setup_window(self) -> None:
        self.master.title("🔍 Проверка надежности пароля")
        self.master.geometry("600x400")
        self.master.resizable(False, False)

    def create_widgets(self) -> None:
        # Заголовок
        ttk.Label(
            self.master,
            text="Проверка надежности пароля",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        # Поле для ввода пароля
        ttk.Label(self.master, text="Введите пароль для проверки:").pack()

        self.password_entry = ttk.Entry(
            self.master,
            show="*",
            font=("Arial", 12),
            width=40
        )
        self.password_entry.pack(pady=10)

        # Кнопка проверки
        ttk.Button(
            self.master,
            text="Проверить",
            command=self.check_password
        ).pack(pady=20)

        # Область для вывода результата
        self.result_label = ttk.Label(
            self.master,
            text="",
            font=("Arial", 12),
            wraplength=500
        )
        self.result_label.pack()

    def check_password(self) -> None:
        """Анализирует введенный пароль"""
        password = self.password_entry.get()

        # Здесь будет логика проверки пароля
        if len(password) < 8:
            self.result_label.config(text="❌ Слишком короткий пароль (минимум 8 символов)")
        else:
            self.result_label.config(text="✅ Пароль соответствует базовым требованиям")