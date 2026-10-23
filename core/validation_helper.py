import re


class ValidationHelper:

    # Паттерн имени: каждое слово с заглавной буквы
    _NAME_PATTERN = re.compile(r"^[A-ZА-ЯЁ][a-zа-яё']*(?:[-\s][A-ZА-ЯЁ][a-zа-яё']*)*$")

    # Паттерн email: user@domain.tld
    _EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    # Проверка имени по паттерну
    @classmethod
    def validate_name(cls, name: str) -> bool:
        return cls._NAME_PATTERN.fullmatch(name) is not None

    # Проверка email по паттерну
    @classmethod
    def validate_email(cls, email: str) -> bool:
        return cls._EMAIL_PATTERN.fullmatch(email) is not None

    # Проверка адреса: строка должна быть непустой и содержать буквы/цифры
    @classmethod
    def validate_address(cls, address: str) -> bool:
        normalized = " ".join(str(address or "").split())
        return bool(normalized) and bool(re.fullmatch(r"[A-Za-zА-Яа-яЁё0-9.,/\-\s]+", normalized))

    # Проверка, что значение приводится к float
    @classmethod
    def validate_price(cls, value) -> bool:
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False