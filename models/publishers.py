class Publisher:

    def __init__(self, publisher_id: int, name: str, contact: str):
        self._publisher_id = publisher_id
        self._name = name
        self._contact = contact

    def to_dict(self) -> dict:
        return {
            "publisher_id": self._publisher_id,
            "name": self._name,
            "contact": self._contact,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Publisher":
        return cls(
            publisher_id=data["publisher_id"],
            name=data["name"],
            contact=data["contact"],
        )