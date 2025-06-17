import secrets
import string

def generate_password(length: int = 12, use_digits: bool = True,
                      use_special_chars: bool = True) -> str:
    chars = string.ascii_letters

    if use_digits:
        chars += string.digits

    if use_special_chars:
        chars += string.punctuation

    if len(chars) == len(string.ascii_letters):
        raise ValueError("Пароль должен содержать хотя бы цифры или специальные символы")

    if length < 8:
        raise ValueError("Длина пароля должна быть не менее 8 символов")

    password = ''.join(secrets.choice(chars) for _ in range(length))

    return password
