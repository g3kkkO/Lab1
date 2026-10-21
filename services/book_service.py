from core.manager import Manager
from models.books import Book
from core.exceptions import (AuthorNotFound, NameTypeError, IdTypeError,
                             YearValueError, PriceValueError, StockValueError,
                             BookNotFound)
from core.validation_helper import ValidationHelper
from datetime import datetime


# Сервис Book — бизнес-логика и валидация для CRUD
class BookService:

    # Инициализация: менеджер репозиториев
    def __init__(self, db: Manager):
        self.db = db

    # READ: получить все книги
    def get_all(self) -> list[Book]:
        return self.db.book.get_all()

    # CREATE: создать книгу (валидация всех полей)
    def create_book(self, title: str, author_ids: list[str], publisher_id: str,
                    year: str, genres_ids: list[str], price: str, stock: str) -> Book:
        self._validate_params(title, author_ids, publisher_id, year, genres_ids, price, stock)
        return self.db.book.create_book(
            title=" ".join(title.split()),
            author_ids=[int(a) for a in author_ids],
            publisher_id=int(publisher_id),
            year=int(year),
            genres_ids=[int(g) for g in genres_ids],
            price=float(price),
            stock=int(stock),
        )

    # READ: найти книгу по ID
    def get_book(self, book_id: str) -> Book:
        if not book_id.isdigit() or int(book_id) <= 0:
            raise IdTypeError
        book_id = int(book_id)
        book = self.db.book.find_book_by_id(book_id=book_id)
        if not book:
            raise BookNotFound
        return book

    # UPDATE: изменить название
    def update_title(self, book_id: str, title: str) -> Book:
        if not book_id.isdigit() or int(book_id) <= 0:
            raise IdTypeError
        updated = self.db.book.update_title(int(book_id), title)
        if not updated:
            raise BookNotFound
        return updated

    # UPDATE: изменить список авторов
    def update_author_ids(self, book_id: str, author_ids: list[str]) -> Book:
        if not book_id.isdigit() or int(book_id) <= 0:
            raise IdTypeError
        self._validate_ids(author_ids)
        updated = self.db.book.update_author_ids(int(book_id), [int(a) for a in author_ids])
        if not updated:
            raise BookNotFound
        return updated

    # UPDATE: изменить издателя
    def update_publisher_id(self, book_id: str, publisher_id: str) -> Book:
        if not book_id.isdigit() or int(book_id) <= 0:
            raise IdTypeError
        if not publisher_id.isdigit() or int(publisher_id) <= 0:
            raise IdTypeError
        updated = self.db.book.update_publisher_id(int(book_id), int(publisher_id))
        if not updated:
            raise BookNotFound
        return updated

    # UPDATE: изменить год
    def update_year(self, book_id: str, year: str) -> Book:
        if not book_id.isdigit() or int(book_id) <= 0:
            raise IdTypeError
        current_year = datetime.now().year
        if not year.isdigit() or not (0 < int(year) <= current_year):
            raise YearValueError
        updated = self.db.book.update_year(int(book_id), int(year))
        if not updated:
            raise BookNotFound
        return updated

    # UPDATE: изменить жанры
    def update_genres(self, book_id: str, genres_ids: list[str]) -> Book:
        if not book_id.isdigit() or int(book_id) <= 0:
            raise IdTypeError
        self._validate_ids(genres_ids)
        updated = self.db.book.update_genres(int(book_id), [int(g) for g in genres_ids])
        if not updated:
            raise BookNotFound
        return updated

    # UPDATE: изменить цену
    def update_price(self, book_id: str, price: str) -> Book:
        if not book_id.isdigit() or int(book_id) <= 0:
            raise IdTypeError
        if not ValidationHelper.validate_price(price) or float(price) <= 0:
            raise PriceValueError
        updated = self.db.book.update_price(int(book_id), float(price))
        if not updated:
            raise BookNotFound
        return updated

    # UPDATE: изменить склад
    def update_stock(self, book_id: str, stock: str) -> Book:
        if not book_id.isdigit() or int(book_id) <= 0:
            raise IdTypeError
        if not stock.isdigit():
            raise StockValueError
        updated = self.db.book.update_stock(int(book_id), int(stock))
        if not updated:
            raise BookNotFound
        return updated

    # DELETE: удалить книгу по ID
    def delete_book(self, book_id: str) -> None:
        if not book_id.isdigit() or int(book_id) <= 0:
            raise IdTypeError
        book_id = int(book_id)
        deleted = self.db.book.delete_book(book_id)
        if deleted:
            print(f"Удалена книга {book_id}")
            return
        raise BookNotFound

    # Валидация всех параметров создания
    def _validate_params(self, title: str, author_ids: list[str], publisher_id: str,
                         year: str, genres_ids: list[str], price: str, stock: str) -> None:
        title = " ".join(title.split())

        self._validate_ids(author_ids)
        self._validate_ids(genres_ids)

        if not publisher_id.isdigit() or int(publisher_id) <= 0:
            raise IdTypeError

        current_year = datetime.now().year
        if not year.isdigit() or not (0 < int(year) <= current_year):
            raise YearValueError

        if not stock.isdigit():
            raise StockValueError

        if not ValidationHelper.validate_price(price) or float(price) <= 0:
            raise PriceValueError

    # Валидация списка ID (каждый — число > 0)
    def _validate_ids(self, ids: list[str]) -> None:
        for raw_id in ids:
            if not raw_id.isdigit() or int(raw_id) <= 0:
                raise IdTypeError