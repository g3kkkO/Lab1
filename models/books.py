class Book:

    def __init__(self, book_id: int, title: str,
                 author_ids: list[int], publisher_id: int,
                 year: int, genres_ids: list[int], price: float, stock: int):
        self._book_id = book_id
        self._title = title
        self._author_ids = author_ids
        self._publisher_id = publisher_id
        self._year = year
        self._genres_ids = genres_ids
        self._price = price
        self._stock = stock

    def to_dict(self) -> dict:
        return {
            "book_id": self._book_id,
            "title": self._title,
            "author_ids": self._author_ids,
            "publisher_id": self._publisher_id,
            "year": self._year,
            "genres_ids": self._genres_ids,
            "price": self._price,
            "stock": self._stock,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(
            book_id=data["book_id"],
            title=data["title"],
            author_ids=data["author_ids"],
            publisher_id=data["publisher_id"],
            year=data["year"],
            genres_ids=data["genres_ids"],
            price=data["price"],
            stock=data["stock"],
        )