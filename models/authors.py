# Класс-модель Author
class Author:

    def __init__(self, author_id: int, name: str):
        self._author_id = author_id
        self._name = name

    # Преобразование объекта в словарь
    def to_dict(self) -> dict:
        return {"author_id": self._author_id, "name": self._name}

    # Создание объекта из словаря
    @classmethod
    def from_dict(cls, data: dict) -> "Author":
        return cls(author_id=data["author_id"], name=data["name"])