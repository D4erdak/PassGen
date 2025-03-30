import secrets
import string

def generate_password(length: int = 12, use_digits: bool = True,
                      use_special_chars: bool = True) -> str:
    """
    Генерирует криптографически стойкий случайный пароль с использованием модуля secrets.
    Соответствует современным стандартам безопасности паролей.

    Параметры:
        length (int): Длина генерируемого пароля. По умолчанию 12 символов.
                     Рекомендуется не менее 12 символов для безопасности.
        use_digits (bool): Включать ли цифры в пароль. По умолчанию True.
        use_special_chars (bool): Включать ли специальные символы. По умолчанию True.

    Возвращает:
        str: Сгенерированный криптографически стойкий пароль

    Исключения:
        ValueError: Если невозможно сгенерировать пароль с заданными параметрами

    Примеры:
        >>> generate_password()
        'aB3#kL9!pY2@'

        >>> generate_password(length=8, use_digits=True, use_special_chars=False)
        'xK7nL9qR'
    """

    # Базовый набор символов - всегда включаем буквы верхнего и нижнего регистра
    chars = string.ascii_letters  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Добавляем цифры, если требуется
    if use_digits:
        chars += string.digits  # '0123456789'

    # Добавляем специальные символы, если требуется
    if use_special_chars:
        chars += string.punctuation  # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    # Проверяем, что есть хотя бы один тип символов кроме букв
    if len(chars) == len(string.ascii_letters):
        raise ValueError("Пароль должен содержать хотя бы цифры или специальные символы")

    # Проверяем минимальную длину пароля
    if length < 8:
        raise ValueError("Длина пароля должна быть не менее 8 символов")

    # Генерация пароля:
    # 1. secrets.choice() криптографически безопасна в отличие от random.choice()
    # 2. Используем list comprehension для генерации каждого символа
    # 3. Объединяем символы в строку с помощью join()
    password = ''.join(secrets.choice(chars) for _ in range(length))

    return password