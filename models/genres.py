class Genre:

    def __init__(self, genres_id: int, genre_name: str):
        self._genres_id = genres_id
        self._genre_name = genre_name

    def to_dict(self) -> dict:
        return {
            "genres_id": self._genres_id,
            "genre_name": self._genre_name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Genre":
        return cls(
            genres_id=data["genres_id"],
            genre_name=data["genre_name"],
        )