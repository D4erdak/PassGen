"""
Модуль главного окна приложения "Генератор паролей PRO".

Содержит класс MainWindow, который реализует графический интерфейс пользователя
с использованием библиотеки Tkinter.
"""

import tkinter as tk
from tkinter import ttk
from generator.PasswordGeneration import generate_password
from utils.Clipboard import copy_to_clipboard


class MainWindow:
    """
    Класс главного окна приложения.

    Отвечает за создание и управление всеми элементами интерфейса.
    """

    def __init__(self, master: tk.Tk) -> None:
        """
        Инициализация главного окна.

        Параметры:
            master (tk.Tk): Корневое окно Tkinter
        """
        self.master = master
        self.setup_window()
        self.setup_style()
        self.create_widgets()
        self.setup_bindings()

    def setup_window(self) -> None:
        """Настройка основных параметров окна."""
        self.master.title("🔐 Генератор паролей PRO")
        self.master.geometry("800x600")
        self.master.resizable(False, False)
        self.master.configure(bg="#f0f0f0")

        # Центрирование окна на экране
        self.center_window()

    def center_window(self) -> None:
        """Центрирует окно на экране."""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'+{x}+{y}')

    def setup_style(self) -> None:
        """Настройка стилей виджетов."""
        self.style = ttk.Style()

        # Общие настройки стилей
        self.style.configure(
            "TFrame",
            background="#f0f0f0",
            relief="flat"
        )

        # Стиль для кнопок
        self.style.configure(
            "TButton",
            font=("Arial", 12),
            padding=10,
            background="#4CAF50",
            foreground="black",
            borderwidth=1,
            focuscolor="#4CAF50"
        )

        # Состояния кнопок
        self.style.map(
            "TButton",
            background=[("active", "#45a049"), ("disabled", "#cccccc")],
            foreground=[("active", "white"), ("disabled", "#888888")]
        )

        # Стиль для поля ввода
        self.style.configure(
            "TEntry",
            font=("Consolas", 16),
            foreground="#2c3e50",
            padding=8,
            relief="solid"
        )

    def create_widgets(self) -> None:
        """Создание и размещение виджетов в окне."""
        # Основной контейнер
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(pady=50, padx=50, fill="both", expand=True)

        # Заголовок
        self.create_header()

        # Поле для отображения пароля
        self.create_password_display()

        # Кнопка генерации
        self.create_generate_button()

        # Панель управления
        self.create_control_panel()

    def create_header(self) -> None:
        """Создает заголовок приложения."""
        ttk.Label(
            self.main_frame,
            text="🔐 Генератор безопасных паролей",
            font=("Arial", 18, "bold"),
            background="#f0f0f0"
        ).pack(pady=(0, 30))

    def create_password_display(self) -> None:
        """Создает поле для отображения пароля."""
        self.password_var = tk.StringVar()

        self.password_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.password_var,
            font=("Consolas", 16),
            width=30,
            state="readonly",
            justify="center",
            foreground="#2c3e50",
            style="TEntry"
        )
        self.password_entry.pack(pady=10, ipady=8)

    def create_generate_button(self) -> None:
        """Создает кнопку генерации пароля."""
        ttk.Button(
            self.main_frame,
            text="🔄 Сгенерировать пароль",
            command=self.on_generate_click,
            style="TButton"
        ).pack(pady=20)

    def create_control_panel(self) -> None:
        """Создает панель управления с настройками."""
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(pady=20)

        # Длина пароля
        self.create_length_control(control_frame)

        # Чекбоксы настроек
        self.create_checkboxes(control_frame)

        # Кнопка копирования
        self.create_copy_button(control_frame)

    def create_length_control(self, parent: ttk.Frame) -> None:
        """Создает элементы управления длиной пароля."""
        ttk.Label(
            parent,
            text="Длина пароля:",
            font=("Arial", 10)
        ).grid(row=0, column=0, padx=5, sticky="e")

        self.length_var = tk.IntVar(value=12)

        ttk.Spinbox(
            parent,
            from_=8,
            to=32,
            textvariable=self.length_var,
            width=5,
            font=("Arial", 10),
            wrap=True
        ).grid(row=0, column=1, padx=5, sticky="w")

    def create_checkboxes(self, parent: ttk.Frame) -> None:
        """Создает чекбоксы для настроек пароля."""
        # Чекбокс для цифр
        self.digits_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            parent,
            text="Цифры (0-9)",
            variable=self.digits_var,
            style="TCheckbutton"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Чекбокс для спецсимволов
        self.symbols_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            parent,
            text="Спецсимволы (!@#)",
            variable=self.symbols_var,
            style="TCheckbutton"
        ).grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def create_copy_button(self, parent: ttk.Frame) -> None:
        """Создает кнопку копирования пароля."""
        ttk.Button(
            parent,
            text="📋 Копировать",
            command=self.handle_copy,
            style="TButton"
        ).grid(row=2, columnspan=2, pady=10)

    def setup_bindings(self) -> None:
        """Настраивает обработчики событий."""
        # Копирование по Ctrl+C
        self.master.bind('<Control-c>', lambda e: self.handle_copy())

        # Генерация по F5
        self.master.bind('<F5>', lambda e: self.on_generate_click())

    def on_generate_click(self) -> None:
        """
        Обработчик нажатия кнопки генерации пароля.

        Генерирует новый пароль с текущими настройками и отображает его.
        """
        try:
            password = generate_password(
                length=self.length_var.get(),
                use_digits=self.digits_var.get(),
                use_special_chars=self.symbols_var.get()
            )
            self.password_var.set(password)
        except Exception as e:
            self.password_var.set("Ошибка генерации!")
            self.master.after(2000, lambda: self.password_var.set(""))

    def handle_copy(self) -> None:
        """
        Обработчик копирования пароля в буфер обмена.

        При успешном копировании временно меняет цвет текста на зеленый.
        """
        if self.password_var.get():
            if copy_to_clipboard(self.password_var.get()):
                original_color = self.password_entry.cget("foreground")
                self.password_entry.config(foreground="green")
                self.master.after(
                    1000,
                    lambda: self.password_entry.config(foreground=original_color))