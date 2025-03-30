"""
Модуль для работы с буфером обмена.

Предоставляет безопасные функции копирования текста в системный буфер обмена
с обработкой ошибок и проверкой поддерживаемых типов данных.
"""

import pyperclip
from typing import Union


def copy_to_clipboard(text: Union[str, int, float]) -> bool:
    """
    Копирует текст в системный буфер обмена безопасным способом.

    Параметры:
        text (str|int|float): Текст для копирования. Числа автоматически
                            преобразуются в строку.

    Возвращает:
        bool: True если копирование успешно, False при ошибке.

    Исключения:
        TypeError: Если передан неподдерживаемый тип данных
    """
    # Проверка и преобразование входных данных
    if text is None:
        return False

    if not isinstance(text, (str, int, float)):
        raise TypeError("Поддерживаются только строки и числа")

    # Преобразование чисел в строку
    text_str = str(text) if isinstance(text, (int, float)) else text

    # Проверка на пустую строку
    if not text_str.strip():
        return False

    try:
        pyperclip.copy(text_str)
        return True
    except pyperclip.PyperclipException:
        # Логирование ошибки можно добавить при необходимости
        return False
    except Exception as e:
        # Перехват всех остальных исключений
        return False