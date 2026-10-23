# Класс-модель Publisher
class Publisher:

    def __init__(self, publisher_id: int, publisher_name: str):
        self._publisher_id = publisher_id
        self._publisher_name = publisher_name

    # Преобразование объекта в словарь
    def to_dict(self) -> dict:
        return {
            "publisher_id": self._publisher_id,
            "publisher_name": self._publisher_name,
        }

    # Создание объекта из словаря
    @classmethod
    def from_dict(cls, data: dict) -> "Publisher":
        return cls(
            publisher_id=data["publisher_id"],
            publisher_name=data["publisher_name"],
        )