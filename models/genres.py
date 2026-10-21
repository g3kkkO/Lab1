class Genre:

    def __init__(self, genre_id: int, genre_name: str):
        self._genre_id = genre_id
        self._genre_name = genre_name

    def to_dict(self) -> dict:
        return {
            "genre_id": self._genre_id,
            "genre_name": self._genre_name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Genre":
        return cls(
            genre_id=data["genre_id"],
            genre_name=data["genre_name"],
        )