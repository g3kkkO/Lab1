from pathlib import Path
from repositories.authors_repo import AuthorRepository
from repositories.books_repo import BookRepository
from repositories.customer_repo import CustomerRepository
from repositories.genres_repo import GenreRepository
from repositories.orders_repo import OrderRepository
from repositories.publisher_repo import PublisherRepository

# Добавлен менеджер для управления репозиториями
class Manager:

    def __init__(self, data_dir: str = "data", fmt: str = "json"):
        base = Path(data_dir)

        self.author = AuthorRepository(str(base / f"authors.{fmt}"))
        self.book = BookRepository(str(base / f"books.{fmt}"))
        self.customer = CustomerRepository(str(base / f"customers.{fmt}"))
        self.genre = GenreRepository(str(base / f"genres.{fmt}"))
        self.order = OrderRepository(str(base / f"orders.{fmt}"))
        self.publisher = PublisherRepository(str(base / f"publishers.{fmt}"))