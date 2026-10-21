# Класс-модель Customer
class Customer:

    def __init__(self, customer_id: int, name: str, email: str):
        self._customer_id = customer_id
        self._name = name
        self._email = email

    # Преобразование объекта в словарь
    def to_dict(self) -> dict:
        return {
            "customer_id": self._customer_id,
            "name": self._name,
            "email": self._email,
        }

    # Создание объекта из словаря
    @classmethod
    def from_dict(cls, data: dict) -> "Customer":
        return cls(
            customer_id=data["customer_id"],
            name=data["name"],
            email=data["email"],
        )