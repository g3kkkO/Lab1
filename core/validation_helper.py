import re




class ValidationHelper:

    _NAME_PATTERN = re.compile(r"^[A-ZА-ЯЁ][a-zа-яё']*(?:[-\s][A-ZА-ЯЁ][a-zа-яё']*)*$")
    _EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    @classmethod
    def validate_name(cls, name: str) -> bool:
        return  cls._NAME_PATTERN.fullmatch(name) is not None

    @classmethod
    def validate_email(cls, email: str) -> bool:
        return  cls._EMAIL_PATTERN.fullmatch(email) is not None

    @classmethod                
    def validate_price(cls,value):
        try:
            float(value)
            return True
        except ValueError:
            return False


