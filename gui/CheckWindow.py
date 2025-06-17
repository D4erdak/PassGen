import tkinter as tk
from tkinter import ttk
import string
from typing import Dict, List


class CheckWindow:
    def __init__(self, master: tk.Toplevel) -> None:
        self.master = master
        self.setup_window()
        self.create_widgets()
        self.setup_style()

    def setup_window(self) -> None:
        self.master.title("🔍 Проверка надежности пароля")
        self.master.geometry("650x500")
        self.master.resizable(False, False)
        self.master.configure(bg="#f0f0f0")

    def setup_style(self) -> None:
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0")
        self.style.configure(
            "TButton",
            font=("Arial", 10),
            padding=8,
            background="#3498db",
            foreground="black"
        )
        self.style.map(
            "TButton",
            background=[("active", "#2980b9")]
        )

    def create_widgets(self) -> None:
        main_frame = ttk.Frame(self.master)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Заголовок
        ttk.Label(
            main_frame,
            text="🔍 Проверка надежности пароля",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))

        # Поле для ввода пароля
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill="x", pady=10)

        ttk.Label(input_frame, text="Введите пароль:").pack(side="left")

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            input_frame,
            textvariable=self.password_var,
            show="*",
            font=("Arial", 12),
            width=40
        )
        self.password_entry.pack(side="left", padx=10)

        # Кнопка проверки и видимости
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame,
            text="Проверить",
            command=self.check_password
        ).pack(side="left", padx=5)

        self.show_password_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            btn_frame,
            text="Показать пароль",
            variable=self.show_password_var,
            command=self.toggle_password_visibility
        ).pack(side="left", padx=5)

        # Результаты проверки
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill="both", expand=True, pady=20)

        ttk.Label(
            results_frame,
            text="Результаты проверки:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        self.results_text = tk.Text(
            results_frame,
            height=10,
            width=60,
            wrap="word",
            font=("Arial", 10),
            state="disabled",
            bg="white",
            padx=10,
            pady=10
        )
        self.results_text.pack(fill="both", expand=True)

        # Шкала надежности
        self.security_level = ttk.Label(
            main_frame,
            text="",
            font=("Arial", 12, "bold")
        )
        self.security_level.pack(pady=10)

    def toggle_password_visibility(self) -> None:
        """Переключает видимость пароля"""
        show = self.show_password_var.get()
        self.password_entry.config(show="" if show else "*")

    def check_password(self) -> None:
        """Проверяет пароль по нескольким критериям"""
        password = self.password_var.get()
        if not password:
            self.show_result("Введите пароль для проверки")
            return

        checks = self.run_security_checks(password)
        self.display_results(checks, password)

    def run_security_checks(self, password: str) -> Dict[str, bool]:
        """Выполняет комплексную проверку пароля"""
        checks = {
            "length": len(password) >= 12,
            "lowercase": any(c in string.ascii_lowercase for c in password),
            "uppercase": any(c in string.ascii_uppercase for c in password),
            "digits": any(c in string.digits for c in password),
            "special": any(c in string.punctuation for c in password),
            "common": password.lower() not in self.get_common_passwords(),
            "repeats": not any(password[i] == password[i + 1] == password[i + 2]
                               for i in range(len(password) - 2)),
            "sequences": not self.has_common_sequences(password)
        }
        return checks

    def get_common_passwords(self) -> List[str]:
        """Возвращает список распространенных паролей"""
        return [
            "password", "123456", "qwerty", "admin", "welcome",
            "12345678", "abc123", "password1", "12345", "123456789"
        ]

    def has_common_sequences(self, password: str) -> bool:
        """Проверяет наличие простых последовательностей"""
        sequences = [
            "123", "234", "345", "456", "567", "678", "789",
            "qwe", "wer", "ert", "rty", "tyu", "yui", "uio", "iop",
            "asd", "sdf", "dfg", "fgh", "ghj", "hjk", "jkl",
            "zxc", "xcv", "cvb", "vbn", "bnm"
        ]
        lower_pass = password.lower()
        return any(seq in lower_pass for seq in sequences)

    def display_results(self, checks: Dict[str, bool], password: str) -> None:
        """Отображает результаты проверки"""
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)

        # Подсчет выполненных проверок
        passed = sum(checks.values())
        total = len(checks)
        security_percent = int((passed / total) * 100)

        # Определение уровня безопасности
        if security_percent >= 90:
            level = "Отличный"
            color = "green"
        elif security_percent >= 70:
            level = "Хороший"
            color = "#4CAF50"
        elif security_percent >= 50:
            level = "Средний"
            color = "orange"
        else:
            level = "Слабый"
            color = "red"

        # Отображение уровня безопасности
        self.security_level.config(
            text=f"Уровень безопасности: {level} ({security_percent}%)",
            foreground=color
        )

        # Детали проверки
        check_details = {
            "length": f"Длина ≥ 12 символов: {len(password)}/12",
            "lowercase": "Содержит строчные буквы",
            "uppercase": "Содержит заглавные буквы",
            "digits": "Содержит цифры",
            "special": "Содержит спецсимволы",
            "common": "Не является распространенным паролем",
            "repeats": "Нет повторяющихся символов подряд",
            "sequences": "Нет простых последовательностей"
        }

        for check, passed in checks.items():
            status = "✓" if passed else "✗"
            color = "green" if passed else "red"
            self.results_text.insert(
                tk.END,
                f"{status} {check_details[check]}\n",
                "green" if passed else "red"
            )

        self.results_text.tag_config("green", foreground="green")
        self.results_text.tag_config("red", foreground="red")
        self.results_text.config(state="disabled")

    def show_result(self, message: str) -> None:
        """Показывает простое сообщение"""
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, message)
        self.results_text.config(state="disabled")
        self.security_level.config(text="", foreground="black")